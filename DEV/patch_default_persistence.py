#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent

def replace(path, old, new, count=1):
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f'{path}: expected {count} occurrence(s), found {actual}: {old[:80]!r}')
    p.write_text(text.replace(old, new, count), encoding='utf-8')

# Versioned runtime headers.
replace('GAME/VERSION', '0.9.7\n', '0.9.8\n')
for path, old, new in [
    ('GAME/OS/AGENTS.md', '# RPG OS v0.9.7 entry point', '# RPG OS v0.9.8 entry point'),
    ('GAME/OS/BOOTSTRAP.md', '# RPG OS v0.9.7 startup', '# RPG OS v0.9.8 startup'),
    ('GAME/OS/LAW.md', '# RPG OS v0.9.7 GM core', '# RPG OS v0.9.8 GM core'),
    ('GAME/ADMIN/AUTOSAVE.md', '# ADMIN — Optional announced autosave (v0.9.7)', '# ADMIN — Standard announced checkpointing (v0.9.8)'),
    ('GAME/QUICKSTART.md', '# Quick start — v0.9.7 experimental', '# Quick start — v0.9.8 experimental'),
    ('GAME/INSTALLATION.md', '# Installation and portability — v0.9.7 experimental', '# Installation and portability — v0.9.8 experimental'),
]:
    replace(path, old, new)

# New-campaign default persistence profile.
replace(
    'GAME/ADMIN/AUTOSAVE.md',
    'PLAY changes no canonical files between saves; a separately selected write-only log permits only its short append.\n\nAutosave is off unless explicitly accepted in the campaign agreement. It invokes the protected complete-present ADMIN CHECKPOINT, not a background service or general PLAY write grant. The separately selected [write-only play log](PLAY_PERSISTENCE.md) performs one short append without persistence reads or checking. Autosave alone does not enable that log. Installation enables neither policy.',
    'PLAY changes no canonical files between saves; the standard new-campaign persistence profile selects the [write-only play log](PLAY_PERSISTENCE.md), which permits only one short append after each completed PLAY reply.\n\nFor new v0.9.8 campaigns, setup proposes announced checkpointing and the write-only play log by default. Accepting the compact campaign proposal selects both unless the operator declines or customizes them. Existing bound campaigns keep their previously accepted persistence policy; absence of an autosave grant in a legacy agreement remains off. Announced checkpointing invokes the protected complete-present ADMIN CHECKPOINT, not a background service or general PLAY write grant. The log performs one short append without persistence reads or checking. Either default may be disabled prospectively through setup or RECALIBRATE.'
)
replace(
    'GAME/ADMIN/AUTOSAVE.md',
    '> Autosave: Enabled under ADMIN/AUTOSAVE.md. Warn one response before automatically invoking a protected complete-present CHECKPOINT when consequential unsaved state or a substantial scene boundary makes it useful, after 15 completed PLAY replies since verified persistence, or at a supported context reading of 65% or more. Coalesce triggers; do not save an unchanged present or repeatedly trigger on an already handled high-context episode. The operator may defer, disable or save immediately. Preserve PC decisions, fictional time and the archive evidence boundary.',
    '> Autosave: Enabled under ADMIN/AUTOSAVE.md. Warn one response before automatically invoking a protected complete-present CHECKPOINT after 20 completed PLAY replies since verified persistence. Consequential-state, substantial-scene-boundary, or supported context-pressure triggers are optional early triggers only when separately accepted for this campaign. Do not save an unchanged present. The operator may defer, disable or save immediately. Preserve PC decisions, fictional time and the archive evidence boundary.'
)
replace('GAME/ADMIN/AUTOSAVE.md', '- Cadence: 15 completed PLAY replies since bind/verified persistence.', '- Cadence: 20 completed PLAY replies since bind/verified persistence.')
replace(
    'GAME/ADMIN/AUTOSAVE.md',
    'With unsaved state, any selected trigger may schedule one checkpoint:',
    'With unsaved state, the standard new-campaign profile schedules on the 20-reply cadence. A campaign may separately accept any of the early triggers below; if selected, they can schedule a checkpoint before cadence:'
)
replace(
    'GAME/ADMIN/AUTOSAVE.md',
    'Example: `echo \'{"enabled":true,"dirty":true,"turn":15,"turns_since_save":15}\' | python -B TOOLS/autosave.py` returns `warn`. At that same turn with `warned_at:15`, it returns `wait`; with `turn:16`, it requests `checkpoint`.',
    'Example: `echo \'{"enabled":true,"dirty":true,"turn":20,"turns_since_save":20}\' | python -B TOOLS/autosave.py` returns `warn`. At that same turn with `warned_at:20`, it returns `wait`; with `turn:21`, it requests `checkpoint`.'
)

