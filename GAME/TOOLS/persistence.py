#!/usr/bin/env python3
"""Experimental foreground incremental persistence. Standard library, no model calls.

Prepared responses are durable proposals, never committed fiction. Confirm requires
an observed completed response. Checks prove storage consistency, not GM semantics.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import uuid

SCHEMA = 'rpg-journal-v1'
LOG_SCHEMA = 'rpg-journal-v2'
HEAD = 'INSTANCE/JOURNAL/HEAD.json'
INTENT = 'INSTANCE/JOURNAL/PREPARE_INTENT.json'
ACTIVE = 'RECOVERY/ACTIVE.md'
CURRENT = 'INSTANCE/CURRENT_SAVE.md'
CONTRACT = 'INSTANCE/CAMPAIGN_CONTRACT.md'
IMMUTABLE = ('engine', 'module', 'pc_record', 'campaign_id', 'save_id', 'save_rev',
             'save_parent', 'commit_kind', 'archive_ref', 'evidence_through',
             'journal_through', 'journal_archive_through', 'journal_stream',
             'journal_head', 'journal_head_sha256', 'journal_archive_head', 'journal_archive_sha256')
IMMUTABLE += ('journal_head_receipt_sha256', 'journal_archive_receipt_sha256')
IMMUTABLE += ('play_log_through', 'play_log_prefix_sha256',
              'play_log_archive_through', 'play_log_archive_prefix_sha256')


class PersistenceError(Exception):
    pass


def _require(value, message):
    if not value:
        raise PersistenceError(message)


def _log_mode(head):
    return head.get('schema') == LOG_SCHEMA and head.get('recording') == 'write-only-log'


def _play_log_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location('rpg_play_log_admin', Path(__file__).with_name('play_log.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _log_snapshot(root):
    try:
        return _play_log_module().snapshot(root)
    except (OSError, ValueError) as exc:
        raise PersistenceError('Session log snapshot failed: ' + str(exc)) from exc


def _hash(data):
    return hashlib.sha256(data).hexdigest()


def _json(data):
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def _id(value):
    _require(isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,159}', value)
             and '..' not in value, 'Invalid portable identifier')
    return value


def _path(root, relative):
    _require(isinstance(relative, str) and relative and '\\' not in relative,
             'Use nonempty campaign-relative POSIX paths')
    parts = relative.split('/')
    for part in parts:
        _require(part not in ('', '.', '..') and not any(c in part for c in ':*?"<>|') and not part.endswith((' ', '.'))
                 and not any(ord(c) < 32 for c in part), 'Unsafe path')
        _require(not re.fullmatch(r'(CON|PRN|AUX|NUL|COM[0-9¹²³]|LPT[0-9¹²³])',
                                 part.split('.')[0], re.I), 'Reserved device path')
    root = Path(os.path.abspath(root))
    result = root.joinpath(*parts)
    check = root
    for part in parts:
        check = check / part
        if check.exists() or check.is_symlink():
            info = check.lstat()
            _require(not stat.S_ISLNK(info.st_mode) and not
                     (getattr(info, 'st_file_attributes', 0) & 0x400), 'Link/reparse path refused')
            # Windows realpath recovers actual casing and expands 8.3 aliases without
            # enumerating an ever-growing batch directory on every current read.
            if os.name == 'nt':
                _require(check.resolve(strict=True).name == part, 'Noncanonical case or path alias')
    for p in [root, *result.parents, result]:
        if p.exists() or p.is_symlink():
            info = p.lstat()
            _require(not stat.S_ISLNK(info.st_mode) and
                     not (getattr(info, 'st_file_attributes', 0) & 0x400), 'Link/reparse path refused')
    _require(result.is_relative_to(root), 'Path escapes campaign')
    return result


def _bytes(root, relative):
    p = _path(root, relative)
    return p.read_bytes() if p.is_file() else None


def _load_json(root, relative):
    data = _bytes(root, relative)
    _require(data is not None, 'Missing ' + relative)
    try:
        return json.loads(data)
    except (ValueError, UnicodeError) as exc:
        raise PersistenceError('Invalid JSON: ' + relative) from exc


def _atomic_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp-' + uuid.uuid4().hex)
    try:
        with temporary.open('xb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        _require(path.read_bytes() == data, 'Write readback failed: ' + str(path))
    finally:
        if temporary.exists():
            temporary.unlink()


def _publish_write(path, data):
    _atomic_write(path, data)


@contextlib.contextmanager
def _lock(root):
    # OS-held lock is released on process exit; the small lock file is retained.
    path = _path(root, 'RECOVERY/persistence.lock')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as stream:
        if path.stat().st_size == 0:
            stream.write(b'0')
            stream.flush()
        stream.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise PersistenceError('Another persistence writer is active') from exc
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == 'nt':
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def _idle(root):
    _require(_bytes(root, ACTIVE) is None, 'Recovery active; finish or restore before continuing')
    _require(_bytes(root, 'HANDOVER/ACTIVE.md') is None, 'Handover active; source is frozen')


def _fields(data):
    text = data.decode('utf-8') if isinstance(data, bytes) else data
    values = {}
    for key, value in re.findall(r'^\|\s*([a-z][a-z0-9_]+)\s*\|\s*([^|\r\n]+)\s*\|\s*$', text, re.M):
        _require(key not in values, 'Duplicate metadata field: ' + key)
        values[key] = value.strip()
    return values


def _set_field(data, key, value):
    text = data.decode('utf-8')
    newline = '\r\n' if '\r\n' in text else '\n'
    pattern = rf'(?m)^\|\s*{re.escape(key)}\s*\|[^\r\n]*'
    if re.search(pattern, text):
        text = re.sub(pattern, '| ' + key + ' | ' + str(value) + ' |', text)
    else:
        anchor = re.search(r'(?m)^\|\s*save_id\s*\|[^\r\n]*', text)
        _require(anchor, 'Missing save identity table')
        text = text[:anchor.end()] + newline + '| ' + key + ' | ' + str(value) + ' |' + text[anchor.end():]
    return text.encode('utf-8')


def _set_section(data, heading, body):
    text = data.decode('utf-8')
    newline = '\r\n' if '\r\n' in text else '\n'
    matches = list(re.finditer(r'(?m)^## ' + re.escape(heading) + r'\r?$', text))
    _require(len(matches) <= 1, 'Duplicate administrative section')
    new = '## ' + heading + newline + newline + body.replace('\n', newline) + newline + newline
    if not matches:
        return (text.rstrip('\r\n') + newline + newline + new).encode('utf-8')
    start = matches[0].start()
    following = re.search(r'(?m)^## ', text[matches[0].end():])
    end = matches[0].end() + following.start() if following else len(text)
    return (text[:start] + new + text[end:]).encode('utf-8')


def _load(root):
    _idle(root)
    _require(_bytes(root, INTENT) is None, 'Interrupted preparation; run recover-prepare using retained intent')
    head = _load_json(root, HEAD)
    fields = _fields(_bytes(root, CURRENT) or b'')
    _require(head.get('schema') in (SCHEMA, LOG_SCHEMA), 'Unsupported journal format')
    _require(head.get('schema') != LOG_SCHEMA or _log_mode(head), 'Unsupported v2 recording mode')
    _require(_hash(_bytes(root, CONTRACT) or b'') == head.get('contract_sha256'),
             'Accepted agreement changed; consolidate before maintenance and explicitly rebind afterward')
    _require(fields.get('campaign_id') == head.get('campaign_id'), 'Foreign campaign journal')
    _require(fields.get('save_id') == head.get('base_save_id'), 'Checkpoint changed outside journal publisher')
    _require(fields.get('journal_stream', head['stream_id']) == head['stream_id'], 'Foreign journal stream')
    for key in ('journal_through', 'journal_archive_through'):
        value = fields.get(key, '0')
        _require(re.fullmatch(r'0|[1-9][0-9]*', value), 'Invalid journal boundary')
        _require(int(value) <= head['seq'], 'Journal boundary is ahead of committed head')
    _require(int(fields.get('journal_archive_through', '0')) <= int(fields.get('journal_through', '0')),
             'Archive journal boundary exceeds consolidation')
    if _log_mode(head):
        _require('incremental recording: write-only-log' in (_bytes(root, CONTRACT) or b'').decode('utf-8').lower(),
                 'Accepted write-only recording policy required')
        _require(int(fields.get('journal_through', '0')) == head['seq'] and head['pending'] is None,
                 'Legacy pending state must be confirmed and consolidated before log-mode adoption')
    return head, fields


def _batch(root, transaction_id):
    return _load_json(root, 'INSTANCE/JOURNAL/batches/' + _id(transaction_id) + '.json')


def _chain(root, head, stop_seq=0, anchor=None):
    chain = []
    current, digest, expected = head['head'], head['head_sha256'], head['seq']
    receipt_digest = head.get('head_receipt_sha256')
    while current is not None and expected > stop_seq:
        path = 'INSTANCE/JOURNAL/batches/' + _id(current) + '.json'
        data = _bytes(root, path)
        _require(data is not None and _hash(data) == digest, 'Missing or altered journal batch')
        batch = json.loads(data)
        _require(batch['seq'] == expected and batch['campaign_id'] == head['campaign_id']
                 and batch['stream_id'] == head['stream_id'], 'Broken journal chain')
        receipt_data = _bytes(root, 'INSTANCE/JOURNAL/receipts/' + current + '.json')
        _require(receipt_data is not None and _hash(receipt_data) == receipt_digest,
                 'Committed delivery receipt missing or altered')
        receipt = json.loads(receipt_data)
        _verify_receipt(batch, receipt)
        chain.append(batch)
        current, digest = batch['parent'], batch['parent_sha256']
        receipt_digest = batch.get('parent_receipt_sha256')
        expected -= 1
        _require(expected >= 0, 'Cyclic journal chain')
    _require(expected == stop_seq, 'Incomplete journal chain')
    if anchor is not None:
        _require((current, digest, receipt_digest) == anchor, 'Journal does not descend from recorded consolidation boundary')
    elif stop_seq == 0:
        _require(current is None and digest is None and receipt_digest is None, 'Broken journal origin')
    return list(reversed(chain))


def _allowed(relative):
    return (relative in (CURRENT, 'INSTANCE/NOW.md', 'INSTANCE/KNOWN.md',
                         'INSTANCE/CAST_STATUS.md', 'INSTANCE/PREP.md') or
            any(relative.startswith(p) and relative.endswith('.md') for p in
                ('INSTANCE/CHAR/', 'INSTANCE/PEOPLE/', 'INSTANCE/NOW/', 'INSTANCE/KNOWN/')))


def _effective(root, head, fields):
    overlay = {}
    through = int(fields.get('journal_through', '0'))
    anchor = ((fields.get('journal_head'), fields.get('journal_head_sha256'), fields.get('journal_head_receipt_sha256'))
              if through else (None, None, None))
    for batch in _chain(root, head, through, anchor):
        for change in batch['changes']:
            path = change['path']
            _require(not any(k.casefold() == path.casefold() and k != path for k in overlay),
                     'Conflicting pending path aliases')
            before = overlay.get(path, _bytes(root, path))
            _require((_hash(before) if before is not None else None) == change['before_sha256'],
                     'Current record changed outside committed chain: ' + path)
            after = change['content'].encode('utf-8')
            _require(_hash(after) == change['after_sha256'], 'Altered resulting record')
            overlay[path] = after
    return overlay


def initialize(root, conversation_id, source_floor=None):
    with _lock(root):
        _idle(root)
        _require(_bytes(root, HEAD) is None, 'Journal already initialized')
        journal_dir = _path(root, 'INSTANCE/JOURNAL')
        _require(not journal_dir.exists() or not any(journal_dir.iterdir()),
                 'Existing journal artifacts require recovery; refuse a fresh empty stream')
        fields = _fields(_bytes(root, CURRENT) or b'')
        _require(fields.get('campaign_id') not in (None, 'none') and fields.get('save_id') not in (None, 'none'),
                 'A bound saved campaign is required')
        _require(fields.get('commit_kind') == 'bind' or
                 (fields.get('commit_kind') == 'close' and fields.get('evidence_through') == fields['save_id']),
                 'Adopt at initial bind or completed full SAVE so no earlier unarchived span is skipped')
        _require(fields.get('journal_stream') is None and fields.get('journal_through', '0') == '0',
                 'Existing journal epoch requires an explicit migration; cannot reset history by init')
        contract = (_bytes(root, CONTRACT) or b'').decode('utf-8')
        log_mode = 'incremental recording: write-only-log' in contract.lower()
        _require(log_mode or 'incremental persistence: enabled' in contract.lower(), 'Accepted incremental policy required')
        _require(not log_mode or source_floor is not None or fields.get('commit_kind') == 'bind',
                 'Existing-campaign log adoption needs its actual completed source floor')
        _id(conversation_id)
        mode = ('operator-confirmation' if 'incremental delivery observer: operator' in contract.lower()
                else 'foreground-confirmation')
        if source_floor is not None:
            _verify_host_receipt(source_floor)
            _require(source_floor['conversation_id'] == conversation_id, 'Source floor belongs to another conversation')
        head = {'schema': LOG_SCHEMA if log_mode else SCHEMA, 'campaign_id': fields['campaign_id'],
                'stream_id': uuid.uuid4().hex, 'base_save_id': fields['save_id'],
                'conversation_id': conversation_id, 'mode': mode, 'source_floor': source_floor,
                'contract_sha256': _hash(_bytes(root, CONTRACT)),
                'head': None, 'head_sha256': None, 'head_receipt_sha256': None,
                'seq': 0, 'pending': None, 'pending_sha256': None,
                'published_save_ids': [fields['save_id']]}
        if log_mode:
            head.update(recording='write-only-log', mode='write-only-log', public_source_floor=source_floor)
            if source_floor is None:
                head['public_source_origin'] = 'conversation-start'
        _atomic_write(_path(root, HEAD), _json(head))
        return {'status': 'initialized', 'mode': head['mode'], 'campaign_id': head['campaign_id']}


def _status(root):
    head, fields = _load(root)
    overlay = _effective(root, head, fields)
    pending = None
    if head['pending']:
        batch = _batch(root, head['pending'])
        _require(_hash(_json(batch)) == head['pending_sha256'], 'Prepared batch was altered')
        pending = {'transaction_id': head['pending'], 'response_sha256': _hash(batch['response'].encode('utf-8')),
                   'conversation_id': batch['conversation_id'], 'state': 'prepared-not-committed'}
    result = {'status': 'pending-delivery' if pending else 'ready', 'head': head['head'],
            'committed_seq': head['seq'], 'consolidated_through': int(fields.get('journal_through', '0')),
            'archived_through': int(fields.get('journal_archive_through', '0')),
            'pending': pending, 'changed_paths': sorted(overlay), 'mode': head['mode']}
    if _log_mode(head):
        snapshot = _log_snapshot(root)
        result.update(recording='write-only-log', uncompiled_note_count=snapshot['note_count'],
                      compilation_required=bool(snapshot['note_count']),
                      log_snapshot={k: snapshot[k] for k in ('after', 'through', 'prefix_sha256')},
                      view='ADMIN status; canonical records are the compiled baseline, with subsequent session-log additions')
    return result


def status(root):
    with _lock(root):
        return _status(root)


def _read_current(root, path):
    _require(_allowed(path), 'Current reader accepts current owner paths only')
    head, fields = _load(root)
    overlay = _effective(root, head, fields)
    _require(not any(k.casefold() == path.casefold() and k != path for k in overlay),
             'Noncanonical pending path alias')
    data = overlay.get(path, _bytes(root, path))
    _require(data is not None, 'Missing effective current record: ' + path)
    result = {'path': path, 'content': data.decode('utf-8'), 'sha256': _hash(data),
            'consolidated_through': int(fields.get('journal_through', '0')), 'committed_seq': head['seq'],
            'view': 'effective-current; not original historical source'}
    if _log_mode(head):
        snapshot = _log_snapshot(root)
        result.update(view='compiled-record baseline plus subsequent session-log additions; Python has not interpreted the notes',
                      uncompiled_log=snapshot['entries'], compilation_required=bool(snapshot['note_count']),
                      log_snapshot={k: snapshot[k] for k in ('after', 'through', 'prefix_sha256')})
    return result


def read_current(root, path):
    with _lock(root):
        return _read_current(root, path)


def _section_span(text, heading):
    _require(isinstance(heading, str) and heading and '\n' not in heading and '\r' not in heading,
             'Section must name one existing Markdown heading')
    matches = list(re.finditer(r'(?m)^(#{1,6}) ' + re.escape(heading) + r'[ \t]*\r?$', text))
    _require(len(matches) == 1, 'Section heading must exist exactly once')
    match = matches[0]
    start = match.end() + (1 if text[match.end():].startswith('\n') else 0)
    following = re.search(r'(?m)^#{1,' + str(len(match.group(1))) + r'} ', text[start:])
    return start, start + following.start() if following else len(text)


def _apply_edits(text, edits):
    """Small selectors are guarded by the owner's required preimage hash."""
    _require(isinstance(edits, list), 'Edits must be a list')
    for edit in edits:
        _require(isinstance(edit, dict), 'Edit must be an object')
        keys = set(edit)
        if keys == {'before', 'after'}:
            old, new = edit['before'], edit['after']
            _require(isinstance(old, str) and old and isinstance(new, str) and text.count(old) == 1,
                     'Edit must identify one exact nonempty source span')
            text = text.replace(old, new, 1)
        elif keys == {'field', 'after'}:
            field, after = edit['field'], edit['after']
            _require(isinstance(field, str) and re.fullmatch(r'[a-z][a-z0-9_]+', field) and
                     isinstance(after, str) and not any(c in after for c in '\r\n|'),
                     'Field edit requires one safe metadata value')
            pattern = (r'(?m)^(\|[ \t]*' + re.escape(field) +
                       r'[ \t]*\|[ \t]*)([^|\r\n]*?)([ \t]*\|[ \t]*)(?=\r?$)')
            matches = list(re.finditer(pattern, text))
            _require(len(matches) == 1, 'Metadata field must exist exactly once')
            match = matches[0]
            text = text[:match.start(2)] + after + text[match.end(2):]
        elif keys in ({'line_prefix', 'after'}, {'section', 'line_prefix', 'after'}):
            prefix, after = edit['line_prefix'], edit['after']
            _require(isinstance(prefix, str) and prefix and isinstance(after, str) and
                     not any(c in prefix + after for c in '\r\n'), 'Line edit requires a nonempty single-line prefix and value')
            start, end = _section_span(text, edit['section']) if 'section' in edit else (0, len(text))
            matches = list(re.finditer(r'(?m)^' + re.escape(prefix) + r'[^\r\n]*', text[start:end]))
            _require(len(matches) == 1, 'Line prefix must exist exactly once in its scope')
            match = matches[0]
            text = text[:start + match.start()] + prefix + after + text[start + match.end():]
        elif keys == {'section', 'append'}:
            appended = edit['append']
            _require(isinstance(appended, str) and appended.strip(), 'Section append requires established content')
            start, end = _section_span(text, edit['section'])
            nested = re.search(r'(?m)^#{1,6} ', text[start:end])
            if nested:
                end = start + nested.start()
            newline = '\r\n' if '\r\n' in text else '\n'
            body = text[start:end].rstrip('\r\n') + newline + appended + newline + newline
            text = text[:start] + body + text[end:]
        else:
            raise PersistenceError('Unknown or mixed edit selectors')
    return text


