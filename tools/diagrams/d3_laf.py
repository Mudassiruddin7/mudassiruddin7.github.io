from dg import *

s = SVG(960, 640, 'LAF-YOLOv10 architecture',
        'YOLOv10n modified at three levels: PC-C2f blocks in the backbone, an Attention-Guided FPN neck with SE-gated lateral '
        'connections and DySample upsampling, and detection heads at P2, P3 and P4 with the P5 head removed; Wise-IoU v3 '
        'supervises box regression. 35.1% mAP@0.5 on VisDrone-DET2019 with 2.3M parameters, 24.3 FPS on Jetson Orin Nano.')
sub = lambda t, dy=5, fs=13: f'<tspan dy="{dy}" font-size="{fs}">{t}</tspan><tspan dy="{-dy}"> </tspan>'
NECK, HEAD = VIOLET, AQUA

s.text(24, 46, 'LAF-YOLOv10<tspan font-size="23" font-weight="400" fill="#52514e">  ·  four plug-in upgrades to YOLOv10n for tiny aerial objects</tspan>', size=30, weight=800)
for x, col, lab in [(168, BLUE, 'Backbone'), (438, NECK, 'Neck'), (668, HEAD, 'Heads')]:
    s.rect(x, 64, 12, 12, fill=col, rx=3)
    s.text(x + 18, 75, lab, size=16, weight=600, fill=INK2)

R = [118, 204, 290, 376]
res = ['160×160 · 32 ch', '80×80 · 64 ch', '40×40 · 128 ch', '20×20 · 256 ch']

# input aerial frame with tiny objects
s.rect(20, 118, 120, 120, fill='#9aa39a', rx=6)
s.rect(20, 166, 120, 22, fill='#6c706b')
s.rect(72, 118, 20, 120, fill='#6c706b')
for cx, cy, c, hit in [(34, 172, '#f2f2f2', 1), (52, 180, '#d94f3d', 0), (112, 170, '#2b2b2b', 1), (126, 180, '#e8c547', 0),
                       (76, 132, '#f2f2f2', 1), (84, 214, '#3d6fd9', 1), (78, 150, '#2b2b2b', 0)]:
    s.rect(cx, cy, 8, 5, fill=c, rx=1)
    if hit:
        s.rect(cx - 3, cy - 3, 14, 11, fill='none', stroke=HEAD, sw=1.6, rx=1)
s.text(80, 258, '640 × 640 frame', size=15, fill=INK2, anchor='middle')
s.text(80, 278, 'objects &lt; 8×8 px', size=15, fill=INK2, anchor='middle')
s.arrow([(142, 150), (166, 124)], color=INK2, sw=2.6, size=12)

# backbone: PC-C2f stages + SPPF
for k, y in enumerate(R):
    s.rect(168, y - 32, 200, 64, fill=tint(BLUE, 0.09), stroke=BLUE, sw=2, rx=10)
    s.text(182, y - 6, f'PC-C2f · stage {k + 1}', size=18, weight=700)
    s.text(182, y + 18, res[k], size=16, fill=INK2)
    if k < 3:
        s.arrow([(268, y + 33), (268, R[k + 1] - 34)], color=BLUE, sw=2.4, size=10)
s.arrow([(268, R[3] + 33), (268, 422)], color=BLUE, sw=2.4, size=10)
s.rect(208, 424, 120, 52, fill=tint(BLUE, 0.09), stroke=BLUE, sw=2, rx=10)
s.text(268, 457, 'SPPF', size=18, weight=700, anchor='middle')

# neck: SE-gated laterals (dashed blue) + DySample top-down fusion (solid violet)
for k in range(3):
    y = R[k]
    s.arrow([(370, y), (436, y)], color=BLUE, sw=2.2, dash='6 5', size=11)
    s.circle(403, y, 15, '#ffffff', stroke=BLUE, sw=2)
    s.text(403, y + 5, 'SE', size=13, weight=700, anchor='middle')
    s.rect(438, y - 32, 160, 64, fill=tint(NECK, 0.08), stroke=NECK, sw=2, rx=10)
    s.text(452, y - 6, 'AG-FPN', size=18, weight=700)
    s.text(452, y + 18, res[k].split(' · ')[0], size=16, fill=INK2)
s.arrow([(330, 450), (518, 450), (518, R[2] + 34)], color=NECK, sw=2.8, size=12)
s.text(528, 418, 'DySample ↑2', size=15, fill=INK2)
for k in (2, 1):
    s.arrow([(518, R[k] - 33), (518, R[k - 1] + 34)], color=NECK, sw=2.8, size=10)
    s.text(528, (R[k] + R[k - 1]) / 2 + 5, '↑2', size=15, fill=INK2)

