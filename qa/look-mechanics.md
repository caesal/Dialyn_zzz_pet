# Dialyn look-direction mechanics

## Natural motion

Dialyn looks around as a planted, living character rather than as a rotated sticker. Her gold pupils lead the gaze, her eyelids reshape, then her head turns or nods a small amount through the neck. The upper torso and shoulders provide only a restrained counter-shift. Both feet, pelvis, lowest contact line, overall body height, and the gold/navy ring's ground contact stay locked. The purple handset remains attached on the black-hair side; the teal cord bends continuously and lags the head by a fraction of one step. The black and white braids follow with tiny inertia but never swap sides. There is exactly one crisp silhouette per pose: no duplicate outlines, ghost images, blur, afterimages, or motion trails.

## Cardinal pose families

- `000 up`: broadly frontal. Gold pupils sit high, upper lids open slightly, chin lifts a little, and the upper chest follows upward. Black hair/handset stays on screen-left and the long white braid stays on screen-right. Feet and ring remain unchanged.
- `090 screen-right`: nose tip and both pupils move unmistakably toward the viewer's screen-right. The white-braid side becomes the leading/more open side of the face while the black-hair/handset side compresses slightly in perspective; the handset never detaches or changes sides. Shoulders turn only enough to support the head.
- `180 down`: broadly frontal. Pupils sit low, upper lids lower slightly, chin tucks, and shoulders soften a little. Braids and cord settle forward by a small continuous amount. Feet, pelvis, scale, and ring contact remain unchanged.
- `270 screen-left`: nose tip and both pupils move unmistakably toward the viewer's screen-left. The black-hair/handset side becomes the leading/more open side while the long white-braid side recedes slightly; the white braid remains opposite the handset. This is independently drawn directional anatomy, not a mirror of `090`.

## Per-step motion budget

Every adjacent 22.5-degree step uses a similar visual increment. At final 192x208 size: pupil travel is about 1-2 px per step; head-center travel is at most 1.5 px; head-angle change is at most about 3 degrees; shoulder/upper-torso counter-shift is at most 1.5 px; braid and cord tips may lag by at most 3 px. The lowest opaque contact line may move by at most 1 px, body height by at most 2 percent, and the ring's planted outer edge by at most 2 px. Do not compensate by scaling, skewing, rotating, or translating the whole character.

## Seam requirements

`157.5 -> 180` must be one ordinary down-right-to-down step, not a redraw or size jump. `337.5 -> 000` must be one ordinary up-left-to-up step. The face construction, eye size, braid attachment points, handset placement, cord continuity, ring geometry, scale, baseline, and line sharpness must remain continuous at both row boundaries.