replace(
    'GAME/ADMIN/PLAY_PERSISTENCE.md',
    'Use only when the agreement selects `Incremental recording: write-only-log`. Continue from working conversation; do not inspect persistence files each turn.',
    'New v0.9.8 campaigns select `Incremental recording: write-only-log` by default unless the operator declines or customizes it in the campaign proposal. Existing bound campaigns use it only when their agreement selects it. Continue from working conversation; do not inspect persistence files each turn.'
)
replace(
    'GAME/ADMIN/PLAY_PERSISTENCE.md',
    'After resolving the declaration, append **one or two concise sentences** describing what actually happened:',
    'After each completed PLAY response, once the declaration is resolved, append **one or two concise sentences** describing what actually happened:'
)
replace(
    'GAME/ADMIN/PLAY_PERSISTENCE.md',
    'The short log supports those operations; it is neither a complete transcript nor a verified full save. Installation alone enables nothing.',
    'The short log supports those operations; it is neither a complete transcript nor a verified full save. A new campaign proposes it by default; installing v0.9.8 over an existing campaign does not silently change that campaign\'s accepted policy.'
)

replace(
    'GAME/ADMIN/NEW_GAME.md',
    'Explain saving in the compact proposal. Default protected saves and any accepted autosave/review policies remain. If requested, propose the [write-only play log](PLAY_PERSISTENCE.md): one or two outcome sentences appended each turn, ADMIN compilation at the accepted checkpoint cadence, and source archiving/selected review at full SAVE. It adds no routine file checking or delivery protocol; notes are working material, not a full transcript. Record `Incremental recording: write-only-log` in the same accepted agreement and use the actual compatible host setup after bind. No extra interview or automatic world-generation setting is required.',
    'Explain saving in the compact proposal. For a new campaign, propose the standard persistence profile by default unless the operator declines or customizes it: `Incremental recording: write-only-log`, one or two outcome sentences appended after each completed PLAY response, and announced CHECKPOINTs on a 20-completed-PLAY-reply cadence under `ADMIN/AUTOSAVE.md`. ADMIN compilation happens at checkpoint; full SAVE archives remaining available source and performs the selected bounded review. These defaults add no routine file checking or delivery protocol, and notes remain working material rather than a full transcript. Record the selected log and autosave policy in the same accepted agreement and use the actual compatible host setup after bind. Existing campaigns are not retrofitted merely by installing v0.9.8. No extra interview or automatic world-generation setting is required.'
)

# Scheduler defaults reflect the fresh-campaign profile; callers still override from the bound agreement.
replace('GAME/TOOLS/autosave.py', "\"\"\"Read-only reference scheduler for RPG OS's opt-in autosave protocol.", "\"\"\"Read-only reference scheduler for RPG OS's standard announced checkpoint protocol.")
replace('GAME/TOOLS/autosave.py', '    enabled: bool = False', '    enabled: bool = True')
replace('GAME/TOOLS/autosave.py', '    interval: int = 15', '    interval: int = 20')
replace('GAME/TOOLS/autosave.py', '    # This must come from the accepted agreement, never from a suggested policy.', '    # Fresh v0.9.8 campaigns accept this by default; bound/legacy campaigns override from their agreement.')

