from dg import *
import math

s = SVG(960, 640, 'CANUF: constraint-aware neurosymbolic uncertainty quantification',
        'Constraints are mined from scientific literature into a knowledge graph and verified; a Bayesian neural backbone gives a '
        'predictive distribution; a differentiable constraint layer projects samples that violate physics back onto the feasible '
        'set and widens uncertainty for large corrections. Expected calibration error falls 34.7% versus Bayesian neural networks '
        'with 99.2% constraint satisfaction.')
sub = lambda t, dy=5, fs=13: f'<tspan dy="{dy}" font-size="{fs}">{t}</tspan><tspan dy="{-dy}"> </tspan>'
PANEL = tint(INK2, 0.035)

s.text(24, 46, 'CANUF<tspan font-size="23" font-weight="400" fill="#52514e">  ·  calibrated uncertainty that obeys scientific constraints</tspan>', size=30, weight=800)

P = [(20, 276, ('Constraint', 'extraction')), (318, 240, ('Bayesian', 'backbone')), (580, 360, ('Differentiable', 'constraint layer'))]
for i, (x, w, (a, b)) in enumerate(P):
    s.rect(x, 72, w, 316, fill=PANEL, stroke=AXIS, sw=2, rx=16)
    s.badge(x + 32, 106, i + 1, BLUE)
    s.text(x + 58, 104, f'{a}\n{b}', size=21, weight=700, lh=1.12)
s.arrow([(298, 230), (316, 230)], color=INK2, sw=3, size=11)
s.arrow([(560, 230), (578, 230)], color=INK2, sw=3, size=11)

# 1 - literature -> knowledge graph -> templates -> verified constraints
for k in range(3):
    s.rect(40 + k * 6, 150 + k * 6, 42, 54, fill='#ffffff', stroke=INK2, sw=1.5, rx=3)
for j in range(4):
    s.line(60, 172 + j * 8, 84, 172 + j * 8, stroke=AXIS, sw=2)
