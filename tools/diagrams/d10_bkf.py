from dg import *

s = SVG(960, 745, 'BKF: layer order and key binding in hybrid language models',
        'BKF puts the global layer first in each block and binds every key to the three tokens before it with a causal '
        'width-4 convolution, so one attention step links a question to its value. All 11 BKF runs learned key-value '
        'retrieval by step 300, against 13 of 20 global-last hybrids learning at steps 1,100 to 3,600, and BKF kept 98.0% '
        'recall at 64 times the training length against 91% to 92% for global-last hybrids given the same length scale.')

PANEL = tint(INK2, 0.035)
LIN = tint(INK2, 0.10)


def flow(x, y1, y2, color=AXIS):
    s.arrow([(x, y1), (x, y2)], color=color, sw=2, size=11)


def hbar(x0, x1, yc, h, color):
    """Horizontal bar from x0 to x1, rounded at the data end."""
    r, y0, y1 = 4, yc - h / 2, yc + h / 2
    if x1 - x0 < 2 * r:
        s.rect(x0, y0, max(x1 - x0, 3), h, fill=color, rx=1.5)
        return
    s.path(f'M{x0} {y0} L{x1 - r} {y0} Q{x1} {y0} {x1} {y0 + r} L{x1} {y1 - r} Q{x1} {y1} {x1 - r} {y1} L{x0} {y1} Z',
           fill=color)


s.text(24, 46, 'BKF<tspan font-size="23" font-weight="400" fill="#52514e">  ·  layer order and key binding decide when a '
                'hybrid learns to retrieve</tspan>', size=30, weight=800)
s.text(24, 78, 'Fifteen designs, 49 models, one training budget; retrieval tested to 64× the training length.',
       size=18, fill=INK2)

# ---------------------------------------------------------------- panel A: layer order
s.rect(20, 96, 430, 320, fill=PANEL, stroke=AXIS, sw=2, rx=14)
s.text(38, 126, 'Layer order: where the global layer sits', size=19, weight=700)
s.text(235, 150, 'Input enters at the top · block of four, repeated twice', size=13, fill=MUTED, anchor='middle')

cols = [
    (44, 'Standard hybrid', 'LLLS · global last',
     [('gated delta rule', LIN, AXIS), ('gated delta rule', LIN, AXIS), ('gated delta rule', LIN, AXIS),
      ('global softmax', tint(BLUE, 0.16), BLUE)]),
    (250, 'BKF (proposed)', 'SLLL · global first',
     [('global, bound keys', tint(ORANGE, 0.18), ORANGE), ('gated delta rule', LIN, AXIS),
      ('gated delta rule', LIN, AXIS), ('gated delta rule', LIN, AXIS)]),
]
for cx0, name, sub, boxes in cols:
    mid = cx0 + 88
    s.text(mid, 176, name, size=16, weight=700, anchor='middle')
    s.text(mid, 194, sub, size=13, fill=INK2, anchor='middle')
    for i, (lab, fill, stroke) in enumerate(boxes):
        by = 208 + i * 38
        s.rect(cx0, by, 176, 30, fill=fill, stroke=stroke, sw=1.8, rx=8)
        s.text(mid, by + 20, lab, size=14, weight=600, anchor='middle')

s.text(235, 374, '8 layers, width 128, 1.7–1.9M parameters', size=12.5, fill=MUTED, anchor='middle')
s.text(38, 396, 'In BKF, layer 0 reads the embeddings; the global-last layer', size=12.5, fill=INK2)
s.text(38, 412, 'reads what three linear layers are still changing.', size=12.5, fill=INK2)

# ---------------------------------------------------------------- panel B: the bound-key global layer
s.rect(470, 96, 470, 320, fill=PANEL, stroke=AXIS, sw=2, rx=14)
s.text(488, 126, 'The bound-key global layer', size=19, weight=700)

s.rect(605, 140, 200, 28, fill='#ffffff', stroke=AXIS, sw=1.8, rx=14)
s.text(705, 159, 'layer input', size=14, weight=600, anchor='middle')
s.line(705, 168, 705, 174, stroke=AXIS, sw=2)
s.line(560, 174, 850, 174, stroke=AXIS, sw=2)

heads = [(500, 'query'), (645, 'key'), (790, 'value')]
mods = [(500, 'scale × λ', BLUE), (645, '+ conv4', ORANGE), (790, '+ conv4', ORANGE)]
for (hx, lab), (mx, mlab, mcol) in zip(heads, mods):
    flow(hx + 60, 174, 186)
    s.rect(hx, 186, 120, 30, fill='#ffffff', stroke=AXIS, sw=1.8, rx=8)
    s.text(hx + 60, 206, lab, size=14, weight=600, anchor='middle')
    flow(hx + 60, 216, 230, mcol)
    s.rect(mx, 230, 120, 30, fill=tint(mcol, 0.14), stroke=mcol, sw=1.8, rx=8)
    s.text(mx + 60, 250, mlab, size=14, weight=700, anchor='middle', fill=INK)
    flow(mx + 60, 260, 274)

