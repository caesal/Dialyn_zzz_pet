# Codex instructions

This repository contains a custom ChatGPT Work pet based on Dialyn from Zenless Zone Zero.

## Start here

1. Read `HANDOFF.md` and `pet.json` before changing anything.
2. Use **Dialyn** as the pet and project name. Chinese prose may say `Dialyn（琉音）` for clarity.
3. Treat `assets/final/dialyn-spritesheet-v2.png` as the approved baseline, not a disposable intermediate.
4. Ask which visible behavior the user wants changed before regenerating frames.

## Editing rules

- For visual changes, use the available image-generation workflow and the canonical ChatGPT Pets skills.
- Preserve the character anchors: black-and-white braids, gold eyes, purple handset, teal cord, and gold/navy ring weapon.
- Do not mirror asymmetric features. The handset stays on the black-hair side; the long white braid stays on the opposite side.
- Replace only affected animation rows whenever possible.
- Keep the v2 atlas at 1536 × 2288 px, with 192 × 208 px cells and frame counts `[6,8,8,4,5,8,6,6,6,8,8]`.
- Preserve transparent backgrounds and remove chroma spill before final validation.
- Never overwrite the approved baseline without also retaining a versioned copy or recoverable Git commit.

## Validation and activation

- Regenerate state GIFs, the all-state preview, and the 16-direction preview after visual changes.
- Run structural, animation, transparency, direction-semantic, and continuity checks.
- Show the user motion before uploading or activating a pet.
- Only after approval: validate the exact final bytes with the Pets preflight, prepare the upload, create/update the pet as `Dialyn`, select it if requested, and verify by stable pet ID.

## Repository hygiene

- Keep final deliverables in `assets/final/`, editable strips in `assets/source/rows/`, previews in `assets/previews/`, and reports in `qa/`.
- Update `pet.json`, `HANDOFF.md`, and relevant QA reports when the approved atlas changes.
- Commit each coherent adjustment with a descriptive message.