s.text(104, 176, 'papers &amp;', size=15, fill=INK2)
s.text(104, 196, 'databases', size=15, fill=INK2)
kg = [(206, 160), (252, 148), (272, 194), (222, 208), (240, 178)]
for a, b in [(0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (4, 2), (1, 4)]:
    s.line(*kg[a], *kg[b], stroke=AXIS, sw=1.8)
for cx, cy in kg:
    s.circle(cx, cy, 7, tint(BLUE, 0.4), stroke=BLUE, sw=1.6)
s.arrow([(172, 182), (192, 182)], color=MUTED, sw=2, size=9)
s.text(238, 234, 'knowledge graph', size=14, fill=INK2, anchor='middle')
s.arrow([(158, 242), (158, 256)], color=MUTED, sw=2, size=9)
s.rect(36, 258, 244, 32, fill='#ffffff', stroke=AXIS, sw=1.6, rx=8)
s.text(158, 279, 'template match · verify', size=15, anchor='middle')
s.rect(36, 298, 244, 50, fill=tint(BLUE, 0.08), stroke=BLUE, sw=1.6, rx=8)
s.text(48, 319, '<tspan font-weight="700">hard</tspan>  thermodynamic · charge', size=14)
s.text(48, 339, '<tspan font-weight="700">soft</tspan>  band gap · density', size=14)
s.chip(36, 356, '91.4% extraction precision', BLUE, size=14, h=24, w=200)

# 2 - Bayesian neural backbone
L = [[(350, y) for y in (160, 200, 240)], [(438, y) for y in (144, 184, 224, 264)], [(526, 204)]]
for la, lb in [(0, 1), (1, 2)]:
    for p in L[la]:
        for q in L[lb]:
            s.line(*p, *q, stroke='#d6d5cf', sw=1.3)
for layer in L:
    for cx, cy in layer:
        s.circle(cx, cy, 9, '#ffffff', stroke=INK2, sw=1.6)
s.path('M372 150 Q384 124 396 150', stroke=BLUE, sw=2.2)
s.math(402, 140, 'q(w)', size=16)
bx, by = 438, 336
s.path(' '.join(('M' if i == 0 else 'L') + f'{bx - 70 + i * 3.5:.1f} {by - 40 * math.exp(-((i - 20) / 7) ** 2):.1f}' for i in range(41)),
       fill=tint(BLUE, 0.15), stroke=BLUE, sw=2)
s.line(bx - 74, by, bx + 74, by, stroke=AXIS, sw=1.5)
s.line(bx, by - 42, bx, by + 4, stroke=INK2, sw=1.4)
s.arrow([(bx, by - 18), (bx + 24, by - 18)], color=INK2, sw=1.6, size=8)
s.math(bx + 28, by - 13, 'σ', size=16)
s.math(bx - 6, by - 46, 'μ', size=16, anchor='end')
s.math(438, 296, 'q(w) ≈ p(w | D)', size=19, anchor='middle')
s.text(438, 370, 'variational inference', size=14, fill=INK2, anchor='middle')

# 3 - projection onto the feasible set, uncertainty widened
A, B = (780, 150), (846, 346)
reg = [(606, 346), (606, 168), A, B]
s.path('M' + ' L'.join(f'{x} {y}' for x, y in reg) + ' Z', fill=tint(BLUE, 0.1), stroke=None)
s.line(*A, *B, stroke=BLUE, sw=2.6)
s.text(640, 206, 'feasible set', size=15, fill=INK2)
s.math(640, 228, 'K', size=18)
dx, dy = B[0] - A[0], B[1] - A[1]
ln = math.hypot(dx, dy)
nx, ny = dy / ln, -dx / ln
s.add('<ellipse cx="846" cy="232" rx="62" ry="44" fill="none" stroke="#52514e" stroke-width="2" stroke-dasharray="7 5"/>')
samples = [(800, 236), (812, 202), (824, 262), (842, 214), (858, 246), (872, 204), (880, 262), (834, 238), (852, 190), (816, 276)]
for px, py in samples:
    dist = (px - A[0]) * nx + (py - A[1]) * ny
    if dist > 0:
        qx, qy = px - dist * nx, py - dist * ny
        s.arrow([(px, py), (qx + nx * 7, qy + ny * 7)], color=RED, sw=1.8, size=8)
        s.circle(px, py, 5, RED)
        s.circle(qx, qy, 5, BLUE, stroke='#ffffff', sw=1.5)
    else:
        s.circle(px, py, 5, BLUE, stroke='#ffffff', sw=1.5)
s.add('<ellipse cx="786" cy="240" rx="34" ry="58" fill="none" stroke="#2a78d6" stroke-width="2.4"/>')
s.math(922, 108, 'ŷ = Π' + sub('K', 5, 13) + '(y)', size=21, anchor='end')
s.line(600, 372, 626, 372, stroke=INK2, sw=2, dash='7 5')
s.text(632, 377, 'raw posterior', size=14, fill=INK2)
s.circle(744, 372, 5, RED)
s.text(754, 377, 'violates K', size=14, fill=INK2)
s.line(838, 372, 862, 372, stroke=BLUE, sw=2.4)
s.text(868, 377, 'projected', size=14, fill=INK2)

# bottom left: explanation
s.rect(20, 404, 380, 220, fill=PANEL, stroke=AXIS, sw=2, rx=16)
s.text(40, 436, 'Explains every correction', size=19, weight=700)
s.path('M42 452 L378 452 Q386 452 386 460 L386 540 Q386 548 378 548 L96 548 L78 568 L80 548 L42 548 Q34 548 34 540 L34 460 Q34 452 42 452 Z',
       fill='#ffffff', stroke=AXIS, sw=1.6)
for j, t in enumerate(['“Prediction moved onto the charge-', 'neutrality boundary; confidence', 'lowered for the larger correction.”']):
    s.text(50, 480 + j * 24, t, size=15, fill=INK)
s.text(40, 604, 'natural-language explanations', size=14, fill=MUTED)
s.text(40, 620, 'generated from constraint violations', size=14, fill=MUTED)

# bottom right: results and datasets
for i, (v, a, b) in enumerate([('−34.7%', 'calibration error', 'vs. Bayesian NNs'),
                               ('99.2%', 'constraints', 'satisfied'),
                               ('+18.3%', 'from constraint-', 'guided recalibration')]):
    x = 416 + i * 178
    s.rect(x, 404, 168, 116, fill=PANEL, stroke=AXIS, sw=2, rx=14)
    s.text(x + 16, 446, v, size=28, weight=700)
    s.text(x + 16, 476, a, size=14, fill=INK2)
    s.text(x + 16, 496, b, size=14, fill=INK2)
s.rect(416, 532, 524, 92, fill=PANEL, stroke=AXIS, sw=2, rx=14)
s.text(434, 562, 'Evaluated on', size=17, weight=700)
cx = 434
for t in ['Materials Project · 140k+', 'QM9', 'climate']:
    cx += s.chip(cx, 578, t, BLUE, size=14, h=28) + 10
s.save('canuf.svg')
