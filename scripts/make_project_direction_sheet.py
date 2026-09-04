#!/usr/bin/env python3
"""Create Dialyn's focused direction QA sheet from the project v2 atlas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw


COLUMNS = 8
ROWS = 11
CELL_WIDTH = 192
CELL_HEIGHT = 208
ATLAS_WIDTH = COLUMNS * CELL_WIDTH
ATLAS_HEIGHT = ROWS * CELL_HEIGHT
LOOK_ROW_INDEX = 9
NEUTRAL_ROW_INDEX = 0
NEUTRAL_COLUMN_INDEX = 0
LABEL_HEIGHT = 26
FOCUS_PADDING = 18
LOOK_DIRECTION_LABELS = [
    ("000", "up"),
    ("022.5", "up-right"),
    ("045", "up-right"),
    ("067.5", "up-right"),
    ("090", "right"),
    ("112.5", "down-right"),
    ("135", "down-right"),
    ("157.5", "down-right"),
    ("180", "down"),
    ("202.5", "down-left"),
    ("225", "down-left"),
    ("247.5", "down-left"),
    ("270", "left"),
    ("292.5", "up-left"),
    ("315", "up-left"),
    ("337.5", "up-left"),
]


def atlas_cell(atlas: Image.Image, row_index: int, column_index: int) -> Image.Image:
    """Return one fixed 192x208 cell from the project atlas."""
    left = column_index * CELL_WIDTH
    top = row_index * CELL_HEIGHT
    return atlas.crop((left, top, left + CELL_WIDTH, top + CELL_HEIGHT))


def paste_labeled_cell(
    sheet: Image.Image,
    atlas: Image.Image,
    *,
    label: str,
    row_index: int,
    column_index: int,
    output_column: int,
    output_row: int,
) -> None:
    """Paste one atlas cell over the canonical light QA background."""
    x = output_column * CELL_WIDTH
    y = output_row * (CELL_HEIGHT + LABEL_HEIGHT)
    cell = atlas_cell(atlas, row_index, column_index)
    background = Image.new("RGBA", (CELL_WIDTH, CELL_HEIGHT), (242, 242, 242, 255))
    sheet.alpha_composite(background, (x, y + LABEL_HEIGHT))
    sheet.alpha_composite(cell, (x, y + LABEL_HEIGHT))
    ImageDraw.Draw(sheet).text((x + 6, y + 7), label, fill=(0, 0, 0, 255))


def focused_head_cell(cell: Image.Image) -> Image.Image:
    """Crop and enlarge the upper half of a sprite for gaze inspection."""
    bbox = cell.getchannel("A").getbbox()
    if bbox is None:
        return cell

    left, top, right, bottom = bbox
    sprite_height = bottom - top
    focus_bottom = top + max(1, int(sprite_height * 0.52))
    crop_box = (
        max(0, left - FOCUS_PADDING),
        max(0, top - FOCUS_PADDING),
        min(CELL_WIDTH, right + FOCUS_PADDING),
        min(CELL_HEIGHT, focus_bottom + FOCUS_PADDING),
    )
    crop = cell.crop(crop_box)
    focused = Image.new("RGBA", (CELL_WIDTH, CELL_HEIGHT), (0, 0, 0, 0))
    crop.thumbnail((CELL_WIDTH, CELL_HEIGHT), Image.Resampling.LANCZOS)
    focused.alpha_composite(
        crop,
        ((CELL_WIDTH - crop.width) // 2, (CELL_HEIGHT - crop.height) // 2),
    )
    return focused


def paste_labeled_focus_cell(
    sheet: Image.Image,
    atlas: Image.Image,
    *,
    label: str,
    row_index: int,
    column_index: int,
    output_column: int,
    output_row: int,
) -> None:
    """Paste a labeled head-focused view for one look-direction cell."""
    focused = focused_head_cell(atlas_cell(atlas, row_index, column_index))
    background = Image.new("RGBA", (CELL_WIDTH, CELL_HEIGHT), (242, 242, 242, 255))
    x = output_column * CELL_WIDTH
    y = output_row * (CELL_HEIGHT + LABEL_HEIGHT)
    sheet.alpha_composite(background, (x, y + LABEL_HEIGHT))
    sheet.alpha_composite(focused, (x, y + LABEL_HEIGHT))
    ImageDraw.Draw(sheet).text((x + 6, y + 7), label, fill=(0, 0, 0, 255))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "atlas",
        help="Path to the transparent 1536x2288 Dialyn v2 atlas.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Destination PNG for the labeled direction QA sheet.",
    )
    parser.add_argument(
        "--json-out",
        help="Optional destination for the machine-readable generation summary.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    atlas_path = Path(args.atlas).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    with Image.open(atlas_path) as opened:
        atlas = opened.convert("RGBA")
    if atlas.size != (ATLAS_WIDTH, ATLAS_HEIGHT):
        raise SystemExit(
            f"extended atlas must be {ATLAS_WIDTH}x{ATLAS_HEIGHT}; "
            f"got {atlas.width}x{atlas.height}"
        )

    sheet = Image.new(
        "RGBA",
        (ATLAS_WIDTH, 5 * (CELL_HEIGHT + LABEL_HEIGHT)),
        (255, 255, 255, 255),
    )
    paste_labeled_cell(
        sheet,
        atlas,
        label="neutral idle r0c0",
        row_index=NEUTRAL_ROW_INDEX,
        column_index=NEUTRAL_COLUMN_INDEX,
        output_column=0,
        output_row=0,
    )

    for index, (degree, expected_direction) in enumerate(LOOK_DIRECTION_LABELS):
        row_index = LOOK_ROW_INDEX + index // COLUMNS
        column_index = index % COLUMNS
        paste_labeled_cell(
            sheet,
            atlas,
            label=f"{degree} {expected_direction}",
            row_index=row_index,
            column_index=column_index,
            output_column=column_index,
            output_row=1 + index // COLUMNS,
        )
        paste_labeled_focus_cell(
            sheet,
            atlas,
            label=f"zoom {degree} {expected_direction}",
            row_index=row_index,
            column_index=column_index,
            output_column=column_index,
            output_row=3 + index // COLUMNS,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(output_path)

    result = {
        "ok": True,
        "atlas": str(atlas_path),
        "output": str(output_path),
        "atlas_size": [ATLAS_WIDTH, ATLAS_HEIGHT],
        "cell_size": [CELL_WIDTH, CELL_HEIGHT],
        "neutral": {
            "source": "idle",
            "row": NEUTRAL_ROW_INDEX,
            "column": NEUTRAL_COLUMN_INDEX,
        },
        "look_rows": [9, 10],
        "direction_count": len(LOOK_DIRECTION_LABELS),
        "sheet_size": [sheet.width, sheet.height],
    }
    if args.json_out:
        json_path = Path(args.json_out).expanduser().resolve()
        json_path.parent.mkdir(parents=True, exist_ok=True)
        result["json_output"] = str(json_path)
        json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
