"""Small guarded edits preserve exact source and avoid regenerating old paragraphs."""
import json
from pathlib import Path
import tempfile
import unittest
import test_persistence as support

p = support.persistence


class SmallEditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='rpg-small-edits-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.fx = support.PersistenceTests()
        self.fx.root = self.root
        self.fx.make_fixture(self.root)
        p.initialize(self.root, 'test-thread')

    def test_metadata_field_preserves_other_bytes(self):
        before = '| datetime | earlier |\r\n| place | unchanged |\r\n'
        self.assertEqual(p._apply_edits(before, [{'field': 'datetime', 'after': 'later'}]),
                         '| datetime | later |\r\n| place | unchanged |\r\n')

    def test_scoped_line_preserves_other_same_named_line(self):
        text = '# Record\n\n## One\n\n- Aim: before\n\n### Detail\nKeep exact.\n\n## Two\n\n- Aim: other\n'
        result = p._apply_edits(text, [{'section': 'One', 'line_prefix': '- Aim: ', 'after': 'after'}])
        self.assertEqual(result, text.replace('- Aim: before', '- Aim: after'))

    def test_append_preserves_neighbor_section_and_nested_heading(self):
        text = '## One\n\nKnown.\n\n### Detail\nKeep.\n\n## Two\n\nOther.\n'
        result = p._apply_edits(text, [{'section': 'One', 'append': '- New established fact.'}])
        self.assertIn('Known.\n- New established fact.\n\n### Detail\nKeep.\n\n## Two\n\nOther.\n', result)
        self.assertTrue(result.startswith('## One\n\nKnown.\n'))

    def test_ambiguous_missing_and_unsafe_selectors_rejected(self):
        cases = [
            ('| datetime | one |\n| datetime | two |\n', {'field': 'datetime', 'after': 'three'}),
            ('| place | one |\n', {'field': 'datetime', 'after': 'three'}),
            ('| place | one |\n', {'field': 'place', 'after': 'bad|value'}),
            ('- Aim: one\n- Aim: two\n', {'line_prefix': '- Aim: ', 'after': 'three'}),
            ('- Aim: one\n', {'line_prefix': '- Aim: ', 'after': 'three\nNew line'}),
            ('## One\nA\n## One\nB\n', {'section': 'One', 'append': 'new'}),
            ('## One\nA\n', {'section': 'Missing', 'append': 'new'}),
            ('Text', {'before': 'Text', 'after': 'New', 'field': 'place'}),
        ]
        for text, edit in cases:
            with self.subTest(edit=edit):
                with self.assertRaises(p.PersistenceError):
                    p._apply_edits(text, [edit])

    def test_prepare_rejects_stale_hash_before_selector(self):
        request = self.fx.request(changes=[{'path': 'INSTANCE/CHAR/PC.md', 'expected_sha256': 'wrong',
                    'edits': [{'line_prefix': 'Cash: ', 'after': '88'}]}])
        before = self.fx.inventory()
        with self.assertRaises(p.PersistenceError):
            p.prepare(self.root, request)
        self.assertEqual(self.fx.inventory(), before)

    def test_save_identity_cannot_be_changed_by_field_selector(self):
        view = p.read_current(self.root, p.CURRENT)
        request = self.fx.request(changes=[{'path': p.CURRENT, 'expected_sha256': view['sha256'],
                    'edits': [{'field': 'save_id', 'after': 'forged'}]}])
        before = self.fx.inventory()
        with self.assertRaises(p.PersistenceError):
            p.prepare(self.root, request)
        self.assertEqual(self.fx.inventory(), before)

    def test_resulting_hash_binds_target_and_retry(self):
        view = p.read_current(self.root, 'INSTANCE/CHAR/PC.md')
        request = self.fx.request(changes=[{'path': view['path'], 'expected_sha256': view['sha256'],
                    'edits': [{'line_prefix': 'Cash: ', 'after': '88'}]}])
        result = p.prepare(self.root, request)
        again = p.prepare(self.root, request)
        self.assertEqual(result['resulting_hashes'], again['resulting_hashes'])
        p.confirm(self.root, self.fx.receipt(request))
        current = p.read_current(self.root, view['path'])
        self.assertEqual(result['resulting_hashes'][view['path']], current['sha256'])
        self.assertEqual(current['content'], view['content'].replace('Cash: 100', 'Cash: 88'))

    def test_close_selectors_preserve_source_and_apply_once(self):
        request = self.fx.commit()
        current = p.read_current(self.root, 'INSTANCE/CHAR/PC.md')
        plan = self.fx.close_plan(current_updates=[{'path': current['path'], 'expected_sha256': current['sha256'],
                         'edits': [{'line_prefix': 'Cash: ', 'after': '86'}]}])
        p.close(self.root, plan)
        p.close(self.root, plan)
        self.assertIn('Cash: 86', p.read_current(self.root, current['path'])['content'])
        archive = (self.root/'ARCHIVE/sessions/fixture-s0003/01_record.md').read_text(encoding='utf-8')
        self.assertIn(request['response'], archive)


if __name__ == '__main__':
    unittest.main()
