#!/usr/bin/env python3
"""
matrix_rain.py — A colorful "Matrix digital rain" effect for your terminal.

Usage:
    python3 matrix_rain.py                     # classic green
    python3 matrix_rain.py --color cyan         # single color
    python3 matrix_rain.py --multi              # random colors per column
    python3 matrix_rain.py --multi --colors green,cyan,magenta,yellow
    python3 matrix_rain.py --speed 0.03         # faster
    python3 matrix_rain.py --charset katakana    # different glyph set

Press Ctrl+C to stop.
"""

from __future__ import annotations

import argparse
import random
import shutil
import sys
import time

from rich.console import Console
from rich.text import Text

console = Console()

CHARSETS = {
    "ascii": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "binary": "01",
    "symbols": "!@#$%^&*()-_=+[]{}<>/\\|;:,.?",
    "katakana": (
        "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    ),
}

DEFAULT_PALETTE = [
    "green",
    "bright_green",
    "cyan",
    "bright_cyan",
    "magenta",
    "bright_magenta",
    "yellow",
    "bright_yellow",
    "blue",
    "bright_blue",
    "red",
    "bright_red",
]


class Column:
    """Tracks the falling 'drop' state for a single column of the matrix."""

    def __init__(self, x: int, height: int, color: str) -> None:
        self.x = x
        self.height = height
        self.color = color
        self.reset()

    def reset(self) -> None:
        self.y = random.randint(-self.height, 0)
        self.length = random.randint(4, self.height // 2 + 4)
        self.speed = random.choice([1, 1, 1, 2])  # most fall at 1 row/tick

    def step(self) -> None:
        self.y += self.speed
        if self.y - self.length > self.height:
            self.reset()


def build_frame(
    columns: list[Column],
    width: int,
    height: int,
    charset: str,
    multi: bool,
    palette: list[str],
) -> Text:
    """Render one animation frame as a rich Text grid."""
    grid = [[" "] * width for _ in range(height)]
    styles = [[None] * width for _ in range(height)]

    for col in columns:
        head = col.y
        for i in range(col.length):
            row = head - i
            if 0 <= row < height:
                ch = random.choice(charset)
                grid[row][col.x] = ch
                if i == 0:
                    # Bright white leading character (classic Matrix "spark")
                    styles[row][col.x] = "bold white"
                else:
                    fade = i / col.length
                    color = col.color if not multi else col.color
                    if fade < 0.15:
                        styles[row][col.x] = f"bold {color}"
                    elif fade < 0.6:
                        styles[row][col.x] = color
                    else:
                        styles[row][col.x] = f"dim {color}"

    text = Text()
    for r in range(height):
        for c in range(width):
            ch = grid[r][c]
            style = styles[r][c]
            text.append(ch, style=style)
        if r != height - 1:
            text.append("\n")
    return text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a Matrix-style falling color-matrix animation in your terminal."
    )
    parser.add_argument(
        "--color",
        default="green",
        help="Single color to use when --multi is not set (rich color name, e.g. green, cyan, magenta).",
    )
    parser.add_argument(
        "--multi",
        action="store_true",
        help="Use multiple colors across columns instead of a single color.",
    )
    parser.add_argument(
        "--colors",
        default=",".join(DEFAULT_PALETTE),
        help="Comma-separated palette used when --multi is set.",
    )
    parser.add_argument(
        "--charset",
        choices=CHARSETS.keys(),
        default="katakana",
        help="Which glyph set to rain with (default: katakana, the classic look).",
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=0.05,
        help="Seconds between frames (lower = faster). Default 0.05.",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=None,
        help="Stop automatically after N seconds (default: run until Ctrl+C).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    charset = CHARSETS[args.charset]
    palette = [c.strip() for c in args.colors.split(",") if c.strip()]

    term_size = shutil.get_terminal_size(fallback=(80, 24))
    width, height = term_size.columns, term_size.lines - 1

    columns: list[Column] = []
    for x in range(width):
        color = random.choice(palette) if args.multi else args.color
        columns.append(Column(x, height, color))

    console.print(f"[bold]Starting matrix rain[/bold] — Ctrl+C to stop.\n")
    time.sleep(0.5)

    start = time.time()
    try:
        with console.screen():
            while True:
                for col in columns:
                    col.step()
                frame = build_frame(columns, width, height, charset, args.multi, palette)
                console.print(frame, end="")
                console.file.write("\x1b[H")  # move cursor to top-left, avoid scrolling
                time.sleep(args.speed)
                if args.duration is not None and time.time() - start >= args.duration:
                    break
    except KeyboardInterrupt:
        pass
    finally:
        console.print("\n[bold green]Matrix rain stopped.[/bold green]")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
