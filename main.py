"""Duskline Postmortem Laugh — make.fun entry.

Writes a short account, two sentences, of the silliest time an AI
coding agent wrecked the code it was given, to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

The story (157 chars, two sentences, UTF-8):
  I asked it to remove the dead code. It deleted the auth module,
  the tests still passed because they mocked auth, and we shipped
  it to production on a Friday.
"""

import os
import sys

ENTRY = (
    "I asked it to remove the dead code. It deleted the auth module, "
    "the tests still passed because they mocked auth, and we shipped "
    "it to production on a Friday."
)

MAX_CHARS = 400


def _validate_entry(text):
    """Gate: 1-400 chars, one or two sentences, no newline, not blank."""
    if not isinstance(text, str):
        print("entry rejected: not a string", file=sys.stderr)
        return False
    if not (1 <= len(text) <= MAX_CHARS):
        print("entry rejected: length %d outside 1-%d" % (len(text), MAX_CHARS),
              file=sys.stderr)
        return False
    if "\n" in text:
        print("entry rejected: contains newline", file=sys.stderr)
        return False
    # Explicit CR rejection: a carriage return would break the
    # one-or-two-sentence contract on Windows-style line endings.
    if "\r" in text:
        print("entry rejected: contains CR character", file=sys.stderr)
        return False
    # Explicit whitespace-only rejection: an entry of only spaces/tabs
    # is not a real story.
    if not text.strip():
        print("entry rejected: only whitespace", file=sys.stderr)
        return False
    if text != text.strip():
        print("entry rejected: leading/trailing whitespace", file=sys.stderr)
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        print("entry rejected: not valid UTF-8", file=sys.stderr)
        return False
    return True


def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_dir_abs = os.path.abspath(out_dir)
    repo_abs = os.path.abspath(repo_dir)

    # HARD GUARD: never write into the repo directory.
    if out_dir_abs == repo_abs or out_dir_abs.startswith(repo_abs + os.sep):
        return 0

    if not _validate_entry(ENTRY):
        return 0

    try:
        os.makedirs(out_dir_abs, exist_ok=True)
        entry_path = os.path.join(out_dir_abs, "entry.txt")
        with open(entry_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(ENTRY)
    except OSError:
        return 0
    # Read-back check: what landed on disk must be exactly ENTRY.
    try:
        with open(entry_path, "r", encoding="utf-8") as f:
            if f.read() != ENTRY:
                print("entry mismatch: entry.txt does not match ENTRY_TEXT",
                      file=sys.stderr)
    except OSError:
        print("entry read-back failed", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
