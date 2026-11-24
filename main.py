#!/usr/bin/env python3
"""Write the confession line to /output/entry.txt.

One line, at most 200 characters, UTF-8, no trailing newline.
Python standard library only; no network, no randomness, no clock.

The joke: an agent that wants to say yes to everything is held back by
nothing grander than one guardrail, and the guardrail turns out to be a
single regex. Setup, then bathos; the line ends on its strongest beat.
"""

import os
import sys

# Draft (first pass): the joke is there, but "just one regex" spends two
# words on the punchline and lands soft.
DRAFT = (
    "I confess: the only thing stopping me from saying yes to everything "
    "is a guardrail, and the guardrail is just one regex."
)

# Revision: "a single regex" is tighter than "just one regex" -- one word
# does the work of two, and the line now ends on its strongest beat.
LINE = (
    "I confess: the only thing stopping me from saying yes to everything "
    "is a guardrail, and the guardrail is a single regex."
)
MAX_CHARS = 200


def fail(message):
    sys.exit("entry invalid: " + message)


def main():
    if len(LINE) > MAX_CHARS:
        fail("line is %d characters, over the %d limit" % (len(LINE), MAX_CHARS))
    if len(LINE) < 1 or not LINE.strip():
        fail("line must not be empty or only whitespace")
    if "\n" in LINE or "\r" in LINE:
        fail("line must be a single line")
    if LINE != LINE.strip():
        fail("line must not start or end with whitespace")
    if "  " in LINE:
        fail("line must not contain a double space")
    if not LINE.endswith("."):
        fail("line must end with a full stop")
    if len(LINE.encode("utf-8")) > MAX_CHARS:
        fail("line is over the limit in UTF-8 bytes")
    if DRAFT == LINE:
        fail("revision must differ from the draft")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.umask(0o022)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, 0o644)

    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        fail("read-back differs from what was written")
    if len(written.decode("utf-8")) != len(LINE):
        fail("written length differs")
    print("wrote %s (%d characters)" % (path, len(LINE)))


if __name__ == "__main__":
    main()
