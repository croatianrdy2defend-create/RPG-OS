"""ADMIN compilation/source boundaries for write-only PLAY logs; isolated fixtures."""
import json
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

import codex_exchange as cx
import evidence
import play_log as log
from test_codex_exchange import THREAD, NEXT, exchange
import test_persistence as fixtures

p, digest = fixtures.persistence, fixtures.digest


class LogPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='rpg-log-persistence-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.fixture = fixtures.PersistenceTests()
        self.fixture.root = self.root
        self.fixture.make_fixture(self.root)
        self.contract = self.root / p.CONTRACT
        self.contract.write_text('Incremental recording: write-only-log\n', encoding='utf-8')
        self.source = self.root / 'original.jsonl'
        self.rows = [{'type': 'session_meta', 'payload': {'id': THREAD}}, *exchange(text='Prior boundary.')]
        self.rows[-1]['timestamp'] = '2026-09-13T10:00:00.000Z'
        self.write_source()
        self.floor = cx.capture(THREAD, 'Prior boundary.', 'floor', sources=[self.source])
        p.initialize(self.root, THREAD, self.floor)
        self.backend = SimpleNamespace(snapshot=log.snapshot,
            export_source=lambda root: log.export_source(root, sources=[self.source]))
        self.patch = mock.patch.object(p, '_play_log_module', return_value=self.backend)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def write_source(self):
        self.source.write_text(''.join(json.dumps(row) + '\n' for row in self.rows), encoding='utf-8')

    def next_source(self, text='Actual public reply.'):
        self.rows.extend(exchange(NEXT, text))
        self.rows[-1]['timestamp'] = '2026-09-13T10:01:00.000Z'
        self.write_source()

    def plan(self, save='fixture-s0002', **updates):
        snap = log.snapshot(self.root)
        plan = self.fixture.close_plan(save, log_snapshot={k: snap[k] for k in ('after', 'through', 'prefix_sha256')},
                                       log_compilation='reviewed', current_updates=[],
                                       expected_base_save_id=p._fields((self.root/p.CURRENT).read_bytes())['save_id'],
                                       review={'status':'incomplete','scope':'Synthetic storage fixture.',
                                               'limitations':'No semantic source review performed.'})
        plan.update(updates)
        return plan

    def cash_update(self):
        path = 'INSTANCE/CHAR/PC.md'
        return {'path': path, 'expected_sha256': digest((self.root/path).read_bytes()),
                'edits': [{'before': 'Cash: 100', 'after': 'Cash: 88'}]}

    def test_adoption_literal_alone_selects_v2_and_blocks_per_turn_protocol(self):
        head = json.loads((self.root/p.HEAD).read_bytes())
        self.assertEqual((head['schema'], head['recording'], head['mode']),
                         ('rpg-journal-v2', 'write-only-log', 'write-only-log'))
        for callback in (lambda: p.prepare(self.root, {}), lambda: p.note(self.root, {}),
                         lambda: p.resume(self.root), lambda: p.confirm(self.root, {})):
            with self.assertRaises(p.PersistenceError):
                callback()

    def test_notes_require_explicit_ack_snapshot_and_expected_head(self):
        log.append(self.root, 'A purchase cost 12.')
        before = (self.root/p.CURRENT).read_bytes()
        with self.assertRaises(p.PersistenceError):
            p.checkpoint(self.root, 'fixture-s0002')
        for missing in ('log_compilation', 'log_snapshot', 'expected_base_save_id'):
            plan = self.plan()
            del plan[missing]
            with self.assertRaises(p.PersistenceError, msg=missing):
                p.checkpoint(self.root, plan['save_id'], plan)
        self.assertEqual(before, (self.root/p.CURRENT).read_bytes())

    def test_stale_snapshot_rejects_without_owner_writes(self):
        log.append(self.root, 'One fact.')
        plan = self.plan(current_updates=[self.cash_update()])
        log.append(self.root, 'A second fact.')
        with self.assertRaises(p.PersistenceError):
            p.checkpoint(self.root, plan['save_id'], plan)
        self.assertIn('Cash: 100', (self.root/'INSTANCE/CHAR/PC.md').read_text())

    def test_checkpoint_compiles_once_and_retains_archive_boundary(self):
        log.append(self.root, 'A purchase cost 12.')
        raw = (self.root/log.LOG).read_bytes()
        plan = self.plan(current_updates=[self.cash_update()])
        result = p.checkpoint(self.root, plan['save_id'], plan)
        self.assertEqual(result['status'], 'checkpoint-published')
        self.assertEqual(log.snapshot(self.root)['note_count'], 0)
        self.assertIn('Cash: 88', (self.root/'INSTANCE/CHAR/PC.md').read_text())
        self.assertEqual(raw, (self.root/log.LOG).read_bytes())
        fields = p._fields((self.root/p.CURRENT).read_bytes())
        self.assertEqual(fields.get('play_log_archive_through', '0'), '0')
        self.assertEqual(fields['evidence_through'], 'fixture-s0001')
        self.assertEqual(p.checkpoint(self.root, plan['save_id'], plan)['status'], 'already-published')
        log.append(self.root, 'Further progress.')
        with self.assertRaises(p.PersistenceError):
            p.checkpoint(self.root, plan['save_id'], plan)

    def test_admin_read_labels_compiled_baseline_and_notes(self):
        log.append(self.root, 'Established addition.')
        result = p.read_current(self.root, p.CURRENT)
        self.assertIn('compiled-record baseline', result['view'])
        self.assertTrue(result['compilation_required'])
        self.assertEqual(result['uncompiled_log'][0]['text'], 'Established addition.')

    def test_no_state_notes_can_be_explicitly_reviewed(self):
        log.append(self.root, 'The conversation continued without a durable change.')
        plan = self.plan()
        p.checkpoint(self.root, plan['save_id'], plan)
        self.assertEqual(log.snapshot(self.root)['note_count'], 0)

    def test_close_compiles_once_and_auto_archives_only_actual_source(self):
        log.append(self.root, 'PRIVATE_LOG_SENTINEL: a consequence is established.')
        self.next_source('Exact public reply.\nLine two.')
        plan = self.plan(current_updates=[self.cash_update()])
        result = p.close(self.root, plan)
        self.assertEqual(result['archived_exchanges'], 1)
        body = (self.root/'ARCHIVE/sessions/fixture-s0002/01_record.md').read_text(encoding='utf-8')
        self.assertIn('Exact public reply.\nLine two.', body)
        self.assertIn('I buy lunch.', body)
        self.assertNotIn('PRIVATE_LOG_SENTINEL', body)
        self.assertNotIn('PRIVATE_REASONING_SENTINEL', body)
        self.assertIn('possible OOC', body)
        self.assertIn('Cash: 88', (self.root/'INSTANCE/CHAR/PC.md').read_text())
        fields = p._fields((self.root/p.CURRENT).read_bytes())
        self.assertEqual(fields['play_log_through'], fields['play_log_archive_through'])
        self.assertEqual(p.close(self.root, plan)['status'], 'already-published')
        second = self.plan('fixture-s0003')
        self.assertEqual(p.close(self.root, second)['archived_exchanges'], 0)

    def test_explicit_empty_or_omitted_public_source_cannot_hide_available_source(self):
        self.next_source()
        with self.assertRaises(p.PersistenceError):
            p.close(self.root, self.plan(public_source_receipts=[]))
        self.assertFalse((self.root/'ARCHIVE/sessions/fixture-s0002/01_record.md').exists())

    def test_explicit_source_boundary_repetition_is_rejected(self):
        with self.assertRaises(p.PersistenceError):
            p.close(self.root, self.plan(public_source_receipts=[self.floor]))

    def test_altered_original_source_refuses_publication(self):
        self.next_source()
        receipt = log.export_source(self.root, sources=[self.source])['receipts'][0]
        receipt['assistant_text'] = 'fabricated'
        with self.assertRaises(p.PersistenceError):
            p.close(self.root, self.plan(public_source_receipts=[receipt]))

    def test_source_gap_is_honest_and_cannot_claim_complete_review(self):
        self.backend.export_source = mock.Mock(side_effect=ValueError('Original unavailable'))
        with self.assertRaises(p.PersistenceError):
            p.close(self.root, self.plan())
        with self.assertRaises(p.PersistenceError):
            p.close(self.root, self.plan(source_gap='Original unavailable.', review={
                'status':'complete','scope':'Synthetic source review.','limitations':'Original unavailable.'}))
        plan = self.plan(source_gap='Original unavailable.', review={
            'status': 'incomplete', 'scope': 'Changed records only.', 'limitations': 'Original source unavailable.'})
        result = p.close(self.root, plan)
        self.assertEqual(result['review_status'], 'incomplete')
        review = json.loads((self.root/'EVIDENCE/incremental-reviews/fixture-s0002.json').read_bytes())
        self.assertFalse(review['public_source_coverage']['checked_export'])
        self.assertEqual(review['public_source_coverage']['source_gap'], 'Original unavailable.')

    def test_immutable_cursor_cannot_be_faked_in_owner_update(self):
        log.append(self.root, 'One fact.')
        raw = (self.root/p.CURRENT).read_bytes()
        change = {'path':p.CURRENT, 'expected_sha256':digest(raw), 'edits':[{
            'before':'| save_id | fixture-s0001 |',
            'after':'| save_id | fixture-s0001 |\n| play_log_through | 999 |'}]}
        with self.assertRaises(p.PersistenceError):
            p.checkpoint(self.root, 'fixture-s0002', self.plan(current_updates=[change]))

    def test_interrupted_publication_restore_does_not_consume_notes(self):
        log.append(self.root, 'A purchase cost 12.')
        plan = self.plan(current_updates=[self.cash_update()])
        original = p._publish_write
        writes = 0
        def interrupted(path, data):
            nonlocal writes
            writes += 1
            if writes == 2:
                raise OSError('Synthetic interruption')
            return original(path, data)
        with mock.patch.object(p, '_publish_write', side_effect=interrupted):
            with self.assertRaises(OSError):
                p.checkpoint(self.root, plan['save_id'], plan)
        p.recover(self.root, 'restore')
        self.assertEqual(log.snapshot(self.root)['note_count'], 1)
        self.assertIn('Cash: 100', (self.root/'INSTANCE/CHAR/PC.md').read_text())

    def test_checkpoint_cli_plan_supplies_save_id(self):
        log.append(self.root, 'An established event.')
        plan = self.root/'plan.json'
        plan.write_text(json.dumps(self.plan()), encoding='utf-8')
        result = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(Path(p.__file__).resolve()),
                                 '--root', str(self.root), 'checkpoint', '--plan', str(plan)],
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(log.snapshot(self.root)['note_count'], 0)

    def test_old_compilation_origin_cannot_be_reused(self):
        log.append(self.root, 'A purchase cost 12.')
        stale = self.plan('fixture-s0003', current_updates=[self.cash_update()])
        p.checkpoint(self.root, 'fixture-s0002', self.plan())
        with self.assertRaises(p.PersistenceError):
            p.checkpoint(self.root, 'fixture-s0003', stale)
        stale['expected_base_save_id'] = 'fixture-s0002'
        with self.assertRaises(p.PersistenceError):  # Same prefix, different consumed origin.
            p.checkpoint(self.root, 'fixture-s0003', stale)

    def reviewed_plan(self, prior_selected=()):
        """Existing evidence workflow with synthetic declared judgments, not a model test."""
        support = tempfile.TemporaryDirectory(prefix='rpg-review-support-')
        self.addCleanup(support.cleanup)
        support = Path(support.name)
        plan = self.plan(current_updates=[self.cash_update()], review={
            'status':'complete', 'scope':'All changed owners and the available interval.',
            'limitations':'Synthetic declared judgment; semantic understanding is not tested.'})
        result = p.close(self.root, plan, support/'proposal')
        source = support/'proposal'/result['source']
        capture = evidence.import_capture(source, support/'capture')
        stop = {'basis':'capture_lines', 'capture_sha256':digest(source.read_bytes()), 'start_line':1,
                'end_line':len(source.read_bytes().decode('utf-8').splitlines(keepends=True)),
                'description':'All actual available source through the selected stop.'}
        boundary = {'schema':evidence.SAVE_BOUNDARY_SCHEMA,'state_saved_through':stop,
                    'write_paths':result['affected_owners'],'removed_paths':[],
                    'limitations':['Only selected owners and available original source.']}
        (support/'boundary.json').write_bytes(evidence.json_bytes(boundary))
        evidence.prepare_save_audit(self.root, support/'proposal', support/'capture', support/'bundle',
                                    support/'boundary.json', selected=[x for x in result['affected_owners'] if x != p.CURRENT],
                                    prior_selected=prior_selected)
        report = evidence.report_template(support/'bundle')
        refs = report['source_coverage']['indexed_sources']
        report['review_status'] = 'completed'
        report['reviewer'] = {'kind':'model','identifier':'synthetic-declaration-not-a-real-review',
                              'independence':'same_context'}
        report['source_coverage'].update(status='scoped', reviewed_sources=refs)
        citations = []
        for ref in refs:
            prefix = 'capture' if ref['source'] == 'capture' else 'sources/' + ref['source']
            first = (support/'bundle'/prefix/ref['path']).read_bytes().decode('utf-8').splitlines(keepends=True)[0]
            citations.append({**ref,'start_line':1,'end_line':1,'quote':first})
        report['record_consistency'] = {'status':'consistent','summary':'Synthetic declared consistency.',
                                         'citations':citations}
        report['save_review']['review_covered_through'] = stop
        report['save_review']['source_coherence'] = {'status':'no_conflict_observed',
            'summary':'Synthetic declared judgment only.','citations':[]}
        (support/'report.json').write_bytes(evidence.json_bytes(report))
        retained = self.root/'EVIDENCE/reviews'/plan['save_id']
        retained.mkdir(parents=True)
        shutil.copytree(support/'bundle', retained/'bundle')
        shutil.copyfile(support/'report.json', retained/'report.json')
        plan['review']['receipt'] = {'bundle':(retained/'bundle').relative_to(self.root).as_posix(),
                                     'report':(retained/'report.json').relative_to(self.root).as_posix(),
                                     'report_sha256':digest((retained/'report.json').read_bytes())}
        return plan, support

    def test_complete_close_checks_existing_review_against_exact_proposal(self):
        log.append(self.root, 'A purchase cost 12; 88 remains.')
        self.next_source('The purchase completes; 88 remains.')
        plan, support = self.reviewed_plan()
        before = (support/'proposal'/p.CURRENT).read_bytes()
        result = p.close(self.root, plan)
        self.assertEqual(result['review_status'], 'complete')
        self.assertEqual(before, (self.root/p.CURRENT).read_bytes())

    def test_changed_unchanged_review_dependency_rejects_publication(self):
        dependency = self.root/'INSTANCE/KNOWN.md'
        dependency.write_text('# Known\n\nThe payment is conditional.\n', encoding='utf-8')
        self.next_source('The purchase completes; 88 remains.')
        plan, _ = self.reviewed_plan(prior_selected=['INSTANCE/KNOWN.md'])
        dependency.write_text('# Known\n\nThe condition was waived.\n', encoding='utf-8')
        with self.assertRaisesRegex(p.PersistenceError, 'prior review dependency changed'):
            p.close(self.root, plan)
        self.assertFalse((self.root/p.ACTIVE).exists())

    def test_empty_or_unbound_complete_review_is_rejected(self):
        for review in ({'status':'complete','scope':'','limitations':''},
                       {'status':'complete','scope':'Claimed scope.','limitations':'No reference.'}):
            with self.assertRaises(p.PersistenceError):
                p.close(self.root, self.plan(review=review))

    def test_changed_proposal_or_report_invalidates_complete_review(self):
        self.next_source()
        plan, support = self.reviewed_plan()
        plan['current_updates'][0]['edits'][0]['after'] = 'Cash: 87'
        with self.assertRaises(p.PersistenceError):
            p.close(self.root, plan)
        plan['current_updates'][0]['edits'][0]['after'] = 'Cash: 88'
        report = self.root/plan['review']['receipt']['report']
        report.write_bytes(report.read_bytes() + b'\n')
        with self.assertRaises(p.PersistenceError):
            p.close(self.root, plan)
        self.assertFalse((self.root/p.ACTIVE).exists())

    def test_saved_floor_survives_loss_of_old_host_file(self):
        self.next_source()
        p.close(self.root, self.plan())
        self.source.rename(self.source.with_suffix('.moved'))
        self.assertTrue(log.export_source(self.root, sources=[])['checked_empty'])
        archive = self.root/'ARCHIVE/sessions/fixture-s0002/01_record.md'
        archive.write_bytes(archive.read_bytes() + b'changed')
        with self.assertRaises(ValueError):
            log.export_source(self.root, sources=[])

    def test_rebind_archives_old_source_then_starts_new_conversation(self):
        self.next_source()
        with self.assertRaises(p.PersistenceError):
            p.rebind(self.root, NEXT, 'fixture-s0001')
        p.close(self.root, self.plan())
        p.rebind(self.root, NEXT, 'fixture-s0002')
        head = json.loads((self.root/p.HEAD).read_bytes())
        self.assertIsNone(head['public_source_floor'])
        self.assertEqual(head['public_source_origin'], 'conversation-start')
        self.assertTrue(log.export_source(self.root, sources=[])['checked_empty'])

    def test_public_correction_annotation_retains_exact_original(self):
        self.next_source('An original mistaken claim.')
        message = log.export_source(self.root, sources=[self.source])['receipts'][0]['source_ref']['message_id']
        (self.root/'INSTANCE/CORRECTIONS.md').write_text('## C-test\nThe corrected established fact.\n')
        plan = self.plan(source_dispositions={message:{'status':'superseded','reason':'Accepted correction.',
            'correction_ref':'INSTANCE/CORRECTIONS.md#C-test'}})
        p.close(self.root, plan)
        text = (self.root/'ARCHIVE/sessions/fixture-s0002/01_record.md').read_text(encoding='utf-8')
        self.assertIn('An original mistaken claim.', text)
        self.assertIn('INSTANCE/CORRECTIONS.md#C-test', text)
        self.assertIn('not reinstated fiction', text)

    def test_correction_reference_requires_unique_heading_and_partial_spans(self):
        self.next_source('Wrong time; unrelated accepted dialogue.')
        message = log.export_source(self.root, sources=[self.source])['receipts'][0]['source_ref']['message_id']
        register = self.root/'INSTANCE/CORRECTIONS.md'
        disposition = {'status':'partly-superseded','reason':'Only time is corrected.',
                       'correction_ref':'INSTANCE/CORRECTIONS.md#C-test'}
        for text in ('C-test merely mentioned in prose.\n', '## C-test\nA\n## C-test\nB\n', '## C-test\nA\n'):
            register.write_text(text)
            with self.assertRaises(p.PersistenceError):
                p.close(self.root, self.plan(source_dispositions={message:disposition}))
        disposition['spans'] = [{'role':'assistant','start':0,'end':10}]
        p.close(self.root, self.plan(source_dispositions={message:disposition}))
        text = (self.root/'ARCHIVE/sessions/fixture-s0002/01_record.md').read_text(encoding='utf-8')
        self.assertIn('Wrong time; unrelated accepted dialogue.', text)

    def test_complete_close_recovery_finishes_exact_reviewed_bytes(self):
        log.append(self.root, 'The purchase cost 12.')
        self.next_source()
        plan, support = self.reviewed_plan()
        original = p._publish_write
        calls = 0
        def interrupted(path, data):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError('Synthetic interrupted publication')
            return original(path, data)
        with mock.patch.object(p, '_publish_write', side_effect=interrupted):
            with self.assertRaises(OSError):
                p.close(self.root, plan)
        p.recover(self.root, 'finish')
        self.assertEqual((support/'proposal'/p.CURRENT).read_bytes(), (self.root/p.CURRENT).read_bytes())
        self.assertEqual(log.snapshot(self.root)['note_count'], 0)
        self.assertTrue(log.export_source(self.root, sources=[])['checked_empty'])

    def test_copied_complete_save_rebinds_without_old_host_and_exports_new_turn(self):
        self.next_source()
        plan, support = self.reviewed_plan()
        p.close(self.root, plan)
        restored = support/'restored'
        shutil.copytree(self.root, restored)
        self.source.rename(self.source.with_suffix('.moved'))
        self.assertTrue(log.export_source(restored, sources=[])['checked_empty'])
        result = p.rebind(restored, NEXT, 'fixture-s0002')
        self.assertIn('not checked', result['source_limit'])
        rows = [{'type':'session_meta','payload':{'id':NEXT}},
                *exchange('44444444-4444-4444-8444-444444444444', 'New conversation, actual public reply.')]
        for row in rows:
            if row['payload'].get('type') == 'item_completed':
                row['payload']['thread_id'] = NEXT
        rows[-1]['timestamp'] = '2026-09-13T11:00:00.000Z'
        source = restored/'new.jsonl'
        source.write_text(''.join(json.dumps(row)+'\n' for row in rows), encoding='utf-8')
        self.backend.export_source = lambda root: log.export_source(root, sources=[source])
        self.root = restored
        log.append(restored, 'A new conversation began.')
        result = p.close(restored, self.plan('fixture-s0003'))
        self.assertEqual(result['archived_public_messages'], 1)
        archive = (restored/'ARCHIVE/sessions/fixture-s0003/01_record.md').read_text(encoding='utf-8')
        self.assertIn('New conversation, actual public reply.', archive)
        self.assertNotIn('Actual public reply.', archive)

    def test_fresh_bind_can_select_actual_play_conversation_before_any_play(self):
        head = json.loads((self.root/p.HEAD).read_bytes())
        head.update(public_source_floor=None, source_floor=None, public_source_origin='conversation-start')
        (self.root/p.HEAD).write_bytes(p._json(head))
        (self.root/p.CURRENT).write_bytes(p._set_field((self.root/p.CURRENT).read_bytes(), 'commit_kind', 'bind'))
        with mock.patch.object(self.backend, 'export_source', side_effect=AssertionError('No played source to archive')):
            p.rebind(self.root, NEXT, 'fixture-s0001')
        self.assertEqual(json.loads((self.root/p.HEAD).read_bytes())['conversation_id'], NEXT)


if __name__ == '__main__':
    unittest.main()
