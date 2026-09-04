# Dialyn ZZZ Pet — Codex handoff

## Goal

Continue refining a chibi Dialyn ChatGPT Work pet with the user, then upload and activate it only after the user approves the motion preview.

## Current approved baseline

- Final atlas: `assets/final/dialyn-spritesheet-v2.png`
- Sprite version: v2
- Dimensions: 1536 × 2288 px
- Cell size: 192 × 208 px
- Total populated frames: 73
- Standard states: idle, running-right, running-left, waving, jumping, failed, waiting, running, review
- Look directions: 16 directions across the final two rows
- SHA-256: `c05ef888d7941d599bbe0339de08e9936c2fbe954173dfd6ab3e13d0903c093c`
- Local validation: passed
- ChatGPT Pets structural preflight: passed (`valid: true`)

## Review first

- All actions: `assets/previews/all-states.gif`
- Look loop: `assets/previews/look-loop.gif`
- Contact sheet: `assets/previews/contact-sheet.png`
- Direction sheet: `assets/previews/direction-sheet.png`
- Detailed reports: `qa/`

## Character anchors

- Black-and-white braided hair and gold eyes
- Purple vintage telephone handset on the black-hair side
- Teal coiled cord and teal/red/gold accents
- Gold and navy ring weapon
- Chibi sticker style with a clean silhouette at small display size
- Personality: sharp-tongued, calm, dependable, with a playful customer-service flavor

Do not horizontally mirror the running or look-direction artwork because the handset and hair are asymmetric.

## Known QA notes

- Every hard quality gate passed.
- The direction continuity report contains review warnings at the transitions `157.5→180` and `337.5→000`; these are visual pose changes, not gate failures.
- The second look row is slightly more compact to prevent edge clipping.
- The ring weapon is simplified or partially hidden in several small frames to avoid transparent interior-hole false positives.

## Recommended next interaction

1. Show `all-states.gif` and `look-loop.gif`.
2. Ask the user which specific action, expression, size, or accessory needs adjustment.
3. Modify only the relevant source row and rebuild the atlas.
4. Re-run all relevant QA and refresh previews.
5. Show the revised motion and obtain approval.
6. If approved, use the canonical ChatGPT Pets creation workflow to create or update a pet named **Dialyn** and activate it only when requested.

## Source and rights note

Official reference links are recorded in `docs/character-brief.md`. This is a non-commercial fan project; character rights remain with their respective owners.