def prepare(root, request):
    with _lock(root):
        head, fields = _load(root)
        _require(not _log_mode(head), 'Write-only PLAY uses play_log append; per-exchange owner patches are disabled')
        transaction_id = _id(request['transaction_id'])
        digest = _hash(_json(request))
        existing = _bytes(root, 'INSTANCE/JOURNAL/batches/' + transaction_id + '.json')
        if existing is not None:
            batch = json.loads(existing)
            _require(batch['request_sha256'] == digest, 'Transaction ID reused with different content')
            _require(head['pending'] == transaction_id or any(b['transaction_id'] == transaction_id for b in _chain(root, head)),
                     'Orphaned prepared batch; inspect before retry')
            return {'status': 'already-prepared-or-committed', 'transaction_id': transaction_id,
                    'resulting_hashes': {c['path']: c['after_sha256'] for c in batch['changes']}}
        _require(head['pending'] is None, 'Resolve the prepared response before preparing another')
        _require(request.get('conversation_id') == head['conversation_id'], 'Wrong conversation writer')
        _require(request.get('expected_head') == head['head'], 'Stale expected journal head')
        _require(isinstance(request.get('response'), str) and request['response'], 'Exact planned response required')
        _require(isinstance(request.get('user_text'), str), 'Actual user text required')
        _require(isinstance(request.get('changes'), list), 'Changes must be a list; empty is allowed')
        overlay = _effective(root, head, fields)
        changes, seen = [], set()
        for change in request['changes']:
            path = change['path']
            _path(root, path)
            _require(_allowed(path), 'Owner is outside incremental write scope: ' + path)
            _require(path.casefold() not in seen, 'Duplicate changed path')
            _require(not any(k.casefold() == path.casefold() and k != path for k in overlay),
                     'Noncanonical pending path alias')
            seen.add(path.casefold())
            before = overlay.get(path, _bytes(root, path))
            before_hash = _hash(before) if before is not None else None
            _require(change.get('expected_sha256') == before_hash, 'Stale expected record: ' + path)
            if before is None:
                _require(isinstance(change.get('content'), str) and 'edits' not in change,
                         'A new record needs its complete established content')
                after = change['content'].encode('utf-8')
            else:
                _require('content' not in change and isinstance(change.get('edits'), list),
                         'Existing records use exact targeted edits')
                text = _apply_edits(before.decode('utf-8'), change['edits'])
                after = text.encode('utf-8')
            if path == CURRENT:
                old_fields, new_fields = _fields(before), _fields(after)
                _require(all(old_fields.get(k) == new_fields.get(k) for k in IMMUTABLE),
                         'Exchange cannot change save identity or publication boundaries')
            if before != after:
                changes.append({'path': path, 'before_sha256': before_hash, 'after_sha256': _hash(after),
                                'content': after.decode('utf-8')})
        batch = {'schema': SCHEMA, 'transaction_id': transaction_id, 'request_sha256': digest,
                 'campaign_id': head['campaign_id'], 'stream_id': head['stream_id'],
                 'conversation_id': request['conversation_id'], 'seq': head['seq'] + 1,
                 'parent': head['head'], 'parent_sha256': head['head_sha256'],
                 'parent_receipt_sha256': head['head_receipt_sha256'],
                 'response': request['response'], 'user_text': request['user_text'],
                 'changes': changes, 'source_notes': request.get('source_notes', []),
                 'actual_results': request.get('actual_results', [])}
        old_head = dict(head)
        head['pending'] = transaction_id
        head['pending_sha256'] = _hash(_json(batch))
        # A complete intent is durable before the first batch/head mutation.
        intent = {'schema': 'rpg-prepare-intent-v1', 'prior_head': old_head, 'target_head': head, 'batch': batch}
        _atomic_write(_path(root, INTENT), _json(intent))
        _recover_prepare_unlocked(root)
        return {'status': 'prepared-not-committed', 'transaction_id': transaction_id,
                'response_sha256': _hash(batch['response'].encode('utf-8')), 'changed_paths': [c['path'] for c in changes],
                'resulting_hashes': {c['path']: c['after_sha256'] for c in changes}}


