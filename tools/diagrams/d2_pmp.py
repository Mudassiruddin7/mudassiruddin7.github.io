from dg import *

s = SVG(960, 640, 'PMP-DACIS: disease-aware pruning for few-shot plant pathology',
        'A pre-trained ResNet-18 (11.2M parameters) is pruned 40% using Disease-Aware Channel Importance Scores, meta-trained '
        'on few-shot tasks, then pruned again with scores re-weighted by meta-gradients, reaching 2.5M parameters that run at '
        '7 FPS on a Raspberry Pi 4 while keeping 92.3% of full accuracy.')
sub = lambda t, dy=6, fs=15: f'<tspan dy="{dy}" font-size="{fs}">{t}</tspan><tspan dy="{-dy}"> </tspan>'
PANEL = tint(INK2, 0.035)

s.text(24, 48, 'PMP-DACIS<tspan font-size="23" font-weight="400" fill="#52514e">  ·  disease-aware pruning meets few-shot meta-learning</tspan>', size=31, weight=800)

# input: leaf photo + full model
s.path('M86 118 C 38 150, 40 222, 86 252 C 132 222, 134 150, 86 118 Z', fill=tint(GREEN, 0.22), stroke=GREEN, sw=2.4)
s.line(86, 128, 86, 246, stroke=GREEN, sw=1.8)
for cx, cy, r in [(66, 176, 7), (104, 198, 9), (74, 214, 5), (100, 160, 5)]:
    s.circle(cx, cy, r, '#8a5a2b', op=0.75)
s.text(86, 280, 'leaf photo', size=18, fill=INK2, anchor='middle')
s.rect(26, 300, 120, 72, fill='#ffffff', stroke=INK2, sw=1.8, rx=10)
s.text(86, 328, 'ResNet-18', size=19, weight=700, anchor='middle')
s.text(86, 358, '11.2M params', size=17, fill=INK2, anchor='middle')
s.arrow([(150, 243), (172, 243)], color=INK2, sw=3, size=13)

XS, PW, Y0, PH = [176, 438, 700], 240, 76, 334
heads = [('DACIS score', 'prune 40%'), ('Episodic', 'meta-learning'), ('Meta-gradient', 're-prune 38%')]
for i, x in enumerate(XS):
    s.rect(x, Y0, PW, PH, fill=PANEL, stroke=AXIS, sw=2, rx=16)
    s.badge(x + 32, Y0 + 34, i + 1, BLUE)
    s.text(x + 58, Y0 + 32, f'{heads[i][0]}\n{heads[i][1]}', size=21, weight=700, lh=1.12)
    if i < 2:
        s.arrow([(x + PW + 3, 243), (x + PW + 20, 243)], color=INK2, sw=3, size=12)


def strip(x, base, heights, keep, gone=(), thr=None):
    for k, hgt in enumerate(heights):
        bx = x + 20 + k * 16
        if k in gone:
            s.rect(bx, base - 10, 11, 10, fill='none', stroke=AXIS, sw=1.3, rx=2, dash='3 2')
            continue
        on = k in keep
        s.path(f'M{bx} {base} L{bx} {base - hgt + 3} Q{bx} {base - hgt} {bx + 3} {base - hgt} L{bx + 8} {base - hgt} '
               f'Q{bx + 11} {base - hgt} {bx + 11} {base - hgt + 3} L{bx + 11} {base} Z', fill=BLUE if on else tint(INK2, 0.22))
    s.line(x + 14, base + 1, x + 213, base + 1, stroke=AXIS, sw=1.5)
    if thr:
        s.line(x + 14, base - thr, x + 213, base - thr, stroke=INK2, sw=1.6, dash='6 5')
        s.math(x + 216, base - thr + 6, 'τ<tspan dy="5" font-size="13">ℓ</tspan>', size=19)


# 1 - DACIS scoring and conservative pruning
x = XS[0]
h1 = [70, 28, 62, 80, 22, 55, 34, 76, 18, 66, 48, 30]
keep1 = {k for k, v in enumerate(h1) if v > 38}
strip(x, 262, h1, keep1, thr=38)
s.rect(x + 26, 280, 12, 12, fill=BLUE, rx=2)
s.text(x + 44, 291, 'keep', size=16, fill=INK2)
s.rect(x + 96, 280, 12, 12, fill=tint(INK2, 0.22), rx=2)
s.text(x + 114, 291, 'prune', size=16, fill=INK2)
s.math(x + PW / 2, 330, '0.3 G + 0.2 V + 0.5 D', size=22, anchor='middle')
s.text(x + PW / 2, 354, 'gradient · variance · Fisher', size=16, fill=INK2, anchor='middle')
s.chip(x + 38, 368, '11.2M → 6.7M', BLUE, size=19, h=32, w=164)

