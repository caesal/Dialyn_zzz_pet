# Dialyn ZZZ Pet — Codex handoff

## Goal and approval boundary

Continue refining the chibi Dialyn（琉音）pet with the user. The refreshed motion set is ready for visual review, but it is **not yet user-approved**. Do not upload, create, update, select, or activate a ChatGPT Pet until the user explicitly confirms the final dynamic effect.

## Current motion-review candidate

- Final atlas: `assets/final/dialyn-spritesheet-v2.png`
- Versioned copy: `assets/final/versions/dialyn-spritesheet-v2-motion-v10-55050da3.png`
- SHA-256: `55050da3ff20912f7c7247f153449cb9122a439dbac73a55531be3aea7646194`
- Sprite version: v2
- Dimensions: 1536 × 2288 px
- Cell size: 192 × 208 px
- Frame counts: `[6,8,8,4,5,8,6,6,6,8,8]`
- Total populated frames: 73
- Transparent unused cells: 15

The last user-validated baseline remains recoverable at `assets/final/versions/dialyn-spritesheet-v2-c05ef888-baseline.png` with SHA-256 `c05ef888d7941d599bbe0339de08e9936c2fbe954173dfd6ab3e13d0903c093c`.

## Motion design in this candidate

- `idle`: stable-footprint drowsy customer-service fidget with smooth eyelid and weight motion; no whole-character shrink.
- `running-right`: eight-pose rightward gait with leg exchange, airborne beats, braid/cord follow-through, and a stable ground seam.
- `running-left`: independently drawn eight-pose leftward gait; it is not a reflected rightward row.
- `waving`: greeting wave with bow, knee bend, hip shift, and lower-body follow-through.
- `jumping`: the approved five-pose jump retained, with the authored vertical arc preserved.
- `failed`: side-lying defeated loop with a small elbow-braced recovery attempt and gradual buckle.
- `waiting`: seated on the ring weapon with palm-up asking, foot tap, weight shift, and handset check.
- `running`: planted task-processing loop with handset listening, nodding, routing gesture, lean, and ring follow-through; no locomotion.
- `review`: standing scan, analytical head tilt, confident acknowledgement, and lower-body rebalance.
- `look directions`: 16 whole-head and eye directions with readable cardinal/intercardinal turns while the body stays planted; no whole-character orbit, mirrored asymmetry, or ghost silhouettes.

The v2 host contract does not support 10-second, 30-fps source rows or a five-minute random idle scheduler. This candidate follows the user-selected fixed-v2 approach and uses the available 4–8 authored poses per state.

## Review first

- All actions: `assets/previews/all-states.gif`
- Look loop: `assets/previews/look-loop.gif`
- State GIFs: `assets/previews/states/`
- Contact sheet: `assets/previews/contact-sheet.png`
- Direction sheet: `assets/previews/direction-sheet.png`
- Main QA summary: `qa/pet-quality-final-v10.json`
- Project contract: `qa/validation-project-contract-final-v10.json`
- Direction blind validation: `qa/direction-blind-validation-v10.json`

## Character anchors

- Black-and-white braided hair and gold eyes
- Purple vintage telephone handset on the black-hair side
- Teal coiled cord and teal/red/gold accents
- Gold and navy ring weapon
- Chibi sticker style with a clean silhouette at small display size
- Personality: sharp-tongued, calm, dependable, with a playful customer-service flavor

Never horizontally mirror an action row: the handset stays on the black-hair side and the long white braid stays opposite.

## QA status

- Repository 73-frame contract: passed.
- PNG/RGBA, dimensions, frame occupancy, and unused-cell transparency: passed.
- Transparent RGB residue: 0 pixels.
- Chroma fringe: 0 pixels.
- Jump: 38 px airborne lift, 0 px landing error.
- Look registration: 0.5 px maximum center drift; 1.08 maximum width ratio; all 16 sprites are 192 px high with baseline y=203.
- Three-reviewer blind direction QA: reviewers 1 and 2 matched all 28 A/B cells. Reviewer 3 reversed both cells in the oblique `horizontal-1` pair and marked eight other oblique cells ambiguous. Strict-majority consensus still confirmed all 28 cells, including unanimous hard cardinal gates, so no consensus result remained unconfirmed.
- Direction continuity: passed with visual-review notes at the `157.5→180` and `337.5→000` expression seams and for legitimate transparent holes inside the ring weapon.
- Standard-frame review: passed. `jumping` and `failed` intentionally use the documented `stable-slots` extraction policy.

Compatibility note: the current bundled `hatch-pet` validator additionally expects an occupied neutral cell at `idle[6]`. This conflicts with this repository's explicit 73-frame contract, where `idle` has six frames and every unused cell must be transparent. `qa/validation-hatch-pet-compat-final-v10.json` preserves that single expected failure; no other hatch error or warning remains.

## Next interaction

1. Show the user `all-states.gif`, `look-loop.gif`, and any requested state GIFs.
2. Obtain explicit approval or a request for another row-specific change.
3. If a row changes, replace only that row, rebuild the atlas/previews/QA, retain the current version, and commit the adjustment separately.
4. Only after explicit motion approval, use the official Pets workflow to validate the exact final bytes, create or update the pet as **Dialyn**, enable/select it if requested, and verify the stable pet ID.

## Source and rights note

Official reference links are recorded in `docs/character-brief.md`. This is a non-commercial fan project; character rights remain with their respective owners.