def _same_user_input(observed, prepared):
    # Codex commonly appends a terminal LF to otherwise identical public input.
    # This is admission comparison only; original receipt bytes remain evidence.
    return (isinstance(observed, str) and isinstance(prepared, str) and
            observed.rstrip('\r\n') == prepared.rstrip('\r\n'))


def _verify_receipt(batch, receipt):
    _require(receipt.get('schema') == 'rpg-delivery-v1' and receipt.get('complete') is True,
             'Observed completed delivery receipt required')
    _require(receipt.get('observer') in ('codex-rollout', 'operator'), 'Unsupported delivery observer')
    _require(receipt.get('transaction_id') == batch['transaction_id'] and
             receipt.get('conversation_id') == batch['conversation_id'], 'Receipt belongs to another transaction/conversation')
    _require(receipt.get('assistant_text') == batch['response'], 'Delivered response differs from prepared response')
    _require(isinstance(receipt.get('source_ref'), dict) and receipt['source_ref'], 'Actual delivery source required')
    if 'user_text' in receipt:
        _require(_same_user_input(receipt['user_text'], batch['user_text']), 'User source differs from prepared exchange')


def _verify_host_receipt(receipt):
    import importlib.util
    _require(receipt.get('observer') == 'codex-rollout', 'Actual host receipt required')
    spec = importlib.util.spec_from_file_location('rpg_codex_delivery', Path(__file__).with_name('codex_exchange.py'))
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    try:
        verifier.verify_receipt(receipt)
    except (ValueError, OSError) as exc:
        raise PersistenceError('Completed source verification failed: ' + str(exc)) from exc


def confirm(root, receipt):
    with _lock(root):
        head, fields = _load(root)
        _require(not _log_mode(head), 'Write-only PLAY has no per-exchange delivery confirmation')
        transaction_id = _id(receipt['transaction_id'])
        batch = _batch(root, transaction_id)
        _verify_receipt(batch, receipt)
        # Already recorded receipts stay portable; only new admission reopens host source.
        receipt_path = 'INSTANCE/JOURNAL/receipts/' + transaction_id + '.json'
        if batch['seq'] <= head['seq'] and any(b['transaction_id'] == transaction_id for b in _chain(root, head)):
            return {'status': 'already-committed', 'transaction_id': transaction_id}
        if receipt['observer'] == 'codex-rollout':
            _verify_host_receipt(receipt)
            users = receipt.get('user_messages', [])
            _require(users and _same_user_input('\n\n'.join(m['text'] for m in users), batch['user_text']),
                     'Prepared user text does not match observed source; reconcile pending exchange')
            floor = head.get('source_floor')
            if floor:
                if receipt['source_ref']['path'] == floor['source_ref']['path']:
                    _require(receipt['source_ref']['end_line'] > floor['source_ref']['end_line'],
                             'Source predates the adopted saved boundary')
                else:
                    from datetime import datetime
                    current_time, floor_time = receipt['source_ref'].get('completed_at'), floor['source_ref'].get('completed_at')
                    _require(current_time and floor_time, 'New rollout requires an observed completion time or explicit rebind')
                    try:
                        newer = datetime.fromisoformat(current_time) > datetime.fromisoformat(floor_time)
                    except (ValueError, TypeError) as exc:
                        raise PersistenceError('Unknown rollout completion ordering') from exc
                    _require(newer, 'New rollout source predates adopted save')
        else:
            _require(head['mode'] == 'operator-confirmation',
                     'Operator attestation was not selected; actual completed host source is required')
        source_id = _hash(_json({'conversation_id': receipt['conversation_id'],
                                'source_ref': {k: v for k, v in receipt['source_ref'].items()
                                               if k in ('turn_id', 'message_id', 'kind')}}))
        _require(receipt['source_ref'].get('message_id'), 'Stable observed message identity required')
        source_path = 'INSTANCE/JOURNAL/deliveries/' + source_id + '.json'
        used_source = _bytes(root, source_path)
        _require(used_source is None or json.loads(used_source)['transaction_id'] == transaction_id,
                 'This completed response was already admitted under another transaction')
        _require(head['pending'] == transaction_id and batch['parent'] == head['head'], 'Prepared predecessor changed')
        _require(_hash(_json(batch)) == head['pending_sha256'], 'Prepared batch was altered')
        overlay = _effective(root, head, fields)
        for change in batch['changes']:
            data = overlay.get(change['path'], _bytes(root, change['path']))
            _require((_hash(data) if data is not None else None) == change['before_sha256'], 'Prepared preimage changed')
        _atomic_write(_path(root, receipt_path), _json(receipt))
        _atomic_write(_path(root, source_path), _json({'transaction_id': transaction_id, 'source_ref': receipt['source_ref']}))
        head.update(head=transaction_id, head_sha256=_hash(_json(batch)), head_receipt_sha256=_hash(_json(receipt)),
                    seq=batch['seq'], pending=None, pending_sha256=None)
        _atomic_write(_path(root, HEAD), _json(head))
        return {'status': 'committed', 'transaction_id': transaction_id, 'committed_seq': head['seq']}