# Bootstrap keeps explicit campaign authority: new setup writes the defaults; legacy absence remains off.
replace(
    'GAME/OS/BOOTSTRAP.md',
    '8. Only if the accepted agreement explicitly enables autosave, follow `ADMIN/AUTOSAVE.md` for its cadence and advance notice. Absent policy means off, not a missing required field.',
    '8. Follow the persistence policy actually recorded in the accepted agreement. New v0.9.8 campaigns normally record the standard write-only log plus announced 20-reply checkpoint cadence during setup unless the operator declined or customized them. Existing/legacy campaigns with no autosave grant remain off; absence is not a missing required field.'
)

# Player-facing guides.
replace(
    'GAME/QUICKSTART.md',
    'An opt-in [write-only play log](ADMIN/PLAY_PERSISTENCE.md) appends one or two outcome sentences per exchange without routine persistence checks. Fresh boot reads compiled state and uncompiled notes once; checkpoints compile changes at the accepted cadence, and full SAVE preserves remaining source and selected review. Keep complete backups. Installation enables no policy.',
    'New campaigns default to a [write-only play log](ADMIN/PLAY_PERSISTENCE.md) that appends one or two outcome sentences after each completed PLAY response, plus announced CHECKPOINTs every 20 completed PLAY replies. Fresh boot reads compiled state and uncompiled notes once; checkpoints compile changes, and full SAVE preserves remaining source and selected review. Keep complete backups. You can disable or customize either persistence default during setup or later through recalibration.'
)
replace('GAME/QUICKSTART.md', '## Optional announced autosave', '## Standard persistence defaults')
replace(
    'GAME/QUICKSTART.md',
    'Say: “Enable the standard announced autosave policy in ADMIN/AUTOSAVE.md for this campaign.” The GM records the accepted policy through setup or recalibration; installation alone leaves it off.\n\nThe standard policy warns after consequential unsaved state or substantial scene boundaries, after 15 completed PLAY replies, or at a supported context reading of at least 65%. The meter must actually be accessible or reported by you. One generic warning precedes a checkpoint after the next completed play turn. Several triggers coalesce; nothing runs unattended. “Checkpoint now,” “save now,” “delay autosave,” “resume autosave” and “disable autosave” remain available.',
    'For a new campaign, the compact setup proposal includes the short write-only log and announced checkpointing by default. The log adds one or two concise factual outcome sentences after every completed PLAY response. The standard checkpoint cadence is **20 completed PLAY replies** since verified persistence, with one generic warning before the checkpoint on the following eligible response. Nothing runs unattended.\n\nYou may decline either default during setup, or later say “disable autosave” / request recalibration of incremental recording. “Checkpoint now,” “save now,” “delay autosave” and “resume autosave” remain available. Additional early checkpoint triggers for consequential state, scene boundaries or supported context pressure are opt-in rather than part of the standard cadence.'
)
replace('GAME/QUICKSTART.md', 'installing v0.9.7.', 'installing v0.9.8.')

