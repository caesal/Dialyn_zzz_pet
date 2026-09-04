#!/usr/bin/env python3
"""Normalize Dialyn's 16 look cells to a shared scale and planted baseline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


CELL_WIDTH = 192
CELL_HEIGHT = 208
LOOK_ROWS = (9, 10)


def visible_points(image: Image.Image, threshold: int = 16) -> list[tuple[int, int]]:
    alpha = image.getchannel("A")
    return [
        (x, y)
        for y in range(image.height)
        for x in range(image.width)
        if alpha.getpixel((x, y)) > threshold
    ]


def lower_center_x(image: Image.Image) -> float:
    points = visible_points(image)
    if not points:
        raise ValueError("look cell is empty")
    top = min(y for _, y in points)
    bottom = max(y for _, y in points) + 1
    lower_start = top + (bottom - top) * 0.72
    lower = [(x, y) for x, y in points if y >= lower_start] or points
    return sum(x for x, _ in lower) / len(lower)


def clear_transparent_rgb(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    data = bytearray(rgba.tobytes())
    for index in range(0, len(data), 4):
        if data[index + 3] == 0:
            data[index : index + 3] = b"\x00\x00\x00"
    return Image.frombytes("RGBA", rgba.size, bytes(data))


def normalize_cell(
    cell: Image.Image,
    target_height: int,
    target_center_x: float,
    target_bottom: int,
    horizontal_anchor: str,
) -> tuple[Image.Image, dict[str, object]]:
    bbox = cell.getbbox()
    if bbox is None:
        raise ValueError("look cell is empty")

    left, top, right, bottom = bbox
    crop = cell.crop(bbox).convert("RGBA")
    source_height = bottom - top
    scale = target_height / source_height
    resized = crop.resize(
        (
            max(1, round(crop.width * scale)),
            max(1, round(crop.height * scale)),
        ),
        Image.Resampling.LANCZOS,
    )

    if horizontal_anchor == "bbox":
        source_center = crop.width / 2
    else:
        source_center = lower_center_x(cell) - left
    target_left = round(target_center_x - source_center * scale)
    target_top = target_bottom - resized.height
    if (
        target_left < 0
        or target_top < 0
        or target_left + resized.width > CELL_WIDTH
        or target_top + resized.height > CELL_HEIGHT
    ):
        raise ValueError("normalized look cell would exceed its 192x208 slot")

    output = Image.new("RGBA", (CELL_WIDTH, CELL_HEIGHT), (0, 0, 0, 0))
    output.alpha_composite(resized, (target_left, target_top))
    output = clear_transparent_rgb(output)
    final_bbox = output.getbbox()
    if final_bbox is None:
        raise ValueError("normalized look cell became empty")

    return output, {
        "source_bbox": [left, top, right, bottom],
        "source_height": source_height,
        "scale": scale,
        "target_left": target_left,
        "target_top": target_top,
        "horizontal_anchor": horizontal_anchor,
        "final_bbox": list(final_bbox),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Input 1536x2288 v2 atlas")
    parser.add_argument("--output", required=True)
    parser.add_argument("--json-out")
    parser.add_argument("--target-height", type=int, default=192)
    parser.add_argument("--target-center-x", type=float, default=98.0)
    parser.add_argument("--target-bottom", type=int, default=203)
    parser.add_argument(
        "--horizontal-anchor",
        choices=("bbox", "lower-band"),
        default="bbox",
        help="Align each cell by its full silhouette center or lower-body center.",
    )
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    with Image.open(input_path) as opened:
        atlas = opened.convert("RGBA")
    if atlas.size != (1536, 2288):
        raise SystemExit(f"expected 1536x2288 atlas, got {atlas.width}x{atlas.height}")

    result = atlas.copy()
    cells: list[dict[str, object]] = []
    direction_index = 0
    for row in LOOK_ROWS:
        for column in range(8):
            box = (
                column * CELL_WIDTH,
                row * CELL_HEIGHT,
                (column + 1) * CELL_WIDTH,
                (row + 1) * CELL_HEIGHT,
            )
            normalized, metrics = normalize_cell(
                atlas.crop(box),
                args.target_height,
                args.target_center_x,
                args.target_bottom,
                args.horizontal_anchor,
            )
            result.paste((0, 0, 0, 0), box)
            result.alpha_composite(normalized, (box[0], box[1]))
            metrics.update(
                {
                    "direction_degrees": direction_index * 22.5,
                    "row": row,
                    "column": column,
                }
            )
            cells.append(metrics)
            direction_index += 1

    result = clear_transparent_rgb(result)
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.save(output_path)

    report = {
        "ok": True,
        "input": str(input_path),
        "output": str(output_path),
        "target_height": args.target_height,
        "target_center_x": args.target_center_x,
        "target_bottom": args.target_bottom,
        "horizontal_anchor": args.horizontal_anchor,
        "cells": cells,
    }
    if args.json_out:
        report_path = Path(args.json_out).expanduser().resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
