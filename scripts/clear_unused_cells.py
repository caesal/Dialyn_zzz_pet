#!/usr/bin/env python3
"""Clear every atlas slot outside the repository's fixed v2 frame counts."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


COLUMNS = 8
ROWS = 11
CELL_WIDTH = 192
CELL_HEIGHT = 208
FRAME_COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    with Image.open(input_path) as opened:
        atlas = opened.convert("RGBA")

    expected = (COLUMNS * CELL_WIDTH, ROWS * CELL_HEIGHT)
    if atlas.size != expected:
        raise SystemExit(f"expected {expected[0]}x{expected[1]}, got {atlas.width}x{atlas.height}")

    empty = Image.new("RGBA", (CELL_WIDTH, CELL_HEIGHT), (0, 0, 0, 0))
    cleared: list[dict[str, int]] = []
    for row, frame_count in enumerate(FRAME_COUNTS):
        for column in range(frame_count, COLUMNS):
            atlas.paste(empty, (column * CELL_WIDTH, row * CELL_HEIGHT))
            cleared.append({"row": row, "column": column})

    output_path.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(output_path)
    print(f"wrote {output_path}")
    print(f"cleared {len(cleared)} unused cells")


if __name__ == "__main__":
    main()