replace('GAME/INSTALLATION.md', '## Optional write-only log', '## Standard write-only log for new campaigns')
replace(
    'GAME/INSTALLATION.md',
    'This copy includes the separately selected [write-only play log](ADMIN/PLAY_PERSISTENCE.md).',
    'New v0.9.8 campaigns select the [write-only play log](ADMIN/PLAY_PERSISTENCE.md) by default unless the operator declines or customizes it during setup.'
)
replace(
    'GAME/INSTALLATION.md',
    'Installing v0.9.7 enables no log or invisible memory service.',
    'A new v0.9.8 campaign proposes the short log by default; upgrading an existing campaign does not silently enable it or any invisible memory service.'
)
replace(
    'GAME/INSTALLATION.md',
    'The optional [announced autosave policy](ADMIN/AUTOSAVE.md) must be explicitly selected. It invokes the same protected complete-present CHECKPOINT after advance notice; no daemon or mandatory script is required.',
    'New v0.9.8 campaigns also propose [announced checkpointing](ADMIN/AUTOSAVE.md) by default: a protected complete-present CHECKPOINT on a 20-completed-PLAY-reply cadence after advance notice. Existing campaigns keep their prior autosave choice unless explicitly recalibrated. No daemon or mandatory script is required.'
)
replace('GAME/INSTALLATION.md', 'Give the GM the v0.9.7 kit as the update source', 'Give the GM the v0.9.8 kit as the update source')
replace('GAME/INSTALLATION.md', 'Valid v0.7.3, v0.8.0, v0.8.1, v0.8.2, v0.9.0, v0.9.1, v0.9.2, v0.9.3 and v0.9.4 records', 'Valid v0.7.3, v0.8.0, v0.8.1, v0.8.2, v0.9.0, v0.9.1, v0.9.2, v0.9.3, v0.9.4, v0.9.5, v0.9.6 and v0.9.7 records')

replace('GAME/README.md', 'Current `main` includes the **13 September 2026 v0.9.7** saving and continuity fixes. Older tagged game ZIPs retain their original bytes.', 'Current `main` includes **v0.9.8** default incremental logging and 20-reply announced checkpoints for new campaigns. Older tagged game ZIPs retain their original bytes.')
replace('GAME/README.md', '**Version 0.9.7.**', '**Version 0.9.8.**')

# Main docs: only the user-facing persistence/version statements needed for this release.
replace(
    'README.md',
    'Autosave and brief write-only PLAY notes are separate optional setup choices. A note does not replace a verified save.',
    'New v0.9.8 campaigns default to a brief write-only PLAY note after each completed play response and an announced CHECKPOINT every 20 completed PLAY replies. You can disable or customize either during setup or recalibration. A note does not replace a verified save.'
)
replace('README.md', '**Current software: v0.9.7.**', '**Current software: v0.9.8.**')
replace('README.md', '[Release changes](DOCS/releases/V0.9.7_CHANGES.md).', '[Release changes](DOCS/releases/V0.9.8_CHANGES.md).')

replace(
    'DOCS/BEGINNER_GUIDE.md',
    'Autosave starts off unless you select it. To enable the standard policy, say **“Enable the standard announced autosave policy in ADMIN/AUTOSAVE.md for this campaign.”** It announces checkpoints during play; it is not a background service. A checkpoint protects the current state but does not archive new exact dialogue.',
    'New v0.9.8 campaigns default to a tiny write-only outcome note after each completed PLAY response and an announced CHECKPOINT every 20 completed PLAY replies. You can decline either during setup or disable/customize them later through recalibration. Checkpointing is not a background service. A checkpoint protects the current state but does not archive new exact dialogue.'
)
replace('DOCS/BEGINNER_GUIDE.md', 'This guide explains the existing v0.9.7 workflow.', 'This guide explains the existing v0.9.8 workflow.')

