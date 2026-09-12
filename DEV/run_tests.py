#!/usr/bin/env python3
"""Run existing regressions in a disposable developer fixture, not a game install.

The historical tests use the original flat layout. This runner assembles their
actual sources from GAME, DOCS and DEV without changing their game semantics.
The separate distribution tests exercise GAME alone and the actual ZIP builder.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SUITES = ('test_validate', 'test_handover', 'test_package_release',
          'test_read_source', 'test_search_index', 'test_evidence',
          'test_save_audit', 'test_agent_state', 'test_autosave', 'test_encounter_generation')


def run(report_path=None):
    results = []
    with tempfile.TemporaryDirectory(prefix='rpg-os-developer-tests-') as tmp:
        kit = Path(tmp) / 'kit'
        shutil.copytree(ROOT / 'GAME', kit)
        mapping = json.loads((ROOT / 'DEV/legacy_map.json').read_text(encoding='utf-8'))
        for old, current in mapping.items():
            if current.startswith('DOCS/'):
                target = kit / old
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / current, target)
        shutil.copytree(ROOT / 'DEV/TOOLS', kit / 'TOOLS', dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT / '.github', kit / '.github')
        (kit / 'DEV').mkdir()
        shutil.copyfile(__file__, kit / 'DEV/run_tests.py')
        for name in SUITES:
            result = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(kit / 'TOOLS' / (name + '.py'))],
                                    cwd=kit, capture_output=True, text=True, encoding='utf-8',
                                    env=dict(os.environ, PYTHONUTF8='1'))
            output = result.stdout + result.stderr
            counts = re.findall(r'Ran (\d+) tests? in', output)
            skips = re.findall(r'OK \(skipped=(\d+)\)', output)
            row = dict(suite=name, exit_code=result.returncode,
                       cases=int(counts[-1]) if counts else 0,
                       skipped=int(skips[-1]) if skips else 0)
            results.append(row)
            print(json.dumps(row), flush=True)
            if result.returncode or not counts:
                print(output, file=sys.stderr)
    summary = dict(suites=results, cases=sum(r['cases'] for r in results),
                   skipped=sum(r['skipped'] for r in results),
                   failed_suites=sum(r['exit_code'] != 0 or r['cases'] == 0 for r in results),
                   scope='Existing synthetic regressions in an assembled developer fixture; not an LLM playtest.')
    if report_path:
        path = Path(report_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))
    return 1 if summary['failed_suites'] else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report')
    raise SystemExit(run(parser.parse_args().report))