def pending(root):
    with _lock(root):
        head, _fields_value = _load(root)
        _require(head['pending'], 'No prepared response')
        batch = _batch(root, head['pending'])
        _require(_hash(_json(batch)) == head['pending_sha256'], 'Prepared batch was altered')
        return batch


def _resume_view(root, compact, paths):
    """Assemble one coherent post-confirmation view; caller owns the writer lock."""
    head, fields = _load(root)
    _require(head['pending'] is None, 'Writer prepared another response while resuming; reconcile it first')
    overlay = _effective(root, head, fields)
    through = int(fields.get('journal_through', '0'))
    selected = list(dict.fromkeys(paths or []))
    for path in selected:
        _require(isinstance(path, str) and _allowed(path), 'Current reader accepts current owner paths only')
        _require(not any(k.casefold() == path.casefold() and k != path for k in overlay),
                 'Noncanonical pending path alias')
        _path(root, path)
    wanted = set(overlay) | {CURRENT} | set(selected)
    data = {}
    for path in sorted(wanted):
        value = overlay[path] if path in overlay else _bytes(root, path)
        _require(value is not None, 'Missing effective current record: ' + path)
        data[path] = value
    hashes = {path: _hash(value) for path, value in data.items()}
    result = {
        'journal': {'status': 'ready', 'head': head['head'], 'committed_seq': head['seq'],
                    'consolidated_through': through,
                    'archived_through': int(fields.get('journal_archive_through', '0')),
                    'pending': None, 'changed_paths': sorted(overlay), 'mode': head['mode']},
        'identity': {key: head[key] for key in
                     ('campaign_id', 'conversation_id', 'stream_id', 'base_save_id', 'head_sha256')},
        'effective_hashes': hashes,
    }

    def body(path):
        return {'path': path, 'content': data[path].decode('utf-8'), 'sha256': hashes[path],
                'consolidated_through': through, 'committed_seq': head['seq'],
                'view': 'effective-current; not original historical source'}

    if not compact:
        result['current'] = body(CURRENT)
    if selected:
        result['records'] = {path: body(path) for path in selected}
    return result


def resume(root, source=None, compact=False, paths=None):
    """Confirm prior delivery, then return one view; API defaults to the full current body.

Compact mode exposes identities and effective owner hashes only. Explicit paths
request bodies from that same locked snapshot, avoiding parallel reader collisions.
"""
    _require(paths is None or isinstance(paths, (list, tuple)), 'Requested paths must be a list')
    _require(all(isinstance(path, str) for path in (paths or [])), 'Requested paths must be strings')
    with _lock(root):
        head, _fields_value = _load(root)
        _require(not _log_mode(head), 'Write-only PLAY does not run resume; use ADMIN status/read only at a real load or save boundary')
        batch = _batch(root, head['pending']) if head['pending'] else None
        if batch is not None:
            _require(_hash(_json(batch)) == head['pending_sha256'], 'Prepared batch was altered')
    confirmed = None
    if batch is not None:
        import importlib.util
        spec = importlib.util.spec_from_file_location('rpg_codex_resume', Path(__file__).with_name('codex_exchange.py'))
        adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(adapter)
        try:
            receipt = adapter.capture(batch['conversation_id'], batch['response'], batch['transaction_id'],
                                      sources=[source] if source else None)
        except (ValueError, OSError) as exc:
            raise PersistenceError('Previous delivery remains pending: ' + str(exc)) from exc
        confirmed = confirm(root, receipt)
    with _lock(root):
        result = _resume_view(root, compact, paths)
    return {'confirmation': confirmed, **result}


def note(root, request):
    raise PersistenceError('No per-exchange note/prepare protocol: use play_log append for write-only recording')


def _recover_prepare_unlocked(root):
    _idle(root)
    intent = _load_json(root, INTENT)
    _require(intent.get('schema') == 'rpg-prepare-intent-v1', 'Unsupported preparation intent')
    head = _load_json(root, HEAD)
    _require(head in (intent['prior_head'], intent['target_head']), 'Preparation head changed; inspect retained intent')
    batch = intent['batch']
    path = 'INSTANCE/JOURNAL/batches/' + _id(batch['transaction_id']) + '.json'
    data = _json(batch)
    _require(_hash(data) == intent['target_head']['pending_sha256'], 'Corrupt preparation intent')
    existing = _bytes(root, path)
    _require(existing is None or existing == data, 'Unexpected prepared file; preserve and investigate')
    _atomic_write(_path(root, path), data)
    _atomic_write(_path(root, HEAD), _json(intent['target_head']))
    _path(root, INTENT).unlink()
    return {'status': 'prepared-not-committed', 'transaction_id': batch['transaction_id']}


def recover_prepare(root):
    with _lock(root):
        return _recover_prepare_unlocked(root)


def rebind(root, conversation_id, expected_base):
    """After authorized protected maintenance/transfer; never absorbs pending changes."""
    with _lock(root):
        source_limit = None
        _idle(root)
        _require(_bytes(root, INTENT) is None, 'Recover interrupted preparation before rebind')
        head = _load_json(root, HEAD)
        fields = _fields(_bytes(root, CURRENT) or b'')
        _require(head['pending'] is None and head['base_save_id'] == expected_base,
                 'Pending exchange or stale rebind request')
        _require(fields.get('campaign_id') == head['campaign_id'] and
                 int(fields.get('journal_through', '0')) == head['seq'],
                 'Consolidate the complete journal before maintenance or transfer')
        if head['seq']:
            _require(fields.get('journal_head') == head['head'] and
                     fields.get('journal_head_sha256') == head['head_sha256'] and
                     fields.get('journal_stream') == head['stream_id'], 'Maintenance lost journal boundaries')
        _id(conversation_id)
        contract = (_bytes(root, CONTRACT) or b'').decode('utf-8').lower()
        selected_log = 'incremental recording: write-only-log' in contract
        _require(selected_log == _log_mode(head), 'Recording-mode changes require explicit journal migration')
        _require(selected_log or 'incremental persistence: enabled' in contract,
                 'Enabled policy required; use ordinary mode when explicitly disabled')
        if _log_mode(head):
            _require(_log_snapshot(root)['note_count'] == 0,
                     'Compile the complete session log before maintenance or transfer')
        if conversation_id != head['conversation_id']:
            if _log_mode(head):
                _require(fields.get('play_log_archive_through', '0') == fields.get('play_log_through', '0'),
                         'Full SAVE before transferring the source conversation')
                fresh_bind = (fields.get('commit_kind') == 'bind' and not head['seq'] and
                              not head.get('public_source_floor') and _log_snapshot(root)['through'] == 0)
                if not fresh_bind:
                    try:
                        remaining = _play_log_module().export_source(root)
                    except (OSError, ValueError) as exc:
                        import play_log
                        _require(fields.get('commit_kind') == 'close' and head.get('public_source_floor') and
                                 play_log._local_floor(Path(root), head, head['public_source_floor']),
                                 'Unavailable old source requires a verified local full-SAVE boundary')
                        source_limit = ('Resumed from the verified local full SAVE. Later old-host messages were unavailable; '
                                        'their absence or acceptance was not checked. ' + str(exc))
                        remaining = None
                    _require(remaining is None or not remaining['receipts'],
                             'Archive the remaining old conversation before rebind')
                head.update(public_source_floor=None, public_source_anchor=None,
                            public_source_origin='conversation-start')
                if source_limit:
                    head['source_transfer_limit'] = source_limit
            head['source_floor'] = None
        head['conversation_id'] = conversation_id
        head['base_save_id'] = fields['save_id']
        head['contract_sha256'] = _hash(_bytes(root, CONTRACT))
        _atomic_write(_path(root, HEAD), _json(head))
        return {'status': 'rebound', 'conversation_id': conversation_id, 'base_save_id': fields['save_id'],
                'source_limit': source_limit}


