"""Write-only PLAY path and SAVE-only source collection; synthetic fixtures."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import play_log as log
import codex_exchange as cx
from test_codex_exchange import THREAD, TURN, NEXT, exchange


class LogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'INSTANCE').mkdir()
        self.current = self.root/'INSTANCE/CURRENT_SAVE.md'
        self.current.write_text('| save_id | test-s1 |\n', encoding='utf-8')

    def test_append_never_reads_or_hashes_campaign(self):
        self.current.write_text('deliberately malformed current data', encoding='utf-8')
        original_open, original_write = os.open, os.write
        with mock.patch.object(Path, 'read_bytes', side_effect=AssertionError('read')), \
             mock.patch.object(Path, 'read_text', side_effect=AssertionError('read')), \
             mock.patch.object(Path, 'open', side_effect=AssertionError('read')), \
             mock.patch.object(Path, 'exists', side_effect=AssertionError('check')), \
             mock.patch.object(Path, 'stat', side_effect=AssertionError('check')), \
             mock.patch.object(hashlib, 'sha256', side_effect=AssertionError('hash')), \
             mock.patch.object(os, 'read', side_effect=AssertionError('read')), \
             mock.patch.object(os, 'open', wraps=original_open) as opened, \
             mock.patch.object(os, 'write', wraps=original_write) as written:
            result = log.append(self.root, 'A brief conversation continued.')
        self.assertEqual(opened.call_count, 1)
        self.assertEqual(written.call_count, 1)
        self.assertTrue(opened.call_args.args[1] & os.O_APPEND)
        self.assertEqual(opened.call_args.args[1] & (os.O_RDONLY | os.O_RDWR), 0)
        self.assertEqual(set(result), {'logged'})

    def test_append_preserves_bytes_and_encodes_one_line(self):
        log.append(self.root, 'A purchase cost €2.00.')
        path = self.root/log.LOG
        before = path.read_bytes()
        log.append(self.root, 'A name was exchanged.\nAn invitation remained open.')
        data = path.read_bytes()
        self.assertTrue(data.startswith(before))
        self.assertEqual(len(data.splitlines()), 2)
        self.assertEqual(log.snapshot(self.root)['note_count'], 2)

    def test_partial_write_reports_without_retry(self):
        with mock.patch.object(os, 'write', return_value=2) as write:
            with self.assertRaises(OSError):
                log.append(self.root, 'A short note.')
        self.assertEqual(write.call_count, 1)

    def test_checkpoint_cursor_excludes_compiled_notes(self):
        log.append(self.root, 'An agreement was made.')
        snap = log.snapshot(self.root)
        self.current.write_text(f'| play_log_through | {snap["through"]} |\n'
                                f'| play_log_prefix_sha256 | {snap["prefix_sha256"]} |\n')
        log.append(self.root, 'The visitor left.')
        self.assertEqual([x['text'] for x in log.snapshot(self.root)['entries']], ['The visitor left.'])

    def test_compiled_prefix_edit_is_detected_at_admin_read(self):
        log.append(self.root, 'An agreement was made.')
        snap = log.snapshot(self.root)
        self.current.write_text(f'| play_log_through | {snap["through"]} |\n'
                                f'| play_log_prefix_sha256 | {snap["prefix_sha256"]} |\n')
        path = self.root/log.LOG
        path.write_bytes(path.read_bytes().replace(b'agreement', b'different'))
        with self.assertRaises(log.LogError):
            log.snapshot(self.root)

    def test_partial_tail_is_detected_only_when_read(self):
        (self.root/log.LOG).write_bytes(b'{"id":')
        log.append(self.root, 'A second note does not repair a partial write.')
        with self.assertRaises(log.LogError):
            log.snapshot(self.root)

    def test_empty_log(self):
        self.assertEqual(log.snapshot(self.root)['note_count'], 0)
        with self.assertRaises(log.LogError):
            log.append(self.root, ' ')


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'INSTANCE/JOURNAL').mkdir(parents=True)
        self.source = self.root/'original.jsonl'
        self.rows = [{'type':'session_meta','payload':{'id':THREAD}}, *exchange(text='Saved.')]
        self.rows[-1]['timestamp'] = '2026-09-13T10:00:00.000Z'
        self.write()
        self.floor = cx.capture(THREAD, 'Saved.', 'floor', sources=[self.source])
        (self.root/'INSTANCE/JOURNAL/HEAD.json').write_text(json.dumps({
            'conversation_id':THREAD, 'public_source_floor':self.floor}))

    def write(self):
        self.source.write_text(''.join(json.dumps(r)+'\n' for r in self.rows), encoding='utf-8')

    def test_export_preserves_actual_dialogue_and_excludes_private_items(self):
        self.rows.extend(exchange(NEXT, 'Public reply.'))
        self.rows[-1]['timestamp'] = '2026-09-13T10:01:00.000Z'
        self.write()
        result = log.export_source(self.root, sources=[self.source])
        self.assertEqual(len(result['receipts']), 1)
        receipt = result['receipts'][0]
        self.assertEqual(receipt['assistant_text'], 'Public reply.')
        self.assertEqual(receipt['user_messages'][0]['text'], 'I buy lunch.')
        self.assertNotIn('PRIVATE_REASONING_SENTINEL', json.dumps(result))
        self.assertNotIn('SECRET_ARGS', json.dumps(result))
        self.assertTrue(cx.verify_receipt(receipt))

    def test_checked_empty_requires_original_floor(self):
        self.assertTrue(log.export_source(self.root, sources=[self.source])['checked_empty'])
        self.rows[-2]['payload']['item']['content'][0]['text'] = 'tampered'
        self.write()
        with self.assertRaises(ValueError):
            log.export_source(self.root, sources=[self.source])

    def test_next_export_does_not_repeat_prior_source(self):
        self.rows.extend(exchange(NEXT, 'Public reply.'))
        self.rows[-1]['timestamp'] = '2026-09-13T10:01:00.000Z'
        self.write()
        receipt = log.export_source(self.root, sources=[self.source])['receipts'][0]
        (self.root/'INSTANCE/JOURNAL/HEAD.json').write_text(json.dumps({
            'conversation_id':THREAD, 'public_source_floor':receipt}))
        self.assertTrue(log.export_source(self.root, sources=[self.source])['checked_empty'])

    def test_export_reads_and_scans_each_source_once(self):
        self.rows.extend(exchange(NEXT, 'Public reply.'))
        self.rows[-1]['timestamp'] = '2026-09-13T10:01:00.000Z'
        self.write()
        with mock.patch.object(cx, '_snapshot', wraps=cx._snapshot) as snapshots, \
             mock.patch.object(cx, '_scan', wraps=cx._scan) as scans:
            result = log.export_source(self.root, sources=[self.source])
        self.assertEqual(len(result['receipts']), 1)
        self.assertEqual(snapshots.call_count, 1)
        self.assertEqual(scans.call_count, 1)


if __name__ == '__main__':
    unittest.main()
