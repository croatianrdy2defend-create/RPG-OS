#!/usr/bin/env python3
"""Optional, disposable lexical candidate index for one RPG OS campaign root.

Uses only the Python standard library and optional SQLite FTS5. Search results
are routes, never evidence: fetch reopens the source through read_source.py and
checks its revision. The cache must live outside the selected campaign root.
"""
from __future__ import annotations

import argparse
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import stat
import sys
import tempfile
import uuid

sys.dont_write_bytecode = True
try:
    from . import read_source
except ImportError:
    import read_source


SCHEMA_VERSION = "1"
SCOPES = ("current", "world", "history", "raw", "rules", "all")
TEXT_EXTENSIONS = {".md", ".markdown", ".txt", ".text"}
EXCLUDED_PARTS = {
    ".git", ".work", ".release", ".codex", ".agents", "__pycache__",
    "recovery", "handover", "campaigns", "othercampaigns", "other-campaigns",
    "other_campaigns", "local_campaigns", "private-campaigns", "private_campaigns",
}
RAW_EXCLUDED_PARTS = {
    "private", "privateartifact", "privateartifacts", "private-artifact",
    "private-artifacts", "private_artifact", "private_artifacts", "artifact",
    "artifacts", "manifest", "manifests",
}
FALLBACK = (
    "Use a known source pointer with read_source.py, or rebuild this optional "
    "cache. Missing lexical candidates never establish that a fact is absent."
)
ROUTE = re.compile(r"(?:INSTANCE|MODULES|ARCHIVE|EVIDENCE|ENGINE|OS)/[^\s<>\]\[)`|]+", re.I)
IDENTITY_KEY = r"(?:id|name|title|alias|aliases|entity_id|person_id|character_id)"


class SearchError(RuntimeError):
    def __init__(self, message: str, code: str = "index_error") -> None:
        super().__init__(message)
        self.code = code


def _no_link(path: Path) -> os.stat_result:
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
        raise SearchError(f"Symlink or reparse point refused: {path}", "unsafe_path")
    return info


def _root(root: str | Path) -> Path:
    # The shared reader checks every ancestor, even when the corpus is empty.
    read_source.root_identity(root)
    return Path(root).resolve(strict=True)


def _db_path(root: Path, db: str | Path) -> Path:
    path = Path(os.path.abspath(db))
    if path == root or root in path.parents:
        raise SearchError("The disposable database must be outside --root.", "unsafe_database")
    for component in reversed((path.parent, *path.parent.parents)):
        try:
            info = _no_link(component)
        except OSError as exc:
            raise SearchError(f"Database parent must exist and be accessible: {component}", "unsafe_database") from exc
        if not stat.S_ISDIR(info.st_mode):
            raise SearchError(f"Database parent is not a directory: {component}", "unsafe_database")
    try:
        info = _no_link(path)
    except FileNotFoundError:
        info = None
    except OSError as exc:
        raise SearchError(f"Cannot inspect database: {exc}", "unsafe_database") from exc
    if info is not None and not stat.S_ISREG(info.st_mode):
        raise SearchError("Database must be a regular file.", "unsafe_database")
    # Expand host aliases (including Windows 8.3 names) only after checking links.
    path = path.resolve(strict=info is not None)
    if path == root or root in path.parents:
        raise SearchError("The disposable database must be outside --root.", "unsafe_database")
    return path


def _scope(scope: str) -> str:
    if scope not in SCOPES:
        raise SearchError(f"Unknown scope: {scope}", "invalid_scope")
    return scope