def disable(root):
    """Explicit opted-out agreement, fully consolidated/archived state; retain history."""
    with _lock(root):
        _idle(root)
        _require(_bytes(root, INTENT) is None, 'Recover preparation before disabling')
        head = _load_json(root, HEAD)
        fields = _fields(_bytes(root, CURRENT) or b'')
        _require(head['pending'] is None and fields.get('campaign_id') == head['campaign_id'] and
                 int(fields.get('journal_through', '0')) == head['seq'] and
                 int(fields.get('journal_archive_through', '0')) == head['seq'],
                 'Full SAVE with no pending state/evidence required before disabling')
        contract = (_bytes(root, CONTRACT) or b'').decode('utf-8').lower()
        _require('incremental persistence: disabled' in contract and 'incremental persistence: enabled' not in contract,
                 'Explicit disabled agreement required')
        _require('incremental recording: write-only-log' not in contract, 'Remove active recording policy before disabling')
        if _log_mode(head):
            _require(_log_snapshot(root)['note_count'] == 0 and
                     fields.get('play_log_archive_through', '0') == fields.get('play_log_through', '0'),
                     'Full SAVE must account for the complete session log before disabling')
        if head['seq']:
            _require(fields.get('journal_head_sha256') == head['head_sha256'] and
                     fields.get('journal_head_receipt_sha256') == head['head_receipt_sha256'],
                     'Consolidated boundary differs')
        target = _path(root, 'INSTANCE/JOURNAL/DISABLED-' + head['stream_id'] + '.json')
        _require(not target.exists(), 'Retained disabled head already exists')
        os.replace(_path(root, HEAD), target)
        return {'status': 'disabled', 'retained_head': target.relative_to(Path(root).absolute()).as_posix()}


def abandon(root, transaction_id, reason):
    """Explicit cancellation only. Retains proposed state and actual results for recovery."""
    with _lock(root):
        head, _ = _load(root)
        _require(head['pending'] == transaction_id and isinstance(reason, str) and reason.strip(),
                 'Explicit pending transaction and cancellation reason required')
        record = {'transaction_id': transaction_id, 'disposition': 'cancelled-uncommitted', 'reason': reason}
        _atomic_write(_path(root, 'INSTANCE/JOURNAL/cancelled/' + _id(transaction_id) + '.json'), _json(record))
        head['pending'] = None
        head['pending_sha256'] = None
        _atomic_write(_path(root, HEAD), _json(head))
        return record


def _publication(root, targets, operation_id):
    """Protect only the declared write set; never recursively scan/copy campaign history."""
    _idle(root)
    operation_id = _id(operation_id)
    opdir = 'RECOVERY/' + operation_id
    _require(not _path(root, opdir).exists(), 'Publication ID already used; recover or choose new ID')
    _require(CURRENT in targets, 'Publication must include current save')
    rows, directories = [], {}
    for relative, after in targets.items():
        target = _path(root, relative)
        before = _bytes(root, relative)
        for parent in target.parents:
            if parent == Path(root).absolute():
                break
            name = parent.relative_to(Path(root).absolute()).as_posix()
            directories[name] = parent.exists()
        rows.append({'path': relative, 'before_sha256': _hash(before) if before is not None else None,
                     'after_sha256': _hash(after), 'before': 'before/' + relative if before is not None else None,
                     'after': 'after/' + relative})
        if before is not None:
            _atomic_write(_path(root, opdir + '/before/' + relative), before)
        _atomic_write(_path(root, opdir + '/after/' + relative), after)
    record = {'schema': 'rpg-publication-v1', 'operation_id': operation_id, 'status': 'started',
              'write_set': rows, 'directories': directories}
    _atomic_write(_path(root, opdir + '/operation.json'), _json(record))
    description = '# Protected journal publication\noperation_id: ' + operation_id + '\nstatus: started\n'
    description += 'Machine-readable target, verified preimages and directory inventory: `operation.json`.\n'
    _atomic_write(_path(root, opdir + '/OPERATION.md'), description.encode('utf-8'))
    plan_hash = _hash(_json({k: v for k, v in record.items() if k != 'status'}))
    _atomic_write(_path(root, ACTIVE), ('operation_id: ' + operation_id + '\nrecord: ' + opdir +
                                      '/OPERATION.md\nplan_sha256: ' + plan_hash + '\n').encode('utf-8'))
    _finish_publication(root, record, 'finish')


def _finish_publication(root, record, action):
    opdir = 'RECOVERY/' + _id(record['operation_id'])
    _require(record.get('schema') == 'rpg-publication-v1', 'Foreign recovery procedure; follow its owning protocol')
    _require(action in ('finish', 'restore'), 'Unknown recovery action')
    _require(record['status'] in ('started', 'complete', 'restored'), 'Malformed recovery status')
    rows = record['write_set']
    _require(len({r['path'].casefold() for r in rows}) == len(rows), 'Duplicate recovery path')
    # Check ALL retained targets and live preimages before resuming any mutation.
    for row in rows:
        relative = row['path']
        _require(row['after'] == 'after/' + relative and
                 (row['before'] is None) == (row['before_sha256'] is None) and
                 (row['before'] is None or row['before'] == 'before/' + relative),
                 'Malformed recovery preimage/target identity')
        _require(relative == HEAD or _allowed(relative) or relative.startswith('ARCHIVE/') or
                 relative.startswith('EVIDENCE/'), 'Out-of-scope recovery target')
        after = _bytes(root, opdir + '/' + row['after'])
        _require(after is not None and _hash(after) == row['after_sha256'], 'Missing/corrupt retained target')
        if row['before']:
            before = _bytes(root, opdir + '/' + row['before'])
            _require(before is not None and _hash(before) == row['before_sha256'], 'Missing/corrupt preimage')
        live = _bytes(root, relative)
        _require((_hash(live) if live is not None else None) in (row['before_sha256'], row['after_sha256']),
                 'Unexpected live change; preserve recovery and investigate: ' + relative)
    for row in sorted(rows, key=lambda r: r['path'] == CURRENT):
        relative = row['path']
        target = _path(root, relative)
        source = row['after'] if action == 'finish' else row['before']
        if source is None:
            if target.exists():
                target.unlink()
        else:
            _publish_write(target, _bytes(root, opdir + '/' + source))
    if action == 'restore':
        for relative, existed in sorted(record['directories'].items(), key=lambda r: -len(r[0])):
            if not existed:
                directory = _path(root, relative)
                if directory.exists():
                    _require(not any(directory.iterdir()), 'Unexpected content in newly created directory')
                    directory.rmdir()
    for row in rows:
        actual = _bytes(root, row['path'])
        expected = row['after_sha256'] if action == 'finish' else row['before_sha256']
        _require((_hash(actual) if actual is not None else None) == expected, 'Publication verification failed')
    record['status'] = 'complete' if action == 'finish' else 'restored'
    _atomic_write(_path(root, opdir + '/operation.json'), _json(record))
    _atomic_write(_path(root, opdir + '/OPERATION.md'),
                  ('# Protected journal publication\noperation_id: ' + record['operation_id'] +
                   '\nstatus: ' + record['status'] + '\nVerified details and retained preimages: `operation.json`.\n').encode('utf-8'))
    _path(root, ACTIVE).unlink()


def recover(root, action):
    with _lock(root):
        marker = _bytes(root, ACTIVE)
        _require(marker, 'No active publication to recover')
        match = re.search(r'^operation_id: ([A-Za-z0-9_.-]+)$', marker.decode('utf-8'), re.M)
        _require(match, 'Malformed recovery marker')
        record = _load_json(root, 'RECOVERY/' + _id(match.group(1)) + '/operation.json')
        _require(record.get('operation_id') == match.group(1), 'Recovery operation identity mismatch')
        expected = re.search(r'^plan_sha256: ([a-f0-9]{64})$', marker.decode('utf-8'), re.M)
        _require(expected and expected.group(1) == _hash(_json({k: v for k, v in record.items() if k != 'status'})),
                 'Recovery plan changed; preserve records and inspect original protected plan')
        _finish_publication(root, record, action)
        return {'status': 'complete' if action == 'finish' else 'restored'}


def _boundary_updates(root, targets, plan):
    """Apply one declared set of ADMIN compilation edits before publication metadata."""
    updates = plan.get('current_updates', []) if plan is not None else []
    _require(isinstance(updates, list), 'Boundary current_updates must be a list')
    seen = set()
    for change in updates:
        path = change['path']
        _path(root, path)
        _require(_allowed(path), 'Unsupported administrative owner; use its protected procedure')
        _require(path.casefold() not in seen and
                 not any(k.casefold() == path.casefold() and k != path for k in targets),
                 'Duplicate or aliased administrative owner update')
        seen.add(path.casefold())
        before = targets[path] if path in targets else _bytes(root, path)
        _require((_hash(before) if before is not None else None) == change['expected_sha256'],
                 'Stale session boundary update')
        if before is None:
            _require(isinstance(change.get('content'), str) and 'edits' not in change,
                     'New authorized boundary record requires its complete established content')
            after = change['content'].encode('utf-8')
        else:
            _require('content' not in change and isinstance(change.get('edits'), list),
                     'Existing boundary record requires targeted edits')
            after = _apply_edits(before.decode('utf-8'), change['edits']).encode('utf-8')
        if path == CURRENT:
            _require(all(_fields(before).get(k) == _fields(after).get(k) for k in IMMUTABLE),
                     'Boundary update cannot rewrite save identity or log boundaries')
        if before != after:
            targets[path] = after