s.rect(500, 274, 410, 38, fill=tint(VIOLET, 0.10), stroke=VIOLET, sw=2, rx=10)
s.text(705, 298, 'softmax attention — no position encoding', size=15, weight=600, anchor='middle')
flow(705, 312, 326)
s.rect(560, 326, 290, 30, fill='#ffffff', stroke=AXIS, sw=1.8, rx=8)
s.text(705, 346, 'output gate → output', size=14, weight=600, anchor='middle')

s.text(488, 378, 'conv4: causal, depthwise, width 4 — binds each key to the three', size=12, fill=INK2)
s.text(488, 394, 'tokens before it, so one step links a question to its value.', size=12, fill=INK2)
s.text(488, 410, 'λ = max(1, log(t+1) / log 256).  BKF adds 2,048 weights.', size=12, fill=INK2)

# ---------------------------------------------------------------- panel C: when retrieval is learned
s.rect(20, 432, 470, 290, fill=PANEL, stroke=AXIS, sw=2, rx=14)
s.text(38, 462, 'When retrieval is learned', size=19, weight=700)

X0, XW = 228, 228
xs = lambda st: X0 + st / 4000 * XW
for t in (0, 1000, 2000, 3000, 4000):
    s.text(xs(t), 486, f'{t:,}', size=11.5, fill=MUTED, anchor='middle')
    s.line(xs(t), 490, xs(t), 494, stroke=AXIS, sw=1.5)
s.line(X0, 494, X0 + XW, 494, stroke=AXIS, sw=1.5)
s.text(X0 + XW / 2, 508, 'training step at which the task is learned', size=11.5, fill=MUTED, anchor='middle')

runs = [
    ('Attention only', '9/9', 300, 1900, BLUE),
    ('Global last (standard)', '13/20', 1100, 3600, tint(INK2, 0.45)),
    ('Global last, bound keys', '8/11', 1100, 3200, AQUA),
    ('BKF (global first)', '11/11', 300, 300, ORANGE),
]
for i, (name, frac, lo, hi, col) in enumerate(runs):
    yc = 534 + i * 42
    s.text(38, yc + 5, name, size=13.5, weight=600 if name.startswith('BKF') else 400)
    s.text(212, yc + 5, frac, size=13, weight=700, anchor='end', fill=col if name.startswith('BKF') else INK2)
    if hi > lo:
        hbar(xs(lo), xs(hi), yc, 16, tint(col, 0.55))
        s.circle(xs(lo), yc, 5.5, col)
        s.circle(xs(hi), yc, 5.5, col)
        s.text(xs(hi) + 9, yc + 5, f'{hi:,}', size=12, fill=MUTED)
    else:
        s.circle(xs(lo), yc, 7, col)
        s.text(xs(lo) + 12, yc + 5, 'all 11 runs by step 300', size=12, weight=600, fill=INK)

s.text(38, 694, 'Global first without bound keys: 1 of 4 runs learned.', size=12, fill=INK2)
s.text(38, 712, 'Sink mass does not predict recall: ρ = 0.49 over 34 runs.', size=12, fill=INK2)

# ---------------------------------------------------------------- panel D: recall on long inputs
s.rect(510, 432, 430, 290, fill=PANEL, stroke=AXIS, sw=2, rx=14)
s.text(528, 462, 'Recall at 64× the training length', size=19, weight=700)
s.text(528, 484, 'exact match on 16,384-token inputs, trained on 256', size=12.5, fill=MUTED)

B0, BW = 700, 190
recall = [
    ('BKF (proposed)', 98.0, ORANGE),
    ('Standard hybrid + scale', 92.1, tint(INK2, 0.45)),
    ('Global last, bound keys', 91.4, AQUA),
    ('Standard hybrid', 50.9, tint(INK2, 0.30)),
]
s.line(B0, 506, B0, 668, stroke=AXIS, sw=1.5)
for i, (name, v, col) in enumerate(recall):
    yc = 522 + i * 42
    s.text(528, yc + 5, name, size=13, weight=600 if i == 0 else 400)
    hbar(B0, B0 + v / 100 * BW, yc, 18, col)
    s.text(B0 + v / 100 * BW + 8, yc + 5, f'{v:.1f}%', size=13, weight=700 if i == 0 else 600)

s.text(528, 694, 'Attention-only designs reach at most 1.1% at 16× the', size=12, fill=INK2)
s.text(528, 712, 'training length, so none of them appears here.', size=12, fill=INK2)

s.save('bkf.svg')
