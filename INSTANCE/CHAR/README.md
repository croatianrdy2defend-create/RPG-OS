# INSTANCE/CHAR

Copy-on-write PC overlay and stable entrypoint.

At bind, ADMIN copies the exact accepted route closure rooted at MODULES/<id>/CHAR/PC.md to matching paths here and points CURRENT_SAVE pc_record to PC.md. PC.md may be one authoritative body or a compact routing index marked exactly `class: character-routing-index`. Every routed shard stays under this CHAR tree; indexes do not duplicate values, and PLAY never browses sibling files.
Never write sheet changes back to MODULE.
