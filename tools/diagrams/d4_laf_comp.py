from dg import *

s = SVG(960, 640, 'LAF-YOLOv10 composability study',
        'Four modules tested one at a time change mAP@0.5 by -2.0, +1.0, -2.5 and +0.5 (sum -3.0), but stacked they lose 5.5 '
        'points, a -2.5 interaction penalty concentrated in the P2/-P5 head swap. Only 73 of 150 backbone tensors load from the '
        'COCO checkpoint, and TIDE shows the gap is missed detections (+15.4) and classification errors (+7.7).')
PANEL = tint(INK2, 0.035)
LOSS, GAIN = RED, BLUE


def hbar(x0, x1, yc, h, color):
    """Horizontal bar from the zero axis x0 to x1, rounded only at the data end."""
    r, y0, y1 = 4, yc - h / 2, yc + h / 2
    if abs(x1 - x0) < 2 * r:
        s.rect(min(x0, x1), y0, max(abs(x1 - x0), 2), h, fill=color, rx=1)
        return
    if x1 > x0:
        s.path(f'M{x0} {y0} L{x1 - r} {y0} Q{x1} {y0} {x1} {y0 + r} L{x1} {y1 - r} Q{x1} {y1} {x1 - r} {y1} L{x0} {y1} Z', fill=color)
    else:
        s.path(f'M{x0} {y0} L{x1 + r} {y0} Q{x1} {y0} {x1} {y0 + r} L{x1} {y1 - r} Q{x1} {y1} {x1 + r} {y1} L{x0} {y1} Z', fill=color)


def legend(x, y, items):
    for col, lab in items:
        s.rect(x, y - 11, 13, 13, fill=col, rx=3)
        s.text(x + 19, y, lab, size=15, fill=INK2)
        x += 19 + est(lab, 15) + 22


s.text(24, 46, 'LAF-YOLOv10<tspan font-size="23" font-weight="400" fill="#52514e">  ·  do four validated upgrades add up?</tspan>', size=30, weight=800)
s.text(24, 78, 'Measured over 3 seeds on VisDrone-DET2019: <tspan font-weight="700" fill="#0b0b0b">24.0 ± 0.4% mAP@0.5</tspan> vs 31.8% for unmodified YOLOv10n.', size=18, fill=INK2)

# top left: each module alone (diverging bars around zero)
s.rect(20, 96, 440, 222, fill=PANEL, stroke=AXIS, sw=2, rx=14)
s.text(38, 126, 'Alone: one module added to the baseline', size=19, weight=700)
Z, SC = 330, 36
s.line(Z, 144, Z, 288, stroke=AXIS, sw=1.5)
alone = [('PC-C2f', -2.0), ('AG-FPN', 1.0), ('P2 head, −P5', -2.5), ('Wise-IoU v3', 0.5)]
for i, (name, d) in enumerate(alone):
    yc = 164 + i * 36
    s.text(186, yc + 6, name, size=17, fill=INK, anchor='end')
    hbar(Z, Z + d * SC, yc, 20, GAIN if d > 0 else LOSS)
    lab = f'{d:+.1f}'.replace('-', '−')
    s.text(Z + d * SC + (7 if d > 0 else -7), yc + 6, lab, size=16, weight=600, anchor='start' if d > 0 else 'end')
s.text(38, 306, 'Sum of isolated effects:', size=16, fill=INK2)
s.text(222, 306, '−3.0 points', size=16, weight=700)
legend(318, 306, [(LOSS, 'loss'), (GAIN, 'gain')])