def _compilation_snapshot(root, head, plan):
    if not _log_mode(head):
        return None
    snapshot = _log_snapshot(root)
    supplied = plan.get('log_snapshot') if plan is not None else None
    if snapshot['note_count']:
        _require(plan is not None and plan.get('log_compilation') == 'reviewed',
                 'Uncompiled session notes require explicit reviewed log compilation')
        _require(isinstance(supplied, dict), 'Compilation needs its chosen log snapshot')
    if supplied is not None:
        _require(isinstance(supplied, dict) and type(supplied.get('through')) is int and
                 type(supplied.get('after')) is int and supplied['after'] == snapshot['after'] and
                 supplied['through'] == snapshot['through'] and
                 supplied.get('prefix_sha256') == snapshot['prefix_sha256'],
                 'Stale or altered log snapshot; review the actual unconsumed notes')
    return snapshot


def _checkpoint_targets(root, head, fields, save_id, plan=None):
    _require(head['pending'] is None, 'Confirm or explicitly reconcile prepared response before publication')
    _id(save_id)
    _require(save_id != fields['save_id'], 'New save ID required')
    _require(save_id not in head.get('published_save_ids', [head['base_save_id']]) and
             save_id != fields.get('save_parent'), 'Save ID already belongs to prior state')
    archive_index = (_bytes(root, 'ARCHIVE/INDEX.md') or b'').decode('utf-8')
    _require(not re.search(r'(?m)^\|\s*' + re.escape(save_id) + r'\s*\|', archive_index),
             'Save ID already owns archived history')
    _require(not _path(root, 'RECOVERY/journal-' + save_id).exists(), 'Save ID has already been used')
    if plan is not None:
        basis = 'expected_base_save_id' if _log_mode(head) else 'expected_head'
        expected = head['base_save_id'] if _log_mode(head) else head['head']
        _require(isinstance(plan, dict) and plan.get(basis, object()) == expected,
                 'Compilation plan is for a different stopping point')
        _require(plan.get('save_id', save_id) == save_id, 'Conflicting save ID in compilation plan')
    snapshot = _compilation_snapshot(root, head, plan)
    overlay = _effective(root, head, fields)
    _boundary_updates(root, overlay, plan)
    current = overlay.get(CURRENT, _bytes(root, CURRENT))
    updates = {'save_id': save_id, 'save_parent': fields['save_id'],
               'save_rev': str(int(fields['save_rev']) + 1), 'commit_kind': 'checkpoint',
               'journal_through': str(head['seq']), 'journal_stream': head['stream_id']}
    if head['seq']:
        updates.update(journal_head=head['head'], journal_head_sha256=head['head_sha256'],
                       journal_head_receipt_sha256=head['head_receipt_sha256'])
    if snapshot is not None:
        updates.update(play_log_through=str(snapshot['through']), play_log_prefix_sha256=snapshot['prefix_sha256'])
    for key, value in updates.items():
        current = _set_field(current, key, value)
    current = _set_section(current, 'Save review',
        'State consolidated through journal sequence ' + str(head['seq']) + ', transaction ' + str(head['head']) + '.\n'
        'History archived through: ' + fields['evidence_through'] + '. This checkpoint adds no archived evidence.\n'
        'Review: lightweight affected-record publication checks; no new semantic source-review claim. '
        'Earlier review records remain retained with their original save/recovery evidence.' +
        ('\nSession log compilation acknowledged through byte ' + str(snapshot['through']) +
         '; GM review is an attestation, not a machine proof of semantic completeness.' if snapshot is not None else ''))
    overlay[CURRENT] = current
    updated_head = dict(head, base_save_id=save_id,
                        published_save_ids=head.get('published_save_ids', [head['base_save_id']]) + [save_id])
    if snapshot is not None and snapshot['note_count']:
        updated_head['last_log_compilation'] = {
            'save_id': save_id, 'through': snapshot['through'], 'prefix_sha256': snapshot['prefix_sha256'],
            'acknowledgement': 'reviewed', 'note': 'GM attestation; storage checks do not prove semantic completeness'}
    overlay[HEAD] = _json(updated_head)
    return overlay


def checkpoint(root, save_id, plan=None):
    with _lock(root):
        head, fields = _load(root)
        if fields['save_id'] == save_id:
            _require(fields.get('commit_kind') == 'checkpoint' and
                     int(fields.get('journal_through', '0')) == head['seq'] and head['pending'] is None,
                     'Save ID reused after more progress or with different kind')
            if _log_mode(head):
                snapshot = _log_snapshot(root)
                _require(snapshot['note_count'] == 0, 'Save ID reused after further log progress')
            return {'status': 'already-published', 'save_id': save_id}
        targets = _checkpoint_targets(root, head, fields, save_id, plan)
        _publication(root, targets, 'journal-' + save_id)
        return {'status': 'checkpoint-published', 'save_id': save_id, 'consolidated_through': head['seq'],
                'evidence_through': fields['evidence_through'], 'new_evidence_archived': False}


def _source_identity(receipt):
    ref = receipt['source_ref']
    return receipt['conversation_id'], ref.get('turn_id'), ref.get('message_id')


def _source_after(receipt, previous):
    _require(_source_identity(receipt) != _source_identity(previous), 'Public source repeats its archived boundary')
    ref, old = receipt['source_ref'], previous['source_ref']
    if ref['path'] == old['path']:
        _require(ref['end_line'] > old['end_line'], 'Public source is not after the archived boundary')
        return
    from datetime import datetime
    try:
        _require(ref.get('completed_at') and old.get('completed_at'), 'Public source ordering needs observed completion times')
        newer = datetime.fromisoformat(ref['completed_at']) > datetime.fromisoformat(old['completed_at'])
    except (ValueError, TypeError) as exc:
        raise PersistenceError('Unknown public source ordering') from exc
    _require(newer, 'Public source is not after the archived boundary')


def _public_sources(root, head, plan):
    """SAVE-only actual conversation export, never an interpretation of PLAY_LOG."""
    if not _log_mode(head):
        return [], None, None
    gap = plan.get('source_gap')
    _require(gap is None or isinstance(gap, str) and gap.strip(), 'Source gap must state the actual limitation')
    exported = None
    try:
        exported = _play_log_module().export_source(root)
    except (OSError, ValueError) as exc:
        _require(gap is not None, 'Actual public-source export unavailable; state an explicit source_gap: ' + str(exc))
    supplied = plan.get('public_source_receipts')
    _require(supplied is None or isinstance(supplied, list), 'public_source_receipts must be a list')
    if exported is not None:
        _require(isinstance(exported, dict) and isinstance(exported.get('receipts'), list) and
                 exported.get('conversation_id') == head['conversation_id'] and
                 exported.get('checked_empty') is (not exported['receipts']), 'Malformed or foreign public-source export')
        expected = exported['receipts']
        if supplied is not None:
            _require(supplied == expected, 'Supplied public source differs from the actual stable source export')
        receipts = expected
    else:
        receipts = supplied or []
    floor = head.get('public_source_floor') or head.get('source_floor')
    _require(floor is not None or head.get('public_source_origin') == 'conversation-start' or not receipts and gap is not None,
             'An actual public-source archive boundary is required')
    previous, seen = floor, set()
    for receipt in receipts:
        if exported is None:
            _verify_host_receipt(receipt)
        _require(receipt['conversation_id'] == head['conversation_id'], 'Public source belongs to another conversation')
        identity = _source_identity(receipt)
        _require(identity not in seen, 'Duplicate public-source message')
        seen.add(identity)
        if previous is not None:
            _source_after(receipt, previous)
        previous = receipt
    coverage = {'checked_export': exported is not None, 'checked_empty': bool(exported and exported['checked_empty']),
                'message_count': len(receipts), 'source_gap': gap,
                'note': 'Actual completed conversation, including possible OOC; delivery is not fictional acceptance.'}
    return receipts, gap, coverage


def _check_close_review(root, targets, source_path, review):
    """Verify the existing bounded review against exact proposed bytes, not semantics."""
    import evidence
    receipt = review.get('receipt')
    _require(isinstance(receipt, dict) and {'bundle', 'report', 'report_sha256'} <= set(receipt),
             'Complete review requires its existing bounded bundle/report/hash receipt')
    for key in ('bundle', 'report', 'delivery_receipt'):
        if receipt.get(key):
            _require(isinstance(receipt[key], str) and receipt[key].startswith('EVIDENCE/'),
                     'Retain complete review artifacts under relative EVIDENCE paths before publication')
            _path(root, receipt[key])
    bundle, report = (_path(root, receipt[key]) for key in ('bundle', 'report'))
    _require(_hash(report.read_bytes()) == receipt['report_sha256'], 'Review report changed after review')
    capture = evidence.check_capture(bundle / 'capture')
    _require(capture['status'] == 'captured' and capture['source_sha256'] == _hash(targets[source_path]),
             'Review capture differs from the actual source proposed for this SAVE')
    delivery = Path(root) / receipt['delivery_receipt'] if receipt.get('delivery_receipt') else None
    checked = evidence.check_save_audit(bundle, report, root, delivery, proposed=targets)
    _require(checked['review_status'] == 'completed' and checked['record_consistency'] == 'consistent' and
             checked['review_covered_through'] is not None and
             checked['review_covered_through']['end_line'] == capture['manifest']['byte_coverage']['source_line_count'],
             'Complete SAVE requires the declared bounded source review through this stopping point')
    owners = {path for path in targets if _allowed(path)}
    _require(owners <= set(checked['matched_paths']), 'Review omits a proposed affected owner')