# Scheduler/protocol regression expectations.
replace('DEV/TOOLS/test_autosave.py', 'return replace(Observation(enabled=True, dirty=True, turn=15, turns_since_save=15), **changes)', 'return replace(Observation(enabled=True, dirty=True, turn=20, turns_since_save=20), **changes)')
replace(
    'DEV/TOOLS/test_autosave.py',
    '    def test_default_off(self):\n        self.assertEqual(decide(Observation(dirty=True, consequential=True)).reason, "disabled")',
    '    def test_default_enabled_for_fresh_profile(self):\n        self.assertTrue(Observation().enabled)\n        self.assertEqual(decide(Observation(dirty=True, turn=20, turns_since_save=20)).action, "warn")\n\n    def test_explicit_disable_still_wins(self):\n        self.assertEqual(decide(Observation(enabled=False, dirty=True, consequential=True)).reason, "disabled")'
)
replace('DEV/TOOLS/test_autosave.py', '("warn", 15)', '("warn", 20)', count=1)
replace('DEV/TOOLS/test_autosave.py', 'self.sample(warned_at=15)', 'self.sample(warned_at=20)', count=3)
replace('DEV/TOOLS/test_autosave.py', 'self.sample(turn=16, warned_at=15)', 'self.sample(turn=21, warned_at=20)', count=4)
replace('DEV/TOOLS/test_autosave.py', 'turns_since_save=15', 'turns_since_save=20', count=1)
replace('DEV/TOOLS/test_autosave.py', 'self.sample(interval=20)', 'self.sample(interval=25)')
replace('DEV/TOOLS/test_autosave.py', '("off unless explicitly accepted", "one response before", "15 completed PLAY replies",', '("new v0.9.8 campaigns", "one response before", "20 completed PLAY replies",')
replace('DEV/TOOLS/test_autosave.py', 'Observation(enabled=True, dirty=True, turn=16, turns_since_save=16, warned_at=15)', 'Observation(enabled=True, dirty=True, turn=21, turns_since_save=21, warned_at=20)')

# Release history and legacy fixture mapping.
release = ROOT / 'DOCS/releases/V0.9.8_CHANGES.md'
release.write_text('''# RPG OS v0.9.8 — default incremental persistence\n\n14 September 2026.\n\n## Changes\n\n- New campaigns now propose the write-only play log by default: after each completed PLAY response, one or two concise factual outcome sentences are appended without per-turn persistence reads or semantic checking.\n- New campaigns now propose announced CHECKPOINTs on a **20 completed PLAY reply** cadence by default. One generic warning precedes the checkpoint; nothing runs unattended.\n- Consequential-state, scene-boundary and supported context-pressure checkpoint triggers remain available as optional early triggers instead of being part of the standard cadence.\n- `END SESSION SAVE` retains the existing behavior: stop fiction, take feedback or an explicit skip, perform due wrap-up, then make a full save.\n- Players may decline or customize either default during setup and may disable/recalibrate them later. Existing campaigns are not silently retrofitted; their accepted persistence policy remains authoritative.\n- The deterministic autosave helper now defaults to the fresh-campaign profile (`enabled=true`, interval 20) while callers for bound/legacy campaigns still override from the accepted agreement.\n\n## Scope\n\nThis release changes the default persistence profile for **new campaigns**. It does not make background saves, treat the short log as a transcript, alter fictional authority, or claim semantic-review perfection. Checkpoints preserve current state; full saves preserve the available history/review boundary according to the existing save procedures.\n''', encoding='utf-8')

p = ROOT / 'DOCS/CHANGELOG.md'
text = p.read_text(encoding='utf-8')
marker = '## v0.9.7 — practical pacing and long-campaign maintenance (2026-09-12)'
if marker not in text:
    raise SystemExit('CHANGELOG marker missing')
entry = '''## v0.9.8 — default incremental persistence (2026-09-14)\n\n- New campaigns default to the one/two-sentence write-only outcome log after every completed PLAY response.\n- New campaigns default to announced CHECKPOINTs every 20 completed PLAY replies; optional early triggers remain separately selectable.\n- END SESSION SAVE continues to perform feedback/wrap-up followed by a full save.\n- Existing campaigns keep their accepted persistence settings unless explicitly recalibrated.\n\nSee [release notes](releases/V0.9.8_CHANGES.md).\n\n'''
p.write_text(text.replace(marker, entry + marker, 1), encoding='utf-8')

p = ROOT / 'DEV/legacy_map.json'
data = json.loads(p.read_text(encoding='utf-8'))
data['V0.9.8_CHANGES.md'] = 'DOCS/releases/V0.9.8_CHANGES.md'
p.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')

print('patched default persistence profile for v0.9.8')
