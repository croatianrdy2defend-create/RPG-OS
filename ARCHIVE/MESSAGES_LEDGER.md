# MESSAGES LEDGER

Cold index. PLAY does not load this at boot.
Pointer must be a POSIX path relative to `ARCHIVE/`, followed by a literal stable heading id (example: `sessions/s01-d001/05_message_exchange.md#M-<save_id>-01`).
Existing pointers to legacy `MESSAGES.md` headings remain valid. The ledger stores a routing gist, not the full exchange.
The machine-readable table uses outer `|` delimiters and one contiguous row block. Every row supplies `when`, `from`, `to`, `gist`, and `pointer`; use an explicit `unknown` where necessary rather than a blank.

| when | from | to | gist | pointer |
|---|---|---|---|---|