def close(root, plan, preview=None):
    """Archive exactly confirmed public exchanges; review is an explicit external judgment.

Plan: save_id, title, route_terms, span, place, session_id, review{status,scope,
limitations,receipt?}, optional current_updates using the prepare edit grammar.
All available public source in the new journal span is retained, including no-op
exchanges. Do not infer missing pre-journal evidence or unrecorded tool results.
"""
    with _lock(root):
        head, fields = _load(root)
        save_id = _id(plan['save_id'])
        basis = 'expected_base_save_id' if _log_mode(head) else 'expected_head'
        expected = head['base_save_id'] if _log_mode(head) else head['head']
        _require(plan.get(basis, object()) == expected or fields['save_id'] == save_id,
                 'Full-save plan is for a different stopping point')
        _require(isinstance(plan.get('review'), dict) and plan['review'].get('status') in
                 ('complete', 'incomplete', 'not-selected'), 'Declared bounded review outcome required')
        review = plan['review']
        _require(isinstance(review.get('scope'), str) and isinstance(review.get('limitations'), str),
                 'Review scope and limitations required')
        if _log_mode(head) and review['status'] == 'complete':
            _require(review['scope'].strip() and review['limitations'].strip(),
                     'Complete review requires a meaningful scope and stated limitations')
        _require(not (_log_mode(head) and plan.get('source_gap') and review['status'] == 'complete'),
                 'A declared source gap requires incomplete or not-selected review status')
        if fields['save_id'] == save_id:
            _require(fields.get('commit_kind') == 'close' and int(fields.get('journal_archive_through', '0')) == head['seq'],
                     'Save ID conflicts with existing publication')
            if _log_mode(head):
                _require(_log_snapshot(root)['note_count'] == 0, 'Save ID reused after further log progress')
                remaining, _gap, _coverage = _public_sources(root, head, plan)
                _require(not remaining, 'Save ID reused after further completed conversation')
            return {'status': 'already-published', 'save_id': save_id}
        targets = _checkpoint_targets(root, head, fields, save_id, plan)
        public_receipts, source_gap, public_coverage = _public_sources(root, head, plan)
        through = int(fields.get('journal_archive_through', '0'))
        anchor = ((fields.get('journal_archive_head'), fields.get('journal_archive_sha256'),
                   fields.get('journal_archive_receipt_sha256')) if through else (None, None, None))
        batches = _chain(root, head, through, anchor)
        folder = 'sessions/' + save_id
        body_path = 'ARCHIVE/' + folder + '/01_record.md'
        _require(_bytes(root, body_path) is None, 'Archive destination already exists')
        evidence_id = 'E-' + save_id + '-01'
        body = ('# Actual public conversation source' if _log_mode(head) else '# Accepted incremental source')
        body += '\n\n## ' + evidence_id + '\n\n'
        body += ('Coverage: available completed public messages after the prior source boundary. ' if _log_mode(head)
                 else 'Coverage: completed, source-matched public exchanges in this journal span. ')
        body += 'Prepared state, private determinations and internal reasoning are excluded. '
        body += 'Earlier evidence coverage remains as previously recorded.\n\n'
        if not batches and not public_receipts:
            body += 'No newly captured gameplay exchanges. This administrative save invents no dialogue.\n'
        if _log_mode(head):
            body += ('\nThe public conversation section below preserves actual completed messages, including possible OOC. '
                     'Completion alone does not make a statement accepted fiction. The session log is retained separately; '
                     'private notes are not copied into this public-source body.\n\n')
            if source_gap:
                body += '### Declared source gap\n\n' + source_gap + '\n\n'
        dispositions = plan.get('source_dispositions', {})
        _require(isinstance(dispositions, dict) and set(dispositions).issubset(
                    {b['transaction_id'] for b in batches} | {r['source_ref']['message_id'] for r in public_receipts}),
                 'Disposition must identify a transaction in this archive span')
        def fenced(text):
            runs = [len(s) for s in re.findall(r'`+', text)]
            fence = '`' * max(3, max(runs, default=0) + 1)
            return fence + 'text\n' + text + '\n' + fence + '\n\n'
        for batch in batches:
            receipt = _load_json(root, 'INSTANCE/JOURNAL/receipts/' + batch['transaction_id'] + '.json')
            user_source = ('\n\n'.join(m['text'] for m in receipt['user_messages'])
                           if receipt['observer'] == 'codex-rollout' else receipt.get('user_text', batch['user_text']))
            disposition = dispositions.get(batch['transaction_id'])
            if disposition:
                _require(disposition.get('status') in ('superseded', 'partly-superseded') and disposition.get('reason') and
                         disposition.get('correction_ref'), 'Explicit accepted supersession reference required')
                if disposition['status'] == 'superseded':
                    body += ('### Superseded exchange ' + batch['transaction_id'] + '\n\n'
                             'Excluded from accepted fiction; original source remains retained in the journal.\n\n' +
                             fenced(json.dumps(disposition, ensure_ascii=False)))
                    continue
                _require(isinstance(disposition.get('spans'), list) and disposition['spans'],
                         'Partial supersession needs exact source character spans')
                body += ('### Partly superseded exchange ' + batch['transaction_id'] + '\n\n'
                         'Preserved surviving original spans follow. Superseded source remains in the journal.\n\n' +
                         fenced(json.dumps(disposition, ensure_ascii=False)))
                for role, source in (('user', user_source), ('assistant', batch['response'])):
                    spans = []
                    for span in disposition['spans']:
                        _require(span.get('role') in ('user', 'assistant') and type(span.get('start')) is int
                                 and type(span.get('end')) is int, 'Invalid source span role or character offsets')
                        if span['role'] == role:
                            _require(0 <= span['start'] < span['end'] <= len(source), 'Source span out of bounds')
                            spans.append((span['start'], span['end']))
                    position = 0
                    body += role.capitalize() + ':\n\n'
                    for start, end in sorted(spans):
                        _require(start >= position, 'Overlapping superseded spans')
                        if start > position:
                            body += fenced(source[position:start])
                        body += '[Superseded source characters ' + str(start) + ':' + str(end) + ' excluded.]\n\n'
                        position = end
                    if position < len(source):
                        body += fenced(source[position:])
                continue
            body += '### Exchange ' + batch['transaction_id'] + '\n\nUser:\n\n'
            body += fenced(user_source) + 'GM:\n\n' + fenced(batch['response'])
        for receipt in public_receipts:
            user_source = '\n\n'.join(m['text'] for m in receipt['user_messages'])
            body += '### Actual public conversation — ' + receipt['source_ref']['message_id'] + '\n\n'
            disposition = dispositions.get(receipt['source_ref']['message_id'])
            if disposition:
                _require(disposition.get('status') in ('superseded', 'partly-superseded') and
                         isinstance(disposition.get('reason'), str) and disposition['reason'].strip() and
                         isinstance(disposition.get('correction_ref'), str) and disposition['correction_ref'].strip(),
                         'Public correction needs status, reason and a direct correction reference')
                correction = disposition['correction_ref'].split('#', 1)
                _require(correction[0] == 'INSTANCE/CORRECTIONS.md' and len(correction) == 2 and correction[1],
                         'Public correction must name an existing unique literal correction heading')
                import read_source
                document = read_source.load_document(Path(root), correction[0])
                _require(sum(section['heading'] == correction[1] for section in read_source.list_sections(document)) == 1,
                         'Public correction heading is absent or ambiguous')
                if disposition['status'] == 'partly-superseded':
                    spans = disposition.get('spans')
                    _require(isinstance(spans, list) and spans, 'Partial correction requires exact superseded source spans')
                    prior_ends = {'user':0, 'assistant':0}
                    texts = {'user':user_source, 'assistant':receipt['assistant_text']}
                    for span in spans:
                        role = span.get('role')
                        _require(role in texts and type(span.get('start')) is int and type(span.get('end')) is int and
                                 prior_ends[role] <= span['start'] < span['end'] <= len(texts[role]),
                                 'Partial correction spans must be ordered, nonoverlapping and inside original text')
                        prior_ends[role] = span['end']
                body += 'Correction applies; original words below are retained as source, not reinstated fiction.\n\n'
                body += fenced(json.dumps(disposition, ensure_ascii=False))
            body += 'User:\n\n' + fenced(user_source) + 'Assistant:\n\n' + fenced(receipt['assistant_text'])
            body += 'Original source reference:\n\n' + fenced(json.dumps(receipt['source_ref'], ensure_ascii=False, sort_keys=True))
        operational = plan.get('operational_evidence', [])
        _require(isinstance(operational, list), 'Operational evidence must be an explicit list')
        for item in operational:
            _require(isinstance(item, dict) and item.get('session_id') and isinstance(item.get('text'), str)
                     and item.get('source_ref'), 'Actual labelled session evidence and source required')
            body += ('### OOC session operational evidence\n\nSession: ' + _id(item['session_id']) + '\n\n' +
                     fenced(item['text']) + 'Source: ' + fenced(json.dumps(item['source_ref'], ensure_ascii=False)))
        targets[body_path] = body.encode('utf-8')
        for key in ('title', 'route_terms', 'span', 'place', 'session_id'):
            _require(isinstance(plan.get(key), str) and plan[key] and '\n' not in plan[key] and '|' not in plan[key],
                     'One-line archive routing field required: ' + key)
        index = ('# Save evidence routes\n\n## R-' + save_id + '-01 — ' + plan['title'] + '\n'
                 'File: `01_record.md`\nEvidence: `' + evidence_id + '`\nTime: ' + plan['span'] +
                 '\nPeople: ' + plan.get('people', 'recorded participants') + '\nPlaces: ' + plan['place'] +
                 '\nTopics: ' + plan['route_terms'] + '\nNotable:\n- Exact selected public source; declared exclusions and review limits.\n')
        targets['ARCHIVE/' + folder + '/INDEX.md'] = index.encode('utf-8')
        archive_index = (_bytes(root, 'ARCHIVE/INDEX.md') or b'').decode('utf-8')
        table_rows = list(re.finditer(r'(?m)^\|[^\r\n]+\|[ \t]*$', archive_index))
        _require(table_rows, 'Missing campaign archive index table')
        row = ('| ' + save_id + ' | close | ' + plan['session_id'] + ' | ' + plan['span'] + ' | ' +
               plan['place'] + ' | ' + plan['route_terms'] + ' | Incremental source; review ' + review['status'] +
               ' | ' + folder + ' | ' + folder + '/INDEX.md |  |')
        last = table_rows[-1]
        newline = '\r\n' if '\r\n' in archive_index else '\n'
        targets['ARCHIVE/INDEX.md'] = (archive_index[:last.end()] + newline + row + archive_index[last.end():]).encode('utf-8')
        current = targets[CURRENT]
        updates = {'commit_kind': 'close', 'archive_ref': folder, 'evidence_through': save_id,
                   'journal_archive_through': str(head['seq'])}
        if head['seq']:
            updates.update(journal_archive_head=head['head'], journal_archive_sha256=head['head_sha256'],
                           journal_archive_receipt_sha256=head['head_receipt_sha256'])
        if _log_mode(head):
            compiled = _fields(current)
            updates.update(play_log_archive_through=compiled['play_log_through'],
                           play_log_archive_prefix_sha256=compiled['play_log_prefix_sha256'])
        for key, value in updates.items():
            current = _set_field(current, key, value)
        current = _set_section(current, 'Save review',
            'State consolidated and available accepted journal evidence accounted through sequence ' + str(head['seq']) + '.\n'
            'Declared review status: ' + review['status'] + '. Actual scope and limitations: '
            '`EVIDENCE/incremental-reviews/' + save_id + '.json`. Read that report before treating the save as reviewed. '
            'Storage verification does not establish semantic completeness.' +
            ('\nSession log accounted through byte ' + _fields(current)['play_log_through'] +
             '. Actual completed public conversation and source limitations are declared in the retained review record.'
             if _log_mode(head) else ''))
        targets[CURRENT] = current
        review_record = {'schema': 'rpg-incremental-review-v1', 'save_id': save_id,
                        'state_through': head['seq'], 'source_from_exclusive': through,
                        'source_through': head['seq'], 'review': review,
                        'note': 'Reported semantic review; helper verifies bytes, never semantic completeness.'}
        if _log_mode(head):
            review_record['public_source_coverage'] = public_coverage
            review_record['log_compilation'] = {
                'through': int(_fields(current)['play_log_through']),
                'prefix_sha256': _fields(current)['play_log_prefix_sha256'],
                'acknowledgement': plan.get('log_compilation', 'no new uncompiled notes')}
            next_head = json.loads(targets[HEAD])
            if public_receipts:
                next_head['public_source_floor'] = public_receipts[-1]
                next_head['public_source_anchor'] = {
                    'save_id': save_id, 'path': body_path, 'sha256': _hash(targets[body_path]),
                    'floor_sha256': _hash(json.dumps(public_receipts[-1], sort_keys=True,
                                                     ensure_ascii=False).encode('utf-8'))}
            if source_gap:
                next_head['public_source_gap'] = source_gap
            targets[HEAD] = _json(next_head)
        targets['EVIDENCE/incremental-reviews/' + save_id + '.json'] = _json(review_record)
        if preview is not None:
            destination = Path(preview).absolute()
            campaign = Path(root).absolute()
            _require(not destination.exists() and destination != campaign and
                     (not destination.is_relative_to(campaign) or
                      destination.is_relative_to(campaign / '.work')), 'Preview needs a new isolated output directory')
            _path(destination, CURRENT)  # Refuse links/reparse ancestors before creating anything.
            for path, data in targets.items():
                _atomic_write(_path(destination, path), data)
            return {'status': 'save-preview', 'directory': str(destination), 'save_id': save_id,
                    'source': body_path, 'affected_owners': sorted(path for path in targets if _allowed(path)),
                    'review': 'Review this exact source and proposed owners once; close verifies the existing report.'}
        if _log_mode(head) and review['status'] == 'complete':
            try:
                _check_close_review(root, targets, body_path, review)
            except Exception as exc:
                raise PersistenceError('Bounded SAVE review not verified: ' + str(exc)) from exc
        _publication(root, targets, 'journal-' + save_id)
        return {'status': 'full-save-published', 'save_id': save_id, 'archived_exchanges': len(batches) + len(public_receipts),
                'review_status': review['status'], 'limitations': review['limitations'],
                **({'archived_public_messages': len(public_receipts), 'source_gap': source_gap} if _log_mode(head) else {})}


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', default='.')
    commands = p.add_subparsers(dest='command', required=True)
    init = commands.add_parser('init'); init.add_argument('--conversation-id', required=True); init.add_argument('--source-floor')
    commands.add_parser('status'); commands.add_parser('pending')
    continuing = commands.add_parser('resume'); continuing.add_argument('--source')
    continuing.add_argument('--full', action='store_true', help='Include the full effective CURRENT_SAVE body')
    continuing.add_argument('--path', action='append', default=[], help='Include this effective current owner; repeat to bundle reads')
    commands.add_parser('recover-prepare')
    commands.add_parser('disable')
    read = commands.add_parser('read'); read.add_argument('--path', required=True)
    stage = commands.add_parser('prepare'); stage.add_argument('--input', required=True)
    acknowledge = commands.add_parser('confirm'); acknowledge.add_argument('--receipt', required=True)
    cancel = commands.add_parser('abandon'); cancel.add_argument('--transaction-id', required=True); cancel.add_argument('--reason', required=True)
    check = commands.add_parser('checkpoint'); check.add_argument('--save-id'); check.add_argument('--plan')
    full = commands.add_parser('close'); full.add_argument('--plan', required=True); full.add_argument('--preview')
    repair = commands.add_parser('recover'); repair.add_argument('--action', choices=('finish', 'restore'), required=True)
    bind = commands.add_parser('rebind'); bind.add_argument('--conversation-id', required=True); bind.add_argument('--expected-base', required=True)
    return p


