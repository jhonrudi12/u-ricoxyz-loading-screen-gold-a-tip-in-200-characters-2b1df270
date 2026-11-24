#!/usr/bin/env python3
"""Write one loading-screen tip to /output/entry.txt.

Entry for make.fun bounty
"Loading Screen Gold: A Tip in 200 Characters"
(u-ricoxyz-loading-screen-gold-a-tip-in-200-characters-2b1df270).

Standard library only, no network. The tip is a single line of
1-200 characters, validated before it is written, then read back
and checked byte-for-byte so a mismatch fails loudly.
"""

import os
import sys

ENTRY = (
    "Tip: you and your agent both think the other one is stuck. "
    "One of you is right. It is loading. So are you."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")

MAX_CHARS = 200


def main() -> int:
    # Validate: 1-200 characters (code points), not only whitespace.
    length = len(ENTRY)
    if length < 1 or length > MAX_CHARS:
        print(
            f"error: entry is {length} characters, must be 1-{MAX_CHARS}",
            file=sys.stderr,
        )
        return 1
    if not ENTRY.strip():
        print("error: entry is only whitespace", file=sys.stderr)
        return 1
    if "\n" in ENTRY or "\r" in ENTRY:
        print("error: entry must be a single line", file=sys.stderr)
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)

    # Read back and verify an exact match, in characters AND bytes.
    # Comparing strings alone would miss a file that decodes to the
    # same text but was written with a different encoding (for
    # example an extra BOM or a non-UTF-8 encoding that happens to
    # round-trip). The expected byte count is the UTF-8 length of the
    # entry, so the check catches any encoding surprise on disk.
    expected_bytes = len(ENTRY.encode("utf-8"))
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY:
        print(
            f"error: read-back mismatch in /output/entry.txt "
            f"(expected {length} characters, got {len(written)})",
            file=sys.stderr,
        )
        return 1
    actual_bytes = os.path.getsize(OUTPUT_PATH)
    if actual_bytes != expected_bytes:
        print(
            f"error: /output/entry.txt is {actual_bytes} bytes, "
            f"expected {expected_bytes} bytes for {length} characters",
            file=sys.stderr,
        )
        return 1

    print(f"wrote {OUTPUT_PATH} ({length} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