# heads: P2 added, P5 removed
heads = [('Detect P2', 'stride 4 · added'), ('Detect P3', 'stride 8'), ('Detect P4', 'stride 16')]
for k in range(3):
    y = R[k]
    s.arrow([(600, y), (666, y)], color=INK2, sw=2.4, size=11)
    s.rect(668, y - 32, 180, 64, fill=tint(HEAD, 0.12 if k == 0 else 0.07), stroke=HEAD, sw=2.6 if k == 0 else 2, rx=10)
    s.text(682, y - 6, heads[k][0], size=18, weight=700)
    s.text(682, y + 18, heads[k][1], size=16, fill=INK2)
s.rect(668, R[3] - 32, 180, 64, fill='#ffffff', stroke=MUTED, sw=2, rx=10, dash='7 6')
s.text(682, R[3] - 6, 'P5 head', size=18, weight=700, fill=MUTED)
s.line(680, R[3] - 12, 758, R[3] - 12, stroke=MUTED, sw=2)
s.text(682, R[3] + 18, 'removed', size=16, fill=MUTED)
s.path(f'M862 86 L872 86 L872 322 L862 322', stroke=INK2, sw=2)
s.add(f'<text x="0" y="0" transform="translate(900 204) rotate(-90)" font-family="{FONT}" font-size="16" '
      f'fill="{INK2}" text-anchor="middle">regression: Wise-IoU v3</text>')

# insets: (a) PC-C2f, (b) AG-FPN fusion, (c) results
PANEL = tint(INK2, 0.035)
for x, w, t in [(20, 330, '(a) PC-C2f block'), (366, 330, '(b) AG-FPN fusion'), (712, 228, '(c) VisDrone-DET2019')]:
    s.rect(x, 496, w, 128, fill=PANEL, stroke=AXIS, sw=2, rx=14)
    s.text(x + 16, 524, t, size=18, weight=700)
s.chip(254, 506, '−75% FLOPs', BLUE, size=14, h=26, w=88)
s.math(40, 582, 'X', size=22)
s.arrow([(58, 575), (80, 575), (80, 556), (104, 556)], color=INK2, sw=2, size=9)
s.arrow([(80, 575), (80, 600), (206, 600), (220, 586)], color=INK2, sw=2, size=9)
s.rect(106, 540, 92, 32, fill=tint(BLUE, 0.12), stroke=BLUE, sw=1.6, rx=6)
s.text(152, 561, '3×3 conv', size=15, weight=600, anchor='middle')
s.text(152, 620, 'C/4 conv · 3C/4 pass', size=13, fill=INK2, anchor='middle')
s.arrow([(198, 556), (218, 568)], color=INK2, sw=2, size=9)
s.circle(230, 576, 12, '#ffffff', stroke=INK2, sw=1.6)
s.text(230, 581, 'C', size=13, weight=700, anchor='middle')
s.arrow([(242, 576), (262, 576)], color=INK2, sw=2, size=9)
s.rect(264, 560, 50, 32, fill=tint(BLUE, 0.12), stroke=BLUE, sw=1.6, rx=6)
s.text(289, 581, '1×1', size=15, weight=600, anchor='middle')
s.math(322, 582, 'Y', size=22)

s.math(382, 562, 'F' + sub('i'), size=20)
s.arrow([(404, 556), (422, 556)], color=INK2, sw=2, size=9)
s.rect(424, 540, 92, 32, fill=tint(NECK, 0.1), stroke=NECK, sw=1.6, rx=6)
s.text(470, 561, 'SE gate', size=15, weight=600, anchor='middle')
s.arrow([(516, 556), (536, 556)], color=INK2, sw=2, size=9)
s.circle(548, 556, 11, '#ffffff', stroke=INK2, sw=1.6)
s.text(548, 561, '×', size=16, weight=700, anchor='middle')
s.math(382, 606, 'F' + sub('i+1'), size=20)
s.arrow([(418, 600), (434, 600)], color=INK2, sw=2, size=9)
s.rect(436, 584, 110, 32, fill=tint(NECK, 0.1), stroke=NECK, sw=1.6, rx=6)
s.text(491, 605, 'DySample ↑2', size=15, weight=600, anchor='middle')
s.arrow([(559, 560), (604, 574)], color=INK2, sw=2, size=9)
s.arrow([(546, 600), (604, 584)], color=INK2, sw=2, size=9)
s.circle(616, 578, 12, '#ffffff', stroke=INK2, sw=1.6)
s.text(616, 583, 'C', size=13, weight=700, anchor='middle')
s.arrow([(628, 578), (650, 578)], color=INK2, sw=2, size=9)
s.math(658, 585, 'F′' + sub('i'), size=20)

for y, v, lab in [(560, '35.1%', 'mAP@0.5 (+3.3)'), (588, '2.3M', 'parameters'), (616, '24.3', 'FPS, Orin Nano')]:
    s.text(728, y, v, size=22, weight=700)
    s.text(812, y, lab, size=15, fill=INK2)
s.save('laf-yolov10.svg')
