# Dialyn ZZZ Pet — Codex handoff

## Goal and approval boundary

The user explicitly approved the final dynamic effect on 2026-09-04 and requested that `custom:dialyn` be updated and enabled. Release v11 is installed in the local desktop Pets directory, `selected-avatar-id` is `custom:dialyn`, and the avatar overlay is enabled. The desktop still needs one manual **Settings → Pets → Refresh** action before the running UI can be claimed to have loaded the new bytes.

## Current approved release

- Final atlas: `assets/final/dialyn-spritesheet-v2.png`
- Versioned copy: `assets/final/versions/dialyn-spritesheet-v2-release-v11-0accdfdd.png`
- SHA-256: `0accdfdd60269f69309ed91dca5f7eb95471b4ed13eff29ba4f9a26574ec1a90`
- Sprite version: v2
- Dimensions: 1536 × 2288 px
- Cell size: 192 × 208 px
- Frame counts: `[6,8,8,4,5,8,6,6,6,8,8]`
- Total populated frames: 73
- Transparent unused cells: 15

The user-approved v10 motion atlas remains recoverable at `assets/final/versions/dialyn-spritesheet-v2-motion-v10-55050da3.png` with SHA-256 `55050da3ff20912f7c7247f153449cb9122a439dbac73a55531be3aea7646194`. The earlier installed baseline also remains recoverable at `assets/final/versions/dialyn-spritesheet-v2-c05ef888-baseline.png` with SHA-256 `c05ef888d7941d599bbe0339de08e9936c2fbe954173dfd6ab3e13d0903c093c`.

Release v11 corrects the publication pipeline order: final look geometry registration is followed by the single chroma-despill pass and then exact-byte validation. Relative to approved v10, alpha is identical across the whole atlas, rows 0–8 are RGBA-identical, and only edge RGB in look rows 9–10 changed. No approved pose, footprint, landing, silhouette, or animation trajectory changed.

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

## Final review artifacts

- All actions: `assets/previews/all-states.gif`
- Look loop: `assets/previews/look-loop.gif`
- State GIFs: `assets/previews/states/`
- Contact sheet: `assets/previews/contact-sheet.png`
- Direction sheet: `assets/previews/direction-sheet.png`
- Main QA summary: `qa/pet-quality-final-v11.json`
- Project contract: `qa/validation-project-contract-final-v11.json`
- Installed-byte validation: `qa/validation-installed-project-contract-final-v11.json`
- Direction blind validation: `qa/direction-blind-validation-v11.json`
- Release delta: `qa/release-delta-final-v11.json`
- Activation record: `qa/activation-final-v11.json`

## Character anchors

- Black-and-white braided hair and gold eyes
- Purple vintage telephone handset on the black-hair side
- Teal coiled cord and teal/red/gold accents
- Gold and navy ring weapon
- Chibi sticker style with a clean silhouette at small display size
- Personality: sharp-tongued, calm, dependable, with a playful customer-service flavor

Never horizontally mirror an action row: the handset stays on the black-hair side and the long white braid stays opposite.

## QA status

- Exact release SHA-256: `0accdfdd60269f69309ed91dca5f7eb95471b4ed13eff29ba4f9a26574ec1a90`.
- Correct order confirmed: geometry registration → one despill pass → exact-byte validation → previews/QA → local installation.
- Repository 73-frame contract: passed.
- PNG/RGBA, dimensions, frame occupancy, and unused-cell transparency: passed.
- Transparent RGB residue: 0 pixels.
- Chroma fringe: 0 pixels.
- Jump: 38 px airborne lift, 0 px landing error.
- Look registration: 0.5 px maximum center drift; 1.08 maximum width ratio; all 16 sprites are 192 px high with baseline y=203.
- Fresh three-reviewer blind direction QA: all 28 A/B cells were unanimous 3/3, including the `090/270` and `000/180` hard cardinal gates; no result was ambiguous or unconfirmed.
- Direction continuity: passed with visual-review notes at the `157.5→180` and `337.5→000` expression seams and for legitimate transparent holes inside the ring weapon.
- Standard-frame review: passed. `jumping` and `failed` intentionally use the documented `stable-slots` extraction policy.

Compatibility note: the current bundled `hatch-pet` validator additionally expects an occupied neutral cell at `idle[6]`. This conflicts with this repository's explicit 73-frame contract, where `idle` has six frames and every unused cell must be transparent. `qa/validation-hatch-pet-compat-final-v11.json` preserves that single expected failure; no other hatch error or warning remains.

## Local installation and next interaction

- Manifest: `C:/Users/c4esa/.codex/pets/dialyn/pet.json`
- Installed atlas: `C:/Users/c4esa/.codex/pets/dialyn/spritesheet.png`
- Stable ID: `custom:dialyn`
- Installed bytes match the approved release SHA exactly.
- `custom:dialyn` is selected and the desktop avatar overlay is enabled.
- The app's local-pet resource cache has not been refreshed non-interactively. Ask the user to click **Settings → Pets → Refresh** once, then visually confirm that Dialyn reloads. Do not require deletion or recreation.
- If a later row changes, replace only that row, rebuild the atlas/previews/QA, retain this release, and commit the adjustment separately.

## Source and rights note

Official reference links are recorded in `docs/character-brief.md`. This is a non-commercial fan project; character rights remain with their respective owners.
