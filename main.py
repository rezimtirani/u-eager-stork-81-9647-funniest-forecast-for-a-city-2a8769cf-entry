"""Funniest Forecast for a City That Isn't — make.fun entry.

Writes one line — tonight's weather forecast for Nowhereville, a city
that does not exist — to $MAKEFUN_OUTPUT_DIR/entry.txt. The rain falls
sideways, the high is Tuesday, and the low is pure confusion. Only the
Python standard library is used.
"""

import os
import sys

FORECAST = "Tonight in Nowhereville: 400% chance of rain falling sideways, highs of Tuesday, lows of pure confusion."

# Sealed gate from the kit's RULES.txt ("## The gate"): the scorer
# takes UTF-8 text of 1 to 120 characters. The req JSON's "200
# characters" is generic template text and does not apply here.
MAX_CHARS = 120


def validate_forecast(text):
    """Return the forecast once it passes the sealed gate, else raise.

    The gate counts characters, not bytes; the line must be a single
    line, not only whitespace, with no trailing newline in the file.
    """
    if not isinstance(text, str):
        raise TypeError("forecast must be text")
    if not text.strip():
        raise ValueError("forecast must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("forecast must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("forecast must not contain control characters")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            "forecast must be 1 to %d characters, got %d" % (MAX_CHARS, len(text))
        )
    return text


def describe_forecast(text):
    """Summarise a forecast the way the sealed gate measures it.

    The gate counts UTF-8 characters, not bytes, so an ASCII forecast
    reads the same either way while a forecast with wide characters
    would not. Returns a one-line human-readable summary.
    """
    return "%d characters, %d UTF-8 bytes, %d words" % (
        len(text),
        len(text.encode("utf-8")),
        len(text.split()),
    )


def forecast_line():
    """Return the one-line forecast for the city that isn't."""
    return validate_forecast(FORECAST)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    line = forecast_line()
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as handle:
        handle.write(line)
    print(
        "wrote %s (%s)"
        % (os.path.join(out_dir, "entry.txt"), describe_forecast(line))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
