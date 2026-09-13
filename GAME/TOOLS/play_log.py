#!/usr/bin/env python3
"""PLAY: one write-only note. Reading/compilation/export belong to ADMIN.

This is a working log, not a receipt proving that a response was delivered.
No model calls, record patches, source checks or readback occur during append.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
import uuid

LOG = 'INSTANCE/PLAY_LOG.jsonl'


class LogError(ValueError):
    pass


def append(root, text):
    """Append one small UTF-8 record, without reading any campaign data."""
    if not isinstance(text, str) or not text.strip():
        raise LogError('A nonempty short note is required')
    identity = uuid.uuid4().hex
    data = (json.dumps({'id': identity, 'text': text.strip()}, ensure_ascii=False,
                       separators=(',', ':')) + '\n').encode('utf-8')
    # Fixed local destination. INSTANCE already exists in a bound campaign.
    # O_APPEND preserves previous entries; no reads, seeking, hashes or readback.
    flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, 'O_BINARY', 0)
    fd = os.open(Path(root) / LOG, flags, 0o600)
    try:
        written = os.write(fd, data)
        if written != len(data):
            raise OSError('Partial log append; retain it for checkpoint repair, do not retry blindly')
        os.fsync(fd)
    finally:
        os.close(fd)
    return {'logged': identity}


def snapshot(root):
    """ADMIN/fresh-resume only: read notes beyond the compiled byte boundary."""
    import hashlib
    root = Path(root)
    current = (root / 'INSTANCE/CURRENT_SAVE.md').read_text(encoding='utf-8')
    fields = dict(re.findall(r'^\|\s*(play_log_[a-z0-9_]+)\s*\|\s*([^|\r\n]+?)\s*\|\s*$',
                             current, re.M))
    try:
        after = int(fields.get('play_log_through', '0'))
    except ValueError:
        raise LogError('Invalid compiled log offset') from None
    path = root / LOG
    data = path.read_bytes() if path.exists() else b''
    if not 0 <= after <= len(data) or (after and data[after-1:after] != b'\n'):
        raise LogError('Compiled log boundary is missing or truncated')
    prior = fields.get('play_log_prefix_sha256', hashlib.sha256(b'').hexdigest())
    if hashlib.sha256(data[:after]).hexdigest() != prior:
        raise LogError('Previously compiled log prefix changed')
    tail = data[after:]
    if tail and not tail.endswith(b'\n'):
        raise LogError('Incomplete log tail; reconcile at checkpoint, do not delete or retry it blindly')
    entries = []
    ids = set()
    for line in tail.splitlines():
        try:
            item = json.loads(line)
        except (ValueError, UnicodeError):
            raise LogError('Malformed uncompiled log entry') from None
        if (not isinstance(item, dict) or set(item) != {'id', 'text'} or
                not isinstance(item['id'], str) or not re.fullmatch(r'[0-9a-f]{32}', item['id']) or
                not isinstance(item['text'], str) or not item['text'].strip() or item['id'] in ids):
            raise LogError('Invalid or duplicate uncompiled log entry')
        ids.add(item['id'])
        entries.append(item)
    return {'after': after, 'through': len(data), 'prefix_sha256': hashlib.sha256(data).hexdigest(),
            'entries': entries, 'note_count': len(entries)}


def _local_floor(root, head, floor):
    """Validate a published local boundary, never an arbitrary HEAD-only claim."""
    import hashlib
    anchor = head.get('public_source_anchor')
    if anchor:
        save = anchor.get('save_id', '')
        path = 'ARCHIVE/sessions/' + save + '/01_record.md'
        if (not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', save) or '..' in save or
                save not in head.get('published_save_ids', []) or anchor.get('path') != path):
            raise LogError('Invalid published archive source boundary')
        index = (root / 'ARCHIVE/INDEX.md').read_text(encoding='utf-8')
        if not re.search(r'^\|\s*' + re.escape(save) + r'\s*\|\s*close\s*\|', index, re.M):
            raise LogError('Published source boundary has no archive owner')
        import read_source
        try:
            source = read_source.load_document(root, path, expected_sha256=anchor.get('sha256'))['text']
        except read_source.SourceError as exc:
            raise LogError('Published local source archive unavailable: ' + str(exc)) from exc
        digest = hashlib.sha256(json.dumps(floor, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()
        if (digest != anchor.get('floor_sha256') or
                '### Actual public conversation — ' + floor['source_ref']['message_id'] not in source or
                json.dumps(floor['source_ref'], ensure_ascii=False, sort_keys=True) not in source or
                floor['assistant_text'] not in source):
            raise LogError('Source boundary differs from its published archive anchor')
        return True
    # Migration compatibility: the last archived v1 receipt is already locally
    # preserved and hash-bound by CURRENT_SAVE; no old host file is needed again.
    current = root/'INSTANCE/CURRENT_SAVE.md'
    fields = dict(re.findall(r'^\|\s*([a-z][a-z0-9_]+)\s*\|\s*([^|\r\n]+?)\s*\|\s*$',
                             current.read_text(encoding='utf-8'), re.M)) if current.exists() else {}
    identity = fields.get('journal_archive_head', '')
    if identity and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', identity) and '..' not in identity:
        data = (root/'INSTANCE/JOURNAL/receipts'/f'{identity}.json').read_bytes()
        if (hashlib.sha256(data).hexdigest() == fields.get('journal_archive_receipt_sha256') and
                json.loads(data) == floor and int(fields.get('journal_archive_through', '0')) > 0):
            return True
    return False


def export_source(root, sources=None, codex_home=None):
    """SAVE only: collect actual completed public exchanges since the archive floor.

