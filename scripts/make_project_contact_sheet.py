#!/usr/bin/env python3
"""Create Dialyn's project-specific labeled contact sheet from a v2 atlas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


COLUMNS = 8
ROWS = 11
CELL_WIDTH = 192
CELL_HEIGHT = 208
ATLAS_WIDTH = COLUMNS * CELL_WIDTH
ATLAS_HEIGHT = ROWS * CELL_HEIGHT
LABEL_HEIGHT = 22
ROW_NAMES = [
    "idle",
    "running-right",
    "running-left",
    "waving",
    "jumping",
    "failed",
    "waiting",
    "running",
    "review",
    "look 000-157.5",
    "look 180-337.5",
]
FRAME_COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]


def is_used_cell(row: int, column: int) -> bool:
    """Return whether the fixed project contract uses this atlas slot."""
    return column < FRAME_COUNTS[row]


def checker(size: tuple[int, int], square: int = 16) -> Image.Image:
    """Create a neutral checkerboard behind transparent atlas cells."""
    image = Image.new("RGB", size, "#ffffff")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], square):
        for x in range(0, size[0], square):
            if (x // square + y // square) % 2:
                draw.rectangle((x, y, x + square - 1, y + square - 1), fill="#e8e8e8")
    return image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "atlas",
        help="Path to the transparent 1536x2288 Dialyn v2 atlas.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Destination PNG for the labeled project contact sheet.",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=0.5,
        help="Display scale applied to each 192x208 cell (default: 0.5).",
    )
    parser.add_argument(
        "--json-out",
        help="Optional destination for the machine-readable generation summary.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.scale <= 0:
        raise SystemExit("--scale must be greater than zero")

    atlas_path = Path(args.atlas).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    with Image.open(atlas_path) as opened:
        atlas = opened.convert("RGBA")
    if atlas.size != (ATLAS_WIDTH, ATLAS_HEIGHT):
        raise SystemExit(
            f"extended atlas must be {ATLAS_WIDTH}x{ATLAS_HEIGHT}; "
            f"got {atlas.width}x{atlas.height}"
        )

    cell_width = max(1, round(CELL_WIDTH * args.scale))
    cell_height = max(1, round(CELL_HEIGHT * args.scale))
    sheet_width = COLUMNS * cell_width
    sheet_height = ROWS * (cell_height + LABEL_HEIGHT)
    sheet = Image.new("RGB", (sheet_width, sheet_height), "#f7f7f7")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    unused_cells: list[dict[str, int]] = []
    for row in range(ROWS):
        y = row * (cell_height + LABEL_HEIGHT)
        draw.rectangle((0, y, sheet_width, y + LABEL_HEIGHT - 1), fill="#111111")
        draw.text((6, y + 5), f"row {row}: {ROW_NAMES[row]}", fill="#ffffff", font=font)
        draw.text(
            (sheet_width - 92, y + 5),
            f"{FRAME_COUNTS[row]} frames",
            fill="#ffffff",
            font=font,
        )

        for column in range(COLUMNS):
            left = column * CELL_WIDTH
            top = row * CELL_HEIGHT
            crop = atlas.crop((left, top, left + CELL_WIDTH, top + CELL_HEIGHT))
            crop = crop.resize((cell_width, cell_height), Image.Resampling.LANCZOS)
            background = checker((cell_width, cell_height))
            background.paste(crop, (0, 0), crop)

            x = column * cell_width
            sheet.paste(background, (x, y + LABEL_HEIGHT))
            used = is_used_cell(row, column)
            outline = "#18a058" if used else "#cc3344"
            draw.rectangle(
                (x, y + LABEL_HEIGHT, x + cell_width - 1, y + LABEL_HEIGHT + cell_height - 1),
                outline=outline,
            )
            draw.text((x + 4, y + LABEL_HEIGHT + 4), str(column), fill="#111111", font=font)
            if not used:
                unused_cells.append({"row": row, "column": column})

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)

    result = {
        "ok": True,
        "atlas": str(atlas_path),
        "output": str(output_path),
        "atlas_size": [ATLAS_WIDTH, ATLAS_HEIGHT],
        "cell_size": [CELL_WIDTH, CELL_HEIGHT],
        "display_scale": args.scale,
        "sheet_size": [sheet.width, sheet.height],
        "row_frame_counts": FRAME_COUNTS,
        "used_frame_slots": sum(FRAME_COUNTS),
        "unused_cells": unused_cells,
    }
    if args.json_out:
        json_path = Path(args.json_out).expanduser().resolve()
        json_path.parent.mkdir(parents=True, exist_ok=True)
        result["json_output"] = str(json_path)
        json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
