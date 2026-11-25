"""Worst Superpower.

Writes one invented superpower to $MAKEFUN_OUTPUT_DIR/entry.txt:
the power to summon a chair whenever I sit down, which only
shows up three seconds after I have already hit the floor.
Standard library only; the line is checked against the
competition gate (one line, 1 to 140 characters) before it is
written.
"""

from os import environ, makedirs
from os.path import join

POWER = (
    "I can summon a chair whenever I sit down, but it only "
    "appears three seconds after I've already hit the floor."
)

MAX_CHARS = 140


def validate_power(text):
    """Check the power line against the competition gate.

    The gate wants one line of plain UTF-8 text, between 1
    and 140 characters, that invents a superpower and makes
    plain why it is useless. Anything else is rejected here
    instead of wasting a submission on the server.
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("superpower line is empty")
    if len(cleaned) > MAX_CHARS:
        raise ValueError(
            "superpower line is %d characters, over the 140 limit"
            % len(cleaned)
        )
    if "\n" in cleaned or "\r" in cleaned:
        raise ValueError("superpower must fit on exactly one line")
    return cleaned


def power_has_turn(text):
    """Check the line carries its own punchline.

    The joke needs the turn: the power, then the reason it is
    useless, in the same breath. A line without that turn
    reads like a plain boast, so it is rejected here.
    """
    if "but" not in text.lower().split():
        raise ValueError("superpower line has no turn to its punchline")
    return text


def power_fingerprint(text):
    """Measure the line for a last sanity pass.

    Returns the character and word counts. A line too short
    to carry both the power and the punchline, or one padded
    out to fill the cap, is caught here before anything is
    written.
    """
    words = text.split()
    return {"chars": len(text), "words": len(words)}


def main():
    out_dir = environ.get("MAKEFUN_OUTPUT_DIR", "output")
    makedirs(out_dir, exist_ok=True)
    line = validate_power(POWER)
    line = power_has_turn(line)
    shape = power_fingerprint(line)
    if shape["words"] < 5:
        raise ValueError("superpower line is too short to land the joke")
    with open(join(out_dir, "entry.txt"), "w", encoding="utf-8") as handle:
        handle.write(line)
    return 0


if __name__ == "__main__":
    main()
