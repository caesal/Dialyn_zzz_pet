#!/usr/bin/env python3
"""Rebuild a complete frame manifest without re-extracting approved rows."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FRAME_COUNTS = {
    "idle": 6,
    "running-right": 8,
    "running-left": 8,
    "waving": 4,
    "jumping": 5,
    "failed": 8,
    "waiting": 6,
    "running": 6,
    "review": 6,
}
ALLOWED_METHODS = {"components", "slots", "stable-slots"}


def parse_color(value: str) -> tuple[int, int, int]:
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
        raise SystemExit(f"invalid chroma key: {value}")
    return tuple(int(value[index : index + 2], 16) for index in (1, 3, 5))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames-root", required=True)
    parser.add_argument("--policy", required=True)
    parser.add_argument("--output")
    parser.add_argument("--chroma-key", default="#FF00FF")
    parser.add_argument("--key-threshold", type=float, default=96.0)
    args = parser.parse_args()

    frames_root = Path(args.frames_root).expanduser().resolve()
    policy_path = Path(args.policy).expanduser().resolve()
    output_path = (
        Path(args.output).expanduser().resolve()
        if args.output
        else frames_root / "frames-manifest.json"
    )
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    methods = policy.get("standard_rows")
    if not isinstance(methods, dict):
        raise SystemExit("policy must contain a standard_rows object")

    rows: list[dict[str, object]] = []
    for state, expected_count in FRAME_COUNTS.items():
        method = methods.get(state)
        if method not in ALLOWED_METHODS:
            raise SystemExit(f"missing or invalid extraction method for {state}: {method!r}")
        state_dir = frames_root / state
        frames = [state_dir / f"{index:02d}.png" for index in range(expected_count)]
        missing = [str(path) for path in frames if not path.is_file()]
        if missing:
            raise SystemExit(f"missing approved frames for {state}: {', '.join(missing)}")
        unexpected = sorted(
            path.name
            for path in state_dir.glob("*.png")
            if path.name not in {frame.name for frame in frames}
        )
        if unexpected:
            raise SystemExit(f"unexpected frame files for {state}: {', '.join(unexpected)}")
        rows.append(
            {
                "state": state,
                "frames": [str(path) for path in frames],
                "method": method,
            }
        )

    red, green, blue = parse_color(args.chroma_key)
    result = {
        "ok": True,
        "chroma_key": {
            "hex": f"#{red:02X}{green:02X}{blue:02X}",
            "rgb": [red, green, blue],
            "threshold": args.key_threshold,
        },
        "rows": rows,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "output": str(output_path), "rows": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