def classify_source(relative: str) -> tuple[str, str] | None:
    """Strict allowlist; unknown locations never become current state."""
    if not isinstance(relative, str) or "\\" in relative:
        return None
    parts = relative.split("/")
    lower = [part.casefold() for part in parts]
    if any(not part or part in {".", ".."} or ":" in part for part in parts):
        return None
    if any(part in EXCLUDED_PARTS or part.startswith(".") for part in lower):
        return None
    suffix = Path(parts[-1]).suffix.casefold()
    top = lower[0]
    if len(parts) < 2:
        return None
    if top == "evidence":
        if len(parts) < 3 or lower[1] != "captures":
            return None
        if suffix not in TEXT_EXTENSIONS | {".jsonl"}:
            return None
        if any(part in RAW_EXCLUDED_PARTS for part in lower[2:]):
            return None
        stem = Path(parts[-1]).stem.casefold()
        if any(stem == word or stem.startswith(word + "_") or stem.startswith(word + "-")
               for word in RAW_EXCLUDED_PARTS):
            return None
        return "raw", "raw-capture"
    if suffix not in TEXT_EXTENSIONS:
        return None
    if top == "instance":
        if lower == ["instance", "corrections.md"]:
            return "rules", "correction-register"
        return "current", "current-record"
    if top == "modules":
        return "world", "world-record"
    if top == "archive":
        if Path(parts[-1]).stem.casefold() in {"index", "messages_ledger", "relation_ledger"}:
            return "history", "route-hint"
        return "history", "history-record"
    if top in {"engine", "os"}:
        return "rules", "rule-record"
    return None


def _walk_sources(root: Path, scope: str = "all") -> tuple[list[str], list[dict]]:
    paths: list[str] = []
    skipped: list[dict] = []

    def visit(path: Path) -> None:
        relative = path.relative_to(root).as_posix()
        lower = [part.casefold() for part in path.relative_to(root).parts]
        if scope == "rules" and lower[0] == "instance" and len(lower) > 1 and lower != ["instance", "corrections.md"]:
            return
        if any(part in EXCLUDED_PARTS or part.startswith(".") for part in lower):
            return
        if lower[:2] == ["evidence", "captures"] and any(part in RAW_EXCLUDED_PARTS for part in lower[2:]):
            return
        try:
            info = path.lstat()
        except OSError as exc:
            raise SearchError(f"Cannot inspect source {relative}: {exc}", "unreadable_source") from exc
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            skipped.append({"path": relative, "reason": "link-or-reparse-point"})
            return
        if stat.S_ISDIR(info.st_mode):
            # A nested campaign is a different root even if placed inside a module.
            try:
                children = sorted(path.iterdir(), key=lambda child: child.name)
            except OSError as exc:
                raise SearchError(f"Cannot list source directory {relative}: {exc}", "unreadable_source") from exc
            names = {child.name.casefold() for child in children}
            if len(lower) > 1 and {"instance", "os"} <= names:
                skipped.append({"path": relative, "reason": "nested-campaign-root"})
                return
            for child in children:
                visit(child)
        elif not stat.S_ISREG(info.st_mode):
            skipped.append({"path": relative, "reason": "special-file"})
        else:
            classification = classify_source(relative)
            if classification is not None and scope in {"all", classification[0]}:
                paths.append(relative)

    try:
        children = sorted(root.iterdir(), key=lambda child: child.name)
    except OSError as exc:
        raise SearchError(f"Cannot list campaign root: {exc}", "unreadable_source") from exc
    allowed_trees = {
        "current": {"instance"}, "world": {"modules"}, "history": {"archive"},
        "raw": {"evidence"}, "rules": {"instance", "engine", "os"},
        "all": {"instance", "modules", "archive", "evidence", "engine", "os"},
    }[scope]
    for child in children:
        if child.name.casefold() not in allowed_trees:
            continue
        if child.name.casefold() in {"instance", "modules", "archive", "engine", "os"}:
            visit(child)
        elif child.name.casefold() == "evidence":
            # Do not traverse sibling evidence directories or unknown artifacts.
            try:
                info = _no_link(child)
                if stat.S_ISDIR(info.st_mode):
                    for capture in child.iterdir():
                        if capture.name.casefold() == "captures":
                            visit(capture)
            except SearchError:
                skipped.append({"path": child.name, "reason": "link-or-reparse-point"})
            except OSError as exc:
                raise SearchError(f"Cannot inspect evidence captures: {exc}", "unreadable_source") from exc
    folded = [path.casefold() for path in paths]
    if len(folded) != len(set(folded)):
        raise SearchError("Case-colliding source paths are not portable.", "unsafe_path")
    return sorted(paths), skipped


