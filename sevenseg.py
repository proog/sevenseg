"""Module for displaying arbitrary strings on a 7-segment display."""

import RPi.GPIO as GPIO
import time

"""GPIO ports for the 7 segment pins"""
segments = (11, 4, 23, 8, 7, 10, 18, 25)

"""GPIO ports for the digit 0-3 pins"""
digits = (22, 27, 17, 24)

"""Width of the display in characters"""
width = len(digits)

"""
Patterns of on/off segments in the following order:
   __1__
  |     |
6 |     | 2
  |__7__|
  |     |
5 |     | 3
  |__4__|    . 8
"""
patterns = {
    " ": (0, 0, 0, 0, 0, 0, 0, 0),
    "0": (1, 1, 1, 1, 1, 1, 0, 0),
    "1": (0, 1, 1, 0, 0, 0, 0, 0),
    "2": (1, 1, 0, 1, 1, 0, 1, 0),
    "3": (1, 1, 1, 1, 0, 0, 1, 0),
    "4": (0, 1, 1, 0, 0, 1, 1, 0),
    "5": (1, 0, 1, 1, 0, 1, 1, 0),
    "6": (1, 0, 1, 1, 1, 1, 1, 0),
    "7": (1, 1, 1, 0, 0, 0, 0, 0),
    "8": (1, 1, 1, 1, 1, 1, 1, 0),
    "9": (1, 1, 1, 1, 0, 1, 1, 0),
    "A": (1, 1, 1, 0, 1, 1, 1, 0),
    "B": (0, 0, 1, 1, 1, 1, 1, 0),
    "C": (1, 0, 0, 1, 1, 1, 0, 0),
    "D": (0, 1, 1, 1, 1, 0, 1, 0),
    "E": (1, 0, 0, 1, 1, 1, 1, 0),
    "F": (1, 0, 0, 0, 1, 1, 1, 0),
    "G": (1, 0, 1, 1, 1, 1, 0, 0),
    "H": (0, 0, 1, 0, 1, 1, 1, 0),
    "I": (0, 1, 1, 0, 0, 0, 0, 0),
    "J": (0, 1, 1, 1, 0, 0, 0, 0),
    "K": (0, 1, 1, 0, 1, 1, 1, 0),
    "L": (0, 0, 0, 1, 1, 1, 0, 0),
    "M": (1, 1, 1, 0, 1, 1, 0, 0),
    "N": (0, 0, 1, 0, 1, 0, 1, 0),
    "O": (0, 0, 1, 1, 1, 0, 1, 0),
    "P": (1, 1, 0, 0, 1, 1, 1, 0),
    "Q": (1, 1, 1, 0, 0, 1, 1, 0),
    "R": (0, 0, 0, 0, 1, 0, 1, 0),
    "S": (1, 0, 1, 1, 0, 1, 1, 0),
    "T": (0, 0, 0, 1, 1, 1, 1, 0),
    "U": (0, 1, 1, 1, 1, 1, 0, 0),
    "V": (0, 0, 1, 1, 1, 0, 0, 0),
    "W": (0, 0, 1, 1, 1, 0, 0, 0),
    "X": (0, 1, 1, 0, 1, 1, 1, 0),
    "Y": (0, 1, 1, 1, 0, 1, 1, 0),
    "Z": (1, 1, 0, 1, 1, 0, 1, 0),
    "-": (0, 0, 0, 0, 0, 0, 1, 0),
    "_": (0, 0, 0, 1, 0, 0, 0, 0),
    ".": (0, 0, 0, 0, 0, 0, 0, 1),
    ",": (0, 0, 0, 0, 0, 0, 0, 1),
}


def display(text, max_loops=0):
    """Display a string, looping it forever or a specified number of times."""
    offset = 0
    loop_count = 0
    text = _clean(text)

    try:
        _reset()
        t = time.time()

        # loop forever or until max_loops
        while loop_count < max_loops or max_loops == 0:
            # render a display-width window into s, starting from offset
            window = text[offset:].ljust(width)
            _render(window)

            # scroll display
            threshold = t + 0.5
            t2 = time.time()

            if t2 > threshold:
                t = t2

                # push window forward
                offset = (offset + 1) % len(text)

                # if we reached the beginning of the string again, that's a loop
                if offset == 0:
                    loop_count += 1
    finally:
        GPIO.cleanup()


def _reset():
    """Reset the display."""
    GPIO.setmode(GPIO.BCM)

    for segment in segments:
        GPIO.setup(segment, GPIO.OUT)
        GPIO.output(segment, 0)

    for digit in digits:
        GPIO.setup(digit, GPIO.OUT)
        GPIO.output(digit, 1)


def _render(s):
    """Render a display-width string."""
    for digit in range(width):
        for loop in range(0, 8):
            char = s[digit].upper()
            pattern = patterns[char]
            GPIO.output(segments[loop], pattern[loop])

        GPIO.output(digits[digit], 0)
        time.sleep(0.001)
        GPIO.output(digits[digit], 1)


def _clean(s):
    """Remove unsupported characters and add leading space for ticker-like behavior."""
    return "".rjust(width) + "".join(c for c in s.upper() if c in patterns)