# 2 - episodic meta-learning: inner loop adapts on S, outer loop updates on Q
x = XS[1]
for cx, lab, sym in [(x + 64, 'support', 'S'), (x + 176, 'query', 'Q')]:
    s.rect(cx - 48, 158, 96, 62, fill='#ffffff', stroke=INK2, sw=1.6, rx=10)
    for k in range(3):
        s.rect(cx - 36 + k * 26, 168, 20, 20, fill=tint(GREEN, 0.3), stroke=GREEN, sw=1.2, rx=4)
    s.text(cx, 211, f'{lab} <tspan font-family="{MATH}" font-style="italic">{sym}</tspan>', size=17, fill=INK2, anchor='middle')
s.circle(x + 64, 290, 22, tint(BLUE, 0.2), stroke=BLUE, sw=2)
s.math(x + 64, 298, 'θ', size=24, anchor='middle')
s.circle(x + 176, 290, 22, tint(BLUE, 0.2), stroke=BLUE, sw=2)
s.math(x + 176, 298, 'θ′', size=24, anchor='middle')
s.carrow(f'M{x + 88} 281 Q{x + 120} 258 {x + 150} 281', color=BLUE, sw=2.6, size=12)
s.text(x + 120, 254, 'adapt on S', size=16, fill=INK2, anchor='middle')
s.carrow(f'M{x + 152} 301 Q{x + 120} 326 {x + 90} 301', color=BLUE, sw=2.6, size=12)
s.text(x + 120, 342, 'update on Q', size=16, fill=INK2, anchor='middle')
s.chip(x + 30, 368, '2,000 few-shot tasks', BLUE, size=18, h=32, w=180)

# 3 - meta-gradient re-ranking and final prune
x = XS[2]
s.math(x + PW / 2, 170, 'DACIS · |G<tspan dy="5" font-size="14">meta</tspan><tspan dy="-5">|</tspan>', size=23, anchor='middle')
h3 = {0: 30, 2: 74, 3: 26, 5: 34, 7: 62, 9: 22, 10: 78}
heights = [h3.get(k, 10) for k in range(12)]
strip(x, 290, heights, {2, 7, 10}, gone={k for k in range(12) if k not in h3}, thr=40)
s.text(x + PW / 2, 318, 'rankings change after', size=16, fill=INK2, anchor='middle')
s.text(x + PW / 2, 338, 'few-shot adaptation', size=16, fill=INK2, anchor='middle')
s.chip(x + 38, 368, '6.7M → 2.5M', BLUE, size=19, h=32, w=164)

# bottom left: taxonomy-aware protection
s.rect(20, 428, 450, 194, fill=PANEL, stroke=AXIS, sw=2, rx=16)
s.text(42, 464, 'Disease taxonomy guards channels', size=21, weight=700)


def shield(cx, cy, fill, stroke):
    s.path(f'M{cx} {cy - 15} L{cx + 13} {cy - 9} L{cx + 13} {cy + 1} C{cx + 13} {cy + 9} {cx + 7} {cy + 14} {cx} {cy + 17} '
           f'C{cx - 7} {cy + 14} {cx - 13} {cy + 9} {cx - 13} {cy + 1} L{cx - 13} {cy - 9} Z', fill=fill, stroke=stroke, sw=2)


s.line(58, 506, 58, 590, stroke=AXIS, sw=2)
rows = [(506, BLUE, BLUE, 'Pathogen type', 'protected'), (552, tint(BLUE, 0.35), BLUE, 'Symptom type', 'partly protected'),
        (598, '#ffffff', MUTED, 'Specific disease', 'prunable')]
for i, (cy, f, st, a, b) in enumerate(rows):
    if i:
        s.line(58, cy, 80, cy, stroke=AXIS, sw=2)
    shield(98, cy, f, st)
    s.text(124, cy + 7, f'{a}<tspan fill="#52514e" font-weight="400">  ·  {b}</tspan>', size=19, weight=700)
s.text(446, 506 + 7, 'coarse', size=15, fill=MUTED, anchor='end')
s.text(446, 598 + 7, 'fine', size=15, fill=MUTED, anchor='end')

# bottom right: deployment on Raspberry Pi 4
s.rect(490, 428, 450, 194, fill=PANEL, stroke=AXIS, sw=2, rx=16)
s.text(512, 464, 'Runs in the field', size=21, weight=700)
s.rect(512, 492, 138, 104, fill=tint(GREEN, 0.28), stroke=GREEN, sw=2, rx=8)
for k in range(10):
    s.rect(524 + k * 11.5, 500, 7, 7, fill=YELLOW, rx=1.5)
s.rect(548, 526, 40, 40, fill='#3a3a38', rx=4)
s.rect(628, 520, 26, 22, fill='#b9b8b1', stroke=INK2, sw=1.2, rx=2)
s.rect(628, 556, 26, 22, fill='#b9b8b1', stroke=INK2, sw=1.2, rx=2)
s.text(581, 616, 'Raspberry Pi 4', size=16, fill=INK2, anchor='middle')
for y, val, lab in [(512, '−78%', 'size, 11.2M → 2.5M'), (560, '92.3%', 'of full accuracy'), (608, '7 FPS', 'real-time, 142 ms')]:
    s.text(676, y, val, size=29, weight=700)
    s.text(778, y, lab, size=17, fill=INK2)
s.save('pmp-dacis.svg')