def main():
    args = parser().parse_args()
    root = Path(args.root).absolute()
    try:
        if args.command == 'init': result = initialize(root, args.conversation_id,
            json.loads(Path(args.source_floor).read_bytes()) if args.source_floor else None)
        elif args.command == 'status': result = status(root)
        elif args.command == 'pending': result = pending(root)
        elif args.command == 'resume': result = resume(root, args.source, compact=not args.full, paths=args.path)
        elif args.command == 'recover-prepare': result = recover_prepare(root)
        elif args.command == 'disable': result = disable(root)
        elif args.command == 'read': result = read_current(root, args.path)
        elif args.command == 'prepare': result = prepare(root, json.loads(Path(args.input).read_bytes()))
        elif args.command == 'confirm': result = confirm(root, json.loads(Path(args.receipt).read_bytes()))
        elif args.command == 'abandon': result = abandon(root, args.transaction_id, args.reason)
        elif args.command == 'checkpoint':
            plan = json.loads(Path(args.plan).read_bytes()) if args.plan else None
            save_id = args.save_id or (plan or {}).get('save_id')
            _require(save_id, 'Checkpoint requires --save-id or a plan containing save_id')
            result = checkpoint(root, save_id, plan)
        elif args.command == 'close': result = close(root, json.loads(Path(args.plan).read_bytes()), args.preview)
        elif args.command == 'rebind': result = rebind(root, args.conversation_id, args.expected_base)
        else: result = recover(root, args.action)
        print(json.dumps(result, ensure_ascii=True))
        return 0
    except (PersistenceError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'status': 'blocked', 'error': str(exc)}, ensure_ascii=True))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