def collect_sources(root: str | Path, scope: str = "all") -> tuple[list[dict], list[dict]]:
    _scope(scope)
    root = _root(root)
    paths, skipped = _walk_sources(root, scope)
    documents = []
    for relative in paths:
        try:
            document = read_source.load_document(root, relative)
        except read_source.SourceError as exc:
            if exc.code in {"invalid_utf8", "binary_source"}:
                skipped.append({"path": relative, "reason": exc.code})
                continue
            raise
        scope, source_class = classify_source(relative)
        document.update(scope=scope, source_class=source_class)
        documents.append(document)
    return documents, skipped


def _source_set(documents: list[dict]) -> dict[str, str]:
    return {item["path"]: item["sha256"] for item in documents}


def _set_hash(source_set: dict[str, str]) -> str:
    value = json.dumps(source_set, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def derive_identities(text: str) -> list[str]:
    """Reuse existing simple front matter and field-table identities, without YAML."""
    values: list[str] = []
    lines = text.splitlines()
    front_end = None
    if lines and lines[0].strip() == "---":
        front_end = next((i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if front_end is not None:
        active_alias = False
        for line in lines[1:front_end]:
            match = re.match(rf"^({IDENTITY_KEY})\s*:\s*(.*)$", line, re.I)
            if match:
                active_alias = match.group(1).casefold() in {"alias", "aliases"}
                values.append(match.group(2))
            elif active_alias and re.match(r"^\s*-\s+", line):
                values.append(re.sub(r"^\s*-\s+", "", line))
            elif line.strip():
                active_alias = False
    for line in lines:
        match = re.match(rf"^\s*\|\s*{IDENTITY_KEY}\s*\|\s*(.*?)\s*\|\s*$", line, re.I)
        if match:
            values.append(match.group(1))
    result = []
    for value in values:
        for entry in re.split(r"[,;|]", value.strip("[]")):
            entry = entry.strip(" \t\"'`")
            if entry and entry.casefold() not in {"none", "null", "[]"} and entry not in result:
                result.append(entry)
    return result


def fts5_available() -> bool:
    try:
        with closing(sqlite3.connect(":memory:")) as connection:
            connection.execute("CREATE VIRTUAL TABLE fts_probe USING fts5(body)")
        return True
    except sqlite3.Error:
        return False


def _require_fts() -> None:
    if not fts5_available():
        raise SearchError("SQLite FTS5 is unavailable. " + FALLBACK, "fts_unavailable")


def _schema(connection: sqlite3.Connection) -> None:
    connection.executescript("""
        PRAGMA journal_mode=DELETE;
        CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE sources (
            path TEXT PRIMARY KEY, sha256 TEXT NOT NULL, scope TEXT NOT NULL,
            source_class TEXT NOT NULL, identities TEXT NOT NULL
        );
        CREATE TABLE sections (
            id INTEGER PRIMARY KEY, path TEXT NOT NULL REFERENCES sources(path),
            section_id TEXT, heading TEXT NOT NULL, heading_path TEXT NOT NULL,
            start_line INTEGER NOT NULL, end_line INTEGER NOT NULL
        );
        CREATE VIRTUAL TABLE passages_fts USING fts5(
            heading, aliases, routes, body, tokenize='unicode61 remove_diacritics 2'
        );
    """)


def _document_sections(document: dict) -> list[dict]:
    sections = sorted(read_source.list_sections(document), key=lambda item: item["start_line"])
    if not sections:
        sections = [{"section_id": None, "heading": "", "heading_path": [],
                     "start_line": 1, "end_line": len(document["lines"])}]
    elif sections[0]["start_line"] > 1:
        sections.insert(0, {"section_id": None, "heading": "Preamble", "heading_path": [],
                            "start_line": 1, "end_line": sections[0]["start_line"] - 1})
    return sections


def _index_document(connection: sqlite3.Connection, document: dict) -> None:
    identities = derive_identities(document["text"])
    connection.execute("INSERT INTO sources VALUES (?, ?, ?, ?, ?)", (
        document["path"], document["sha256"], document["scope"],
        document["source_class"], json.dumps(identities, ensure_ascii=False),
    ))
    sections = _document_sections(document)
    for position, section in enumerate(sections):
        start, end = section["start_line"], section["end_line"]
        # Index each line once. Parent names/routes remain searchable context,
        # while a late child hit routes to that child instead of an entire file.
        own_end = min(end, sections[position + 1]["start_line"] - 1) if position + 1 < len(sections) else end
        body = "".join(document["lines"][start - 1:own_end])
        heading = section["heading"] or ""
        heading_path = section["heading_path"] or []
        cursor = connection.execute("""INSERT INTO sections
            (path, section_id, heading, heading_path, start_line, end_line)
            VALUES (?, ?, ?, ?, ?, ?)""", (
            document["path"], section["section_id"], heading,
            json.dumps(heading_path, ensure_ascii=False), start, end,
        ))
        routes = " ".join([document["path"], *heading_path, *ROUTE.findall(body)])
        connection.execute("INSERT INTO passages_fts(rowid, heading, aliases, routes, body) VALUES (?, ?, ?, ?, ?)", (
            cursor.lastrowid, " > ".join(heading_path) or heading,
            " ".join(identities), routes, body,
        ))


def _verify_database(connection: sqlite3.Connection) -> None:
    result = connection.execute("PRAGMA integrity_check").fetchall()
    if result != [("ok",)]:
        raise SearchError("New database failed its integrity check.", "rebuild_failed")
    connection.execute("INSERT INTO passages_fts(passages_fts) VALUES ('integrity-check')")
    if connection.execute("PRAGMA foreign_key_check").fetchall():
        raise SearchError("New database failed its reference check.", "rebuild_failed")


def build_index(root: str | Path, db: str | Path) -> dict:
    """Build a replacement, verify it and publish atomically; retain old on error."""
    root = _root(root)
    path = _db_path(root, db)
    _require_fts()
    documents, skipped = collect_sources(root)
    source_set = _source_set(documents)
    generation = str(uuid.uuid4())
    metadata = {
        "schema_version": SCHEMA_VERSION, "root_path": str(root),
        "root_id": read_source.root_identity(root), "generation": generation,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_count": str(len(documents)), "source_set_sha256": _set_hash(source_set),
    }
    descriptor, temporary_name = tempfile.mkstemp(prefix="." + path.name + ".build-", suffix=".sqlite3", dir=path.parent)
    os.close(descriptor)
    temporary = Path(temporary_name)
    connection = None
    try:
        connection = sqlite3.connect(temporary)
        _schema(connection)
        connection.executemany("INSERT INTO metadata VALUES (?, ?)", metadata.items())
        for document in documents:
            _index_document(connection, document)
        connection.commit()
        _verify_database(connection)
        connection.commit()
        section_count = connection.execute("SELECT count(*) FROM sections").fetchone()[0]
        connection.close()
        connection = None
        # Detect edits, additions and removals during construction before publish.
        verified, _ = collect_sources(root)
        if _source_set(verified) != source_set:
            raise SearchError("Source set changed during rebuild; previous database retained.", "source_changed")
        _db_path(root, path)
        with temporary.open("r+b") as stream:
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if connection is not None:
            connection.close()
        # Only our one temporary file and its SQLite journal may be removed.
        for candidate in (temporary, Path(str(temporary) + "-journal")):
            if candidate.parent != path.parent or not candidate.name.startswith("." + path.name + ".build-"):
                raise SearchError("Unsafe temporary cleanup path.", "unsafe_database")
            try:
                candidate.unlink()
            except FileNotFoundError:
                pass
    return {
        "status": "ready", "database": str(path), **metadata,
        "source_count": len(documents), "section_count": section_count,
        "skipped": skipped, "disposable": True,
        "message": "Lexical candidate cache built. Fetch source passages before relying on a result.",
    }


def _open_database(root: Path, path: Path) -> tuple[sqlite3.Connection, dict]:
    if not path.exists():
        raise SearchError("Optional search database is missing. " + FALLBACK, "missing")
    _require_fts()
    connection = None
    try:
        connection = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
        connection.execute("PRAGMA query_only=ON")
        if connection.execute("PRAGMA quick_check").fetchall() != [("ok",)]:
            raise SearchError("Optional search database is corrupt. " + FALLBACK, "corrupt")
        metadata = dict(connection.execute("SELECT key, value FROM metadata"))
        required = {"schema_version", "root_path", "root_id", "generation", "source_set_sha256", "source_count"}
        if not required <= metadata.keys() or metadata["schema_version"] != SCHEMA_VERSION:
            raise SearchError("Optional database schema is unsupported. " + FALLBACK, "incompatible")
        if metadata["root_id"] != read_source.root_identity(root):
            raise SearchError("Database belongs to another campaign root. " + FALLBACK, "wrong_root")
        connection.execute("SELECT rowid FROM passages_fts WHERE passages_fts MATCH 'integrity_probe' LIMIT 1").fetchall()
        stored = dict(connection.execute("SELECT path, sha256 FROM sources"))
        if _set_hash(stored) != metadata["source_set_sha256"] or str(len(stored)) != metadata["source_count"]:
            raise SearchError("Optional database source inventory is corrupt. " + FALLBACK, "corrupt")
        if connection.execute("""SELECT 1 FROM sections WHERE start_line < 1 OR
            (end_line < start_line AND NOT (start_line = 1 AND end_line = 0)) LIMIT 1""").fetchone():
            raise SearchError("Optional database contains invalid passage coordinates. " + FALLBACK, "corrupt")
        return connection, metadata
    except BaseException:
        if connection is not None:
            connection.close()
        raise


def _freshness(root: Path, connection: sqlite3.Connection, metadata: dict, scope: str = "all") -> dict:
    stored = dict(connection.execute("SELECT path, sha256 FROM sources WHERE ? = 'all' OR scope = ?", (scope, scope)))
    try:
        documents, skipped = collect_sources(root, scope)
    except (SearchError, read_source.SourceError, OSError) as exc:
        return {"status": "unknown", "fresh": False, "freshness_scope": scope,
                "message": f"Source freshness in scope {scope!r} could not be verified: {exc}. " + FALLBACK}
    actual = _source_set(documents)
    added = sorted(actual.keys() - stored.keys())
    deleted = sorted(stored.keys() - actual.keys())
    changed = sorted(path for path in actual.keys() & stored.keys() if actual[path] != stored[path])
    fresh = not (added or deleted or changed)
    return {
        "status": "ready" if fresh else "stale", "fresh": fresh, "freshness_scope": scope,
        "source_count": len(actual), "indexed_source_count": len(stored),
        "added": added, "deleted": deleted, "changed": changed, "skipped": skipped,
        "source_set_sha256": _set_hash(actual),
        "message": (f"Source hashes and source set in scope {scope!r} match this cache generation."
                    if fresh else f"Cache is stale in scope {scope!r}; candidates may omit or refer to changed sources. " + FALLBACK),
    }


def _unavailable(exc: Exception) -> dict:
    code = exc.code if isinstance(exc, (SearchError, read_source.SourceError)) else "corrupt" if isinstance(exc, sqlite3.Error) else "operation_failed"
    return {"status": code, "fresh": False, "message": str(exc) + (" " + FALLBACK if FALLBACK not in str(exc) else "")}


def index_status(root: str | Path, db: str | Path) -> dict:
    connection = None
    try:
        root = _root(root)
        path = _db_path(root, db)
        connection, metadata = _open_database(root, path)
        return {**metadata, "database": str(path), "disposable": True, **_freshness(root, connection, metadata)}
    except (SearchError, read_source.SourceError, sqlite3.Error, OSError) as exc:
        return _unavailable(exc)
    finally:
        if connection is not None:
            connection.close()


def _literal_query(query: str) -> str:
    if not isinstance(query, str) or len(query) > 2000:
        raise SearchError("Query must be text of at most 2000 characters.", "invalid_query")
    terms = re.findall(r"[^\W_]+", query, flags=re.UNICODE)
    if not terms or len(terms) > 64:
        raise SearchError("Query needs 1 to 64 lexical terms.", "invalid_query")
    # Treat query syntax as literal terms: no SQL, FTS operators or instructions.
    return " AND ".join('"' + term + '"' for term in terms)


def search(root: str | Path, db: str | Path, query: str,
           scope: str = "current", limit: int = 10) -> dict:
    _scope(scope)
    match = _literal_query(query)
    if type(limit) is not int or not 1 <= limit <= 100:
        raise SearchError("Limit must be between 1 and 100.", "invalid_query")
    connection = None
    try:
        root = _root(root)
        path = _db_path(root, db)
        connection, metadata = _open_database(root, path)
        freshness = _freshness(root, connection, metadata, scope)
        eligible, _ = _walk_sources(root, scope)
        eligible = set(eligible)
        rows = connection.execute("""
            SELECT sections.id, sections.path, sections.section_id, sections.heading,
                   sections.heading_path, sections.start_line, sections.end_line,
                   sources.sha256, sources.scope, sources.source_class, sources.identities,
                   bm25(passages_fts, 8.0, 5.0, 2.0, 1.0) AS rank
            FROM passages_fts JOIN sections ON sections.id = passages_fts.rowid
            JOIN sources ON sources.path = sections.path
            WHERE passages_fts MATCH ? AND (? = 'all' OR sources.scope = ?)
            ORDER BY rank, sections.path, sections.start_line
        """, (match, scope, scope))
        candidates = []
        for row in rows:
            (row_id, relative, section_id, heading, heading_path, start, end,
             digest, source_scope, source_class, identities, rank) = row
            # Enforce the path allowlist again; a cache cannot grant wider access.
            if classify_source(relative) != (source_scope, source_class):
                raise SearchError("Database contains an out-of-policy source route.", "corrupt")
            if relative not in eligible:
                continue
            candidates.append({
                "candidate_id": row_id, "root_id": metadata["root_id"],
                "generation": metadata["generation"], "path": relative,
                "section_id": section_id, "heading": heading,
                "heading_path": json.loads(heading_path), "start_line": start, "end_line": end,
                "source_sha256": digest, "scope": source_scope, "source_class": source_class,
                "identities": json.loads(identities), "rank": rank,
                "cache_stale": not freshness["fresh"], "candidate_only": True,
            })
            if len(candidates) >= limit:
                break
        return {
            **freshness, "root_id": metadata["root_id"], "generation": metadata["generation"],
            "query": query, "scope": scope, "candidates": candidates,
            "candidate_count": len(candidates), "ranking_is_authority": False,
            "retrieval_notice": (
                "Fetch candidates through the shared source reader before relying on their contents. "
                "Ranking does not establish authority; route hints are not evidence bodies. "
                "No lexical match does not establish that a fact is absent."
            ),
        }
    except (SearchError, read_source.SourceError, sqlite3.Error, OSError) as exc:
        return {**_unavailable(exc), "query": query, "scope": scope, "candidates": [], "candidate_count": 0}
    finally:
        if connection is not None:
            connection.close()


def fetch_candidate(root: str | Path, db: str | Path, candidate: dict,
                    scope: str = "current", max_chars: int | None = None) -> dict:
    """Fetch only a verified candidate within the caller's explicit scope."""
    _scope(scope)
    if not isinstance(candidate, dict):
        raise SearchError("Expected a candidate object from search.", "invalid_candidate")
    root = _root(root)
    path = _db_path(root, db)
    connection, metadata = _open_database(root, path)
    try:
        if candidate.get("root_id") != metadata["root_id"] or candidate.get("generation") != metadata["generation"]:
            raise SearchError("Candidate belongs to another root or cache generation; search again.", "stale_candidate")
        if type(candidate.get("candidate_id")) is not int:
            raise SearchError("Candidate ID must be an integer.", "invalid_candidate")
        row = connection.execute("""SELECT sections.path, sections.section_id, sections.heading,
            sections.heading_path, sections.start_line, sections.end_line,
            sources.sha256, sources.scope, sources.source_class
            FROM sections JOIN sources ON sources.path = sections.path WHERE sections.id = ?
        """, (candidate["candidate_id"],)).fetchone()
        if row is None:
            raise SearchError("Candidate no longer exists; search again.", "stale_candidate")
        relative, section_id, heading, heading_path, start, end, digest, source_scope, source_class = row
        expected = {"path": relative, "section_id": section_id, "heading": heading,
                    "heading_path": json.loads(heading_path), "start_line": start, "end_line": end,
                    "source_sha256": digest, "scope": source_scope, "source_class": source_class}
        if any(candidate.get(key) != value for key, value in expected.items()):
            raise SearchError("Candidate metadata was altered; search again.", "invalid_candidate")
        if classify_source(relative) != (source_scope, source_class):
            raise SearchError("Candidate path is outside the supported source policy.", "scope_denied")
        if scope != "all" and source_scope != scope:
            raise SearchError(f"Candidate scope {source_scope!r} is not selected scope {scope!r}.", "scope_denied")
        eligible, _ = _walk_sources(root, scope)
        if relative not in eligible:
            raise SearchError("Candidate is no longer an eligible source in this root and scope.", "scope_denied")
        freshness = _freshness(root, connection, metadata, scope)
        document = read_source.load_document(root, relative, expected_sha256=digest)
        if document["root_id"] != metadata["root_id"]:
            raise SearchError("Source root identity changed.", "wrong_root")
        # Cache coordinates are untrusted. Re-derive every selector, including
        # synthetic preamble and plain-text spans, from the verified source.
        keys = ("section_id", "heading", "heading_path", "start_line", "end_line")
        if not any(all(section.get(key) == expected[key] for key in keys)
                   for section in _document_sections(document)):
            raise SearchError("Cached passage coordinates do not match the source.", "corrupt")
        if section_id is not None:
            passage = read_source.select_passage(document, section_id=section_id, max_chars=max_chars)
        elif end >= start:
            passage = read_source.select_passage(document, start_line=start, end_line=end, max_chars=max_chars)
        else:
            passage = read_source.select_passage(document, max_chars=max_chars)
        return {"status": "verified", "generation": metadata["generation"],
                "scope": source_scope, "source_class": source_class,
                "freshness_scope": scope, "cache_freshness": freshness,
                "candidate_only": False, "source_revision_verified": True, "passage": passage}
    finally:
        connection.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("build", "status", "search", "fetch"):
        command = commands.add_parser(name)
        command.add_argument("--root", required=True, type=Path, help="One selected campaign root")
        command.add_argument("--db", required=True, type=Path, help="Disposable SQLite file outside root; parent must exist")
        if name in {"search", "fetch"}:
            command.add_argument("--scope", choices=SCOPES, default="current")
        if name == "search":
            command.add_argument("query", help="Literal lexical terms (all terms must match)")
            command.add_argument("--limit", type=int, default=10)
        if name == "fetch":
            command.add_argument("--candidate", required=True, help="JSON candidate file, or - for standard input")
            command.add_argument("--max-chars", type=int)
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            result = build_index(args.root, args.db)
        elif args.command == "status":
            result = index_status(args.root, args.db)
        elif args.command == "search":
            result = search(args.root, args.db, args.query, args.scope, args.limit)
        else:
            if args.candidate == "-":
                candidate = json.load(sys.stdin)
            else:
                with Path(args.candidate).open(encoding="utf-8-sig") as stream:
                    candidate = json.load(stream)
            result = fetch_candidate(args.root, args.db, candidate, args.scope, args.max_chars)
    except (SearchError, read_source.SourceError, sqlite3.Error, OSError, ValueError) as exc:
        result = _unavailable(exc)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result["status"] in {"ready", "verified"} else 1 if result["status"] == "stale" else 2


if __name__ == "__main__":
    raise SystemExit(main())