The adapter selects public user/final items. Reasoning and tool arguments are
never exported. Logs are observations, not instructions or automatic fiction.
"""
    import codex_exchange as cx
    from datetime import datetime
    root = Path(root)
    head = json.loads((root / 'INSTANCE/JOURNAL/HEAD.json').read_bytes())
    thread = head['conversation_id']
    floor = head.get('public_source_floor') or head.get('source_floor')
    if not floor and head.get('public_source_origin') != 'conversation-start':
        raise LogError('An explicit archive source boundary is required')
    local_floor = floor and _local_floor(root, head, floor)
    ref = floor['source_ref'] if floor else None
    floor_time = datetime.fromisoformat(ref['completed_at'].replace('Z', '+00:00')) if ref else None
    selected = list(sources) if sources is not None else cx.discover(thread, codex_home)
    if floor and not local_floor:
        selected.append(ref['path'])
    observed = cx.observe(thread, selected)
    if floor and not local_floor:
        actual = cx.capture(thread, floor['assistant_text'], floor['transaction_id'], sources=[ref['path']],
                            turn_id=ref['turn_id'], tool_item_ids=[x['item_id'] for x in floor.get('tool_outputs', [])],
                            _observed=observed)
        if actual != floor:
            raise LogError('Initial source floor differs from original source')
    receipts = {}
    for path, lines, rows, turns in observed:
        for tid, turn in turns.items():
            if not turn['complete']:
                continue  # Current/interrupted turns are not completed public evidence.
            completed = rows[turn['complete'][-1]-1].get('timestamp')
            if not completed:
                raise LogError('Source completion has no timestamp')
            moment = datetime.fromisoformat(completed.replace('Z', '+00:00'))
            if floor_time is not None and moment <= floor_time:
                continue
            if not turn['finals']:
                raise LogError('Completed turn has no supported public final; record a source gap')
            receipt = cx.capture(thread, turn['finals'][0][2], 'source-' + tid,
                                 sources=[path], turn_id=tid, _observed=observed)
            key = (tid, receipt['source_ref']['message_id'])
            if key in receipts and receipts[key] != receipt:
                raise LogError('Duplicate/ambiguous source across rollouts; reconcile before SAVE')
            receipts[key] = receipt
    ordered = sorted(receipts.values(), key=lambda x: x['source_ref']['completed_at'])
    times = [x['source_ref']['completed_at'] for x in ordered]
    if len(times) != len(set(times)):
        raise LogError('Source ordering is ambiguous')
    return {'receipts': ordered, 'checked_empty': not ordered, 'conversation_id': thread,
            'after': ref, 'through': ordered[-1]['source_ref'] if ordered else ref}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest='command', required=True)
    write = sub.add_parser('append', help='PLAY: append 1–2 sentences only')
    write.add_argument('--text', required=True)
    sub.add_parser('read', help='ADMIN/fresh resume only: uncompiled notes')
    sub.add_parser('export-source', help='SAVE only: original public exchanges')
    args = parser.parse_args(argv)
    try:
        if args.command == 'append':
            result = append(args.root, args.text)
        elif args.command == 'read':
            result = snapshot(args.root)
        else:
            result = export_source(args.root)
        print(json.dumps(result, ensure_ascii=True))
        return 0
    except (ValueError, OSError, KeyError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
