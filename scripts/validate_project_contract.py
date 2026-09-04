#!/usr/bin/env python3
"""Validate the repository's 73-frame Dialyn v2 atlas contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path

from PIL import Image, ImageFilter


COLUMNS = 8
ROWS = 11
CELL_WIDTH = 192
CELL_HEIGHT = 208
WIDTH = COLUMNS * CELL_WIDTH
HEIGHT = ROWS * CELL_HEIGHT
ROW_SPECS = [
    ("idle", 6),
    ("running-right", 8),
    ("running-left", 8),
    ("waving", 4),
    ("jumping", 5),
    ("failed", 8),
    ("waiting", 6),
    ("running", 6),
    ("review", 6),
    ("look-000-to-157.5", 8),
    ("look-180-to-337.5", 8),
]


def parse_color(value: str) -> tuple[int, int, int]:
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
        raise SystemExit(f"invalid chroma key: {value}")
    return tuple(int(value[index : index + 2], 16) for index in (1, 3, 5))


def distance(color: tuple[int, int, int], key: tuple[int, int, int]) -> float:
    return math.sqrt(sum((channel - target) ** 2 for channel, target in zip(color, key)))


def alpha_count(image: Image.Image) -> int:
    return sum(image.getchannel("A").histogram()[1:])


def transparent_residue(image: Image.Image) -> int:
    return sum(
        alpha == 0 and bool(red or green or blue)
        for red, green, blue, alpha in image.get_flattened_data()
    )


def chroma_counts(
    image: Image.Image,
    key: tuple[int, int, int],
    *,
    leak_threshold: float = 36.0,
    fringe_threshold: float = 96.0,
) -> tuple[int, int]:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    transparent = Image.new("L", alpha.size)
    transparent.putdata([255 if value == 0 else 0 for value in alpha.get_flattened_data()])
    near_transparency = transparent.filter(ImageFilter.MaxFilter(5))

    leak = 0
    fringe = 0
    for pixel, nearby in zip(rgba.get_flattened_data(), near_transparency.get_flattened_data()):
        red, green, blue, alpha_value = pixel
        if alpha_value > 16 and distance((red, green, blue), key) <= leak_threshold:
            leak += 1
        if (
            alpha_value >= 16
            and nearby > 0
            and distance((red, green, blue), key) <= fringe_threshold
        ):
            fringe += 1
    return leak, fringe


def alpha_box(image: Image.Image) -> tuple[int, int, int, int] | None:
    return image.getchannel("A").getbbox()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("atlas")
    parser.add_argument("--json-out")
    parser.add_argument("--chroma-key", default="#FF00FF")
    parser.add_argument("--min-used-pixels", type=int, default=50)
    parser.add_argument("--max-chroma-leak-pixels", type=int, default=400)
    args = parser.parse_args()

    atlas_path = Path(args.atlas).expanduser().resolve()
    encoded = atlas_path.read_bytes()
    key = parse_color(args.chroma_key)
    errors: list[str] = []
    warnings: list[str] = []

    with Image.open(atlas_path) as opened:
        source_format = opened.format
        source_mode = opened.mode
        atlas = opened.convert("RGBA")

    if atlas.size != (WIDTH, HEIGHT):
        errors.append(f"expected {WIDTH}x{HEIGHT}, got {atlas.width}x{atlas.height}")
    if source_format != "PNG":
        errors.append(f"expected PNG, got {source_format}")
    if "A" not in source_mode:
        errors.append(f"expected an alpha-bearing source mode, got {source_mode}")

    cells: list[dict[str, object]] = []
    used_count = 0
    for row, (state, frame_count) in enumerate(ROW_SPECS):
        for column in range(COLUMNS):
            left = column * CELL_WIDTH
            top = row * CELL_HEIGHT
            cell = atlas.crop((left, top, left + CELL_WIDTH, top + CELL_HEIGHT))
            nontransparent = alpha_count(cell)
            used = column < frame_count
            if used:
                used_count += 1
                if nontransparent < args.min_used_pixels:
                    errors.append(f"{state}[{column}] is empty or too sparse ({nontransparent} pixels)")
            elif nontransparent:
                errors.append(f"{state}[{column}] is unused but contains {nontransparent} pixels")
            cells.append(
                {
                    "state": state,
                    "row": row,
                    "column": column,
                    "used": used,
                    "nontransparent_pixels": nontransparent,
                }
            )

    if used_count != 73:
        errors.append(f"expected 73 used frame slots, counted {used_count}")

    residue = transparent_residue(atlas)
    if residue:
        errors.append(f"transparent pixels retain RGB data in {residue} locations")
    leak, fringe = chroma_counts(atlas, key)
    if leak > args.max_chroma_leak_pixels:
        errors.append(f"opaque chroma-like pixels exceed limit: {leak}")
    if fringe:
        errors.append(f"visible chroma-contaminated edge pixels: {fringe}")

    idle_cell = atlas.crop((0, 0, CELL_WIDTH, CELL_HEIGHT))
    idle_box = alpha_box(idle_cell)
    jump_boxes = [
        alpha_box(atlas.crop((column * CELL_WIDTH, 4 * CELL_HEIGHT, (column + 1) * CELL_WIDTH, 5 * CELL_HEIGHT)))
        for column in range(5)
    ]
    jump_baselines = [box[3] - 1 if box else None for box in jump_boxes]
    idle_baseline = idle_box[3] - 1 if idle_box else None
    airborne_lift = (
        idle_baseline - min(value for value in jump_baselines if value is not None)
        if idle_baseline is not None and all(value is not None for value in jump_baselines)
        else None
    )
    landing_delta = (
        abs(jump_baselines[-1] - idle_baseline)
        if idle_baseline is not None and jump_baselines[-1] is not None
        else None
    )
    if airborne_lift is None or airborne_lift < 12:
        errors.append(f"jump lift is insufficient: {airborne_lift}")
    if landing_delta is None or landing_delta > 4:
        errors.append(f"jump landing misses idle baseline by {landing_delta} pixels")

    look_boxes = [
        alpha_box(atlas.crop((column * CELL_WIDTH, row * CELL_HEIGHT, (column + 1) * CELL_WIDTH, (row + 1) * CELL_HEIGHT)))
        for row in (9, 10)
        for column in range(8)
    ]
    look_centers = [((box[0] + box[2]) / 2) if box else None for box in look_boxes]
    look_widths = [(box[2] - box[0]) if box else None for box in look_boxes]
    neutral_center = ((idle_box[0] + idle_box[2]) / 2) if idle_box else None
    max_center_drift = (
        max(abs(center - neutral_center) for center in look_centers if center is not None)
        if neutral_center is not None and all(center is not None for center in look_centers)
        else None
    )
    width_ratio = (
        max(width for width in look_widths if width is not None)
        / min(width for width in look_widths if width is not None)
        if all(width is not None and width > 0 for width in look_widths)
        else None
    )
    if max_center_drift is None or max_center_drift > 12:
        errors.append(f"look center drift exceeds 12 pixels: {max_center_drift}")
    if width_ratio is None or width_ratio > 1.25:
        errors.append(f"look width ratio exceeds 1.25: {width_ratio}")

    result = {
        "ok": not errors,
        "atlas": str(atlas_path),
        "encoded_bytes": len(encoded),
        "sha256": hashlib.sha256(encoded).hexdigest(),
        "format": source_format,
        "mode": source_mode,
        "width": atlas.width,
        "height": atlas.height,
        "sprite_version_number": 2,
        "used_frame_slots": used_count,
        "transparent_rgb_residue_pixels": residue,
        "opaque_chroma_key_pixels": leak,
        "chroma_fringe_pixels": fringe,
        "jump": {
            "idle_baseline": idle_baseline,
            "jump_baselines": jump_baselines,
            "airborne_lift_pixels": airborne_lift,
            "landing_delta_pixels": landing_delta,
        },
        "look_registration": {
            "direction_count": len(look_boxes),
            "neutral_center_x": neutral_center,
            "look_centers_x": look_centers,
            "look_widths": look_widths,
            "maximum_center_drift_pixels": max_center_drift,
            "maximum_width_ratio": width_ratio,
        },
        "errors": errors,
        "warnings": warnings,
        "cells": cells,
    }
    if args.json_out:
        output = Path(args.json_out).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
