"""Compact-resume regressions in isolated fixtures; no live source or campaign IO."""
import contextlib
import io
import json
import os
import sys
import unittest
from unittest import mock

import test_persistence_delivery as delivery

persistence = delivery.persistence


class FastResumeTests(unittest.TestCase):
    def setUp(self):
        self.fx = delivery.DeliveryPersistenceTests()
        self.fx.setUp()
        self.addCleanup(self.fx.doCleanups)
        self.root = self.fx.root

    def test_default_api_retains_full_current_body(self):
        result = persistence.resume(self.root)
        self.assertEqual(result['current'], persistence.read_current(self.root, persistence.CURRENT))
        self.assertIsNone(result['confirmation'])
        self.assertEqual(result['journal']['committed_seq'], 0)

    def test_compact_result_has_hashes_and_identity_without_prose(self):
        current = self.root / persistence.CURRENT
        current.write_bytes(current.read_bytes() + ("\nPRIVATE_FIXTURE_BODY " * 1000).encode())
        request, _ = self.fx.commit()
        compact = persistence.resume(self.root, compact=True)
        encoded = json.dumps(compact)
        self.assertNotIn('current', compact)
        self.assertNotIn('records', compact)
        self.assertNotIn('PRIVATE_FIXTURE_BODY', encoded)
        self.assertNotIn(request['response'], encoded)
        self.assertNotIn(request['user_text'], encoded)
        self.assertNotIn('source_ref', encoded)
        self.assertEqual(set(compact['effective_hashes']), {persistence.CURRENT, 'INSTANCE/CHAR/PC.md'})
        self.assertEqual(compact['identity']['conversation_id'], delivery.THREAD)
        self.assertEqual(compact['identity']['base_save_id'], 'fixture-s0001')
        self.assertLess(len(encoded), len(json.dumps(persistence.resume(self.root))) // 10)

    def test_pending_actual_delivery_is_confirmed_before_compact_view(self):
        request = self.fx.request()
        persistence.prepare(self.root, request)
        receipt = self.fx.receipt(request)
        result = persistence.resume(self.root, source=receipt['source_ref']['path'], compact=True)
        self.assertEqual(result['confirmation']['status'], 'committed')
        self.assertEqual(result['journal']['committed_seq'], 1)
        self.assertIsNone(result['journal']['pending'])
        effective = persistence.read_current(self.root, 'INSTANCE/CHAR/PC.md')
        self.assertEqual(result['effective_hashes']['INSTANCE/CHAR/PC.md'], effective['sha256'])

    def test_requested_bodies_and_hashes_use_one_post_confirmation_boundary(self):
        request = self.fx.request()
        request['changes'].append({'path': 'INSTANCE/PEOPLE/new-fixture.md', 'expected_sha256': None,
                                   'content': '# Newly established fixture\n'})
        persistence.prepare(self.root, request)
        receipt = self.fx.receipt(request)
        wanted = ['INSTANCE/CHAR/PC.md', 'INSTANCE/PEOPLE/new-fixture.md', persistence.CURRENT]
        result = persistence.resume(self.root, source=receipt['source_ref']['path'], compact=True, paths=wanted)
        self.assertEqual(set(result['records']), set(wanted))
        for path, value in result['records'].items():
            self.assertEqual(value['committed_seq'], result['journal']['committed_seq'])
            self.assertEqual(value['consolidated_through'], result['journal']['consolidated_through'])
            self.assertEqual(value['sha256'], result['effective_hashes'][path])
        self.assertIn('Cash: 88', result['records']['INSTANCE/CHAR/PC.md']['content'])
        self.assertFalse((self.root / 'INSTANCE/PEOPLE/new-fixture.md').exists())

    def test_view_assembles_once_under_lock_without_public_read_reentry(self):
        original_effective = persistence._effective
        calls = []
        def checked(*args, **kwargs):
            calls.append(True)
            with self.assertRaises(persistence.PersistenceError):
                with persistence._lock(self.root):
                    pass
            return original_effective(*args, **kwargs)
        with mock.patch.object(persistence, '_effective', side_effect=checked), \
                mock.patch.object(persistence, 'read_current', side_effect=AssertionError('public read reentry')), \
                mock.patch.object(persistence, 'status', side_effect=AssertionError('public status reentry')):
            result = persistence.resume(self.root, compact=True, paths=['INSTANCE/CHAR/PC.md', 'INSTANCE/NOW.md'])
        self.assertEqual(len(calls), 1)
        self.assertEqual(len(result['records']), 2)

    def test_missing_and_forbidden_requested_paths_rejected(self):
        for path in ('INSTANCE/PEOPLE/missing.md', 'OS/LAW.md', '../outside.md'):
            with self.subTest(path=path):
                with self.assertRaises(persistence.PersistenceError):
                    persistence.resume(self.root, compact=True, paths=[path])

    def test_pending_case_alias_rejected_before_consolidation(self):
        request = self.fx.request(changes=[{'path': 'INSTANCE/PEOPLE/CaseTest.md',
                                           'expected_sha256': None, 'content': '# Fixture\n'}])
        self.fx.commit(request)
        with self.assertRaises(persistence.PersistenceError):
            persistence.resume(self.root, compact=True, paths=['INSTANCE/PEOPLE/casetest.md'])

    @unittest.skipUnless(os.name == 'nt', 'Existing disk case alias requires Windows')
    def test_disk_case_alias_rejected(self):
        with self.assertRaises(persistence.PersistenceError):
            persistence.resume(self.root, compact=True, paths=['INSTANCE/CHAR/pc.md'])

    def test_interrupted_delivery_remains_pending(self):
        request = self.fx.request()
        persistence.prepare(self.root, request)
        receipt = self.fx.receipt(request)
        source = self.root / (request['transaction_id'] + '.jsonl')
        rows = [json.loads(line) for line in source.read_text().splitlines()]
        rows[-1]['payload']['type'] = 'turn_aborted'
        source.write_text(''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8')
        with self.assertRaises(persistence.PersistenceError):
            persistence.resume(self.root, source=receipt['source_ref']['path'], compact=True)
        self.assertEqual(persistence.status(self.root)['committed_seq'], 0)
        self.assertIsNotNone(persistence.status(self.root)['pending'])

    def run_cli(self, *arguments):
        output = io.StringIO()
        with mock.patch.object(sys, 'argv', ['persistence.py', '--root', str(self.root), 'resume', *arguments]), \
                contextlib.redirect_stdout(output):
            code = persistence.main()
        self.assertEqual(code, 0, output.getvalue())
        return json.loads(output.getvalue())

    def test_cli_defaults_compact_with_explicit_full_override(self):
        compact = self.run_cli()
        self.assertNotIn('current', compact)
        self.assertIn(persistence.CURRENT, compact['effective_hashes'])
        full = self.run_cli('--full')
        self.assertIn('content', full['current'])

    def test_cli_bundles_repeated_paths_in_one_view(self):
        result = self.run_cli('--path', 'INSTANCE/CHAR/PC.md', '--path', 'INSTANCE/NOW.md')
        self.assertNotIn('current', result)
        self.assertEqual(set(result['records']), {'INSTANCE/CHAR/PC.md', 'INSTANCE/NOW.md'})


if __name__ == '__main__':
    unittest.main()
