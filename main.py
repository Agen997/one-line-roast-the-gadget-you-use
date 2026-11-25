#!/usr/bin/env python3
"""One-Line Roast: The Gadget You Use Every Day.

Scores 6 original candidate roasts against the judge's 5 criteria, in the
brief's own order (weights 5/4/3/2/1), and writes the winner to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

Judge criteria, most important first:
  1. Roasts a gadget or app people use every day in a single line.
  2. Actually funny: the joke lands on a first read, sting of recognition.
  3. Fresh: an angle, comparison or detail not seen before.
  4. Neatly worded: tight, well timed, no wasted words, inside the limit.
  5. One person's specific gripe, concrete detail about how it behaves.

Gate: /output/entry.txt must be UTF-8 text of 1-200 characters, exactly
one line, not only whitespace.
"""

import os
import sys

# (text, scores per criterion 1-5, each 0-5)
CANDIDATES = [
    (
        "My smartwatch congratulated me for standing up after eleven hours "
        "in my chair, a participation trophy for my spine.",
        [5, 5, 4, 5, 5],
    ),
    (
        "My phone's autocorrect changed 'meeting at 3' to 'mating at 3' "
        "and sent it to my boss before I could stop it.",
        [5, 5, 3, 4, 5],
    ),
    (
        "My earbuds' case swears they're 100% charged, then the left one "
        "dies mid-sentence on every call \u2014 optimism with a battery.",
        [5, 4, 3, 4, 4],
    ),
    (
        "My laptop's fan sounds like a jet taking off whenever I open a "
        "second tab \u2014 I didn't buy a computer, I bought a departure lounge.",
        [5, 4, 3, 4, 4],
    ),
    (
        "My printer is offline only when I actually need it \u2014 it can "
        "smell a deadline the way a dog smells fear.",
        [5, 4, 3, 4, 4],
    ),
    (
        "My Wi-Fi router needs a restart every time it rains, as if the "
        "weather personally offends it.",
        [5, 3, 4, 5, 3],
    ),
]

WEIGHTS = [5, 4, 3, 2, 1]

# Rejected drafts and why (kept as a record of the choice):
# - "My phone dies at four in the afternoon." -- the brief's own example;
#   the judge has seen it, freshness 0.
# - "My smart kettle wants a firmware update before it boils water." --
#   also the brief's own example, same problem.
# - "My app asks me to rate it before it even opens." -- brief's example
#   again; every entrant will have thought of it.
# - "My phone battery is at 1% by lunch." -- generic complaint, could be
#   about anything, no concrete detail, no punch.
# - "My earbuds are always tangled." -- wired-earbud nostalgia; most people
#   use wireless now, and it has no twist.


def score(entry):
    text, marks = entry
    return sum(w * m for w, m in zip(WEIGHTS, marks))


def main():
    ranked = sorted(CANDIDATES, key=score, reverse=True)
    winner, marks = ranked[0]
    # Gate: one line, 1-200 chars, not only whitespace.
    assert "\n" not in winner, "winner must be a single line"
    assert 1 <= len(winner) <= 200, "winner must be 1-200 characters"
    assert winner.strip(), "winner must not be only whitespace"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(winner)
    print(f"winner ({len(winner)} chars, score {score(ranked[0])}): {winner}")
    for entry in ranked[1:]:
        print(f"  {score(entry)}: {entry[0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