# top right: stacked (additive ablation as a step chart)
s.rect(480, 96, 460, 222, fill=PANEL, stroke=AXIS, sw=2, rx=14)
s.text(498, 126, 'Stacked: modules added in sequence', size=19, weight=700)
yv = lambda v: 282 - (v - 25) * 19
cols = [(540, 'base', 31.5), (620, 'PC-C2f', 29.5), (700, 'AG-FPN', 30.5), (780, 'P2, −P5', 25.5), (860, 'WIoU', 26.0)]
for i, (cx, lab, v) in enumerate(cols):
    if i:
        pv = cols[i - 1][2]
        s.line(cols[i - 1][0] + 17, yv(pv), cx - 17, yv(pv), stroke=AXIS, sw=1.5)
        top, bot = min(yv(pv), yv(v)), max(yv(pv), yv(v))
        s.rect(cx - 12, top, 24, max(bot - top, 3), fill=GAIN if v > pv else LOSS, rx=3)
        d = f'{v - pv:+.1f}'.replace('-', '−')
        s.text(cx + 18, (top + bot) / 2 + 6, d, size=15, weight=600)
    s.line(cx - 17, yv(v), cx + 17, yv(v), stroke=INK, sw=2.4)
    s.text(cx, 306, lab, size=15, fill=INK2, anchor='middle')
s.text(540, yv(31.5) - 9, '31.5', size=15, weight=600, anchor='middle')
s.text(860, yv(26.0) + 22, '26.0', size=15, weight=600, anchor='middle')
s.rect(808, 140, 122, 58, fill='#ffffff', stroke=LOSS, sw=1.8, rx=8)
s.text(869, 164, 'interaction', size=15, fill=INK2, anchor='middle')
s.text(869, 187, 'penalty −2.5', size=16, weight=700, anchor='middle')
s.path(f'M818 198 L796 222', stroke=LOSS, sw=1.8)

# bottom left: partial pretrained-weight transplant
s.rect(20, 334, 440, 290, fill=PANEL, stroke=AXIS, sw=2, rx=14)
s.text(38, 364, 'Why: a partial weight transplant', size=19, weight=700)
for k in range(150):
    cx, cy = 40 + (k % 15) * 17, 384 + (k // 15) * 17
    s.rect(cx, cy, 13, 13, fill=BLUE if k < 73 else tint(INK2, 0.16), rx=2.5)
s.text(40, 584, '73 of 150 backbone tensors', size=18, weight=700)
s.text(40, 606, 'shape-match the COCO checkpoint', size=15, fill=INK2)
legend(312, 398, [(BLUE, 'copied')])
legend(312, 424, [(tint(INK2, 0.16), 'random init')])
for j, ln in enumerate(['PC-C2f reshapes', 'backbone channels,', 'so shape-matched', 'loading leaves half', 'the backbone random']):
    s.text(312, 470 + j * 20, ln, size=14, fill=INK2)

# bottom right: TIDE error shift vs YOLOv10n
s.rect(480, 334, 460, 290, fill=PANEL, stroke=AXIS, sw=2, rx=14)
s.text(498, 364, 'Where accuracy went: TIDE error shift', size=19, weight=700)
legend(498, 390, [(LOSS, 'more error than YOLOv10n'), (GAIN, 'less error')])
Z2, SC2 = 630, 11.5
s.line(Z2, 404, Z2, 600, stroke=AXIS, sw=1.5)
tide = [('Miss', 15.4), ('Cls', 7.7), ('Loc', -2.5), ('Both', -1.3), ('Dupe', -0.55), ('Bkg', -8.06)]
for i, (name, d) in enumerate(tide):
    yc = 420 + i * 32
    s.text(498, yc + 6, name, size=16, fill=INK)
    hbar(Z2, Z2 + d * SC2, yc, 18, LOSS if d > 0 else GAIN)
    lab = (f'+{d:g}' if d > 0 else f'−{abs(d):g}')
    s.text(Z2 + d * SC2 + 7 if d > 0 else Z2 + 7, yc + 6, lab, size=15, weight=600)
s.text(Z2 + 190, 610, 'mAP@0.5 penalty, points', size=13, fill=MUTED, anchor='middle')
s.save('laf-yolov10-composability.svg')
