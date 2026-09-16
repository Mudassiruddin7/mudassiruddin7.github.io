from dg import *

s = SVG(960, 640, 'CryptoFair-FL: verifiable fairness in federated learning',
        'Each institution computes group-conditional prediction counts locally and sends only Paillier ciphertexts. A secure '
        'aggregator adds them homomorphically with a batched O(n log n) protocol, and a fairness verifier checks demographic '
        'parity and equalized odds under (0.5, 1e-6) differential privacy, feeding the result back into training.')
sub = lambda t, dy=5, fs=13: f'<tspan dy="{dy}" font-size="{fs}">{t}</tspan><tspan dy="{-dy}"> </tspan>'
PANEL = tint(INK2, 0.035)
CIPH = VIOLET

s.text(24, 46, 'CryptoFair-FL<tspan font-size="23" font-weight="400" fill="#52514e">  ·  verify fairness without seeing anyone’s data</tspan>', size=30, weight=800)


def lock(x, y, col, sc=1.0):
    s.path(f'M{x + 3 * sc} {y} v{-4 * sc} a{4 * sc} {4 * sc} 0 0 1 {8 * sc} 0 v{4 * sc}', stroke=col, sw=2)
    s.rect(x, y, 14 * sc, 11 * sc, fill=col, rx=2)


# feedback loop (dashed) from verifier back to institutions
s.arrow([(795, 100), (795, 78), (145, 78), (145, 98)], color=BLUE, sw=2.4, dash='8 6', size=12)
s.text(470, 70, 'fairness feedback → model update', size=15, fill=INK2, anchor='middle')

# institutions
for cy, name in [(156, 'Hospital 1'), (286, 'Hospital 2'), (452, 'Hospital n')]:
    y = cy - 56
    s.rect(20, y, 250, 112, fill=PANEL, stroke=AXIS, sw=2, rx=14)
    s.rect(38, y + 30, 40, 48, fill='#ffffff', stroke=INK2, sw=1.8, rx=3)
    s.path(f'M34 {y + 32} L58 {y + 16} L82 {y + 32}', stroke=INK2, sw=1.8)
    s.rect(54, y + 44, 8, 22, fill=INK2, rx=1)
    s.rect(47, y + 51, 22, 8, fill=INK2, rx=1)
    s.text(94, y + 44, name, size=19, weight=700)
    lock(96, y + 70, INK2, 0.9)
    s.text(116, y + 80, 'data stays local', size=14, fill=INK2)
    for k, a in enumerate([0.55, 0.2, 0.3, 0.7]):
        s.rect(200 + (k % 2) * 24, y + 28 + (k // 2) * 24, 20, 20, fill=tint(BLUE, a), rx=3)
    s.text(222, y + 96, 'counts', size=13, fill=MUTED, anchor='middle')
    # ciphertext on the wire
    s.arrow([(272, cy), (292, cy)], color=CIPH, sw=2.4, size=10)
    s.rect(294, cy - 17, 106, 34, fill=tint(CIPH, 0.1), stroke=CIPH, sw=1.8, rx=17)
    lock(306, cy - 2, CIPH, 0.85)
    s.math(362, cy + 6, 'Enc(s' + sub(name[-1], 4, 12) + ')', size=17, anchor='middle')
    s.arrow([(400, cy), (418, cy)], color=CIPH, sw=2.4, size=10)
s.text(145, 364, '⋮', size=28, fill=MUTED, anchor='middle')

# secure aggregator: homomorphic addition tree
s.rect(420, 100, 196, 408, fill=tint(CIPH, 0.06), stroke=CIPH, sw=2.2, rx=14)
s.text(518, 134, 'Secure', size=20, weight=700, anchor='middle')
s.text(518, 158, 'aggregator', size=20, weight=700, anchor='middle')
leaves = [456, 496, 540, 580]
for i, lx in enumerate(leaves):
    s.line(lx, 236, (476 if i < 2 else 560), 296, stroke=CIPH, sw=2)
    s.rect(lx - 10, 214, 20, 22, fill='#ffffff', stroke=CIPH, sw=1.6, rx=3)
    lock(lx - 6, 226, CIPH, 0.6)
for nx in (476, 560):
    s.line(nx, 296, 518, 350, stroke=CIPH, sw=2)
for nx, ny, r in [(476, 296, 15), (560, 296, 15), (518, 350, 17)]:
    s.circle(nx, ny, r, '#ffffff', stroke=CIPH, sw=2)
    s.text(nx, ny + 7, '⊕', size=21, weight=700, fill=CIPH, anchor='middle')
s.line(518, 367, 518, 384, stroke=CIPH, sw=2)
s.rect(462, 384, 112, 34, fill=tint(CIPH, 0.12), stroke=CIPH, sw=1.8, rx=17)
s.math(518, 407, 'Enc(Σ s)', size=18, anchor='middle')
s.text(518, 452, 'Paillier, 2048-bit', size=15, fill=INK2, anchor='middle')
s.text(518, 476, 'batched ⊕ tree', size=15, fill=INK2, anchor='middle')
s.arrow([(618, 222), (646, 222)], color=INK2, sw=2.6, size=12)

# fairness verifier
s.rect(650, 100, 290, 248, fill=tint(BLUE, 0.07), stroke=BLUE, sw=2.2, rx=14)
s.text(668, 132, 'Fairness verifier', size=20, weight=700)
s.chip(668, 146, '+ DP noise  ε = 0.5, δ = 10⁻⁶', CIPH, size=15, h=28, w=236)
s.line(740, 206, 740, 282, stroke=INK2, sw=2.4)
s.path('M716 284 L764 284', stroke=INK2, sw=3)
s.line(700, 214, 780, 206, stroke=INK2, sw=2.4)
for px, py, lab in [(700, 214, 'a = 0'), (780, 206, 'a = 1')]:
    s.line(px, py, px - 16, py + 34, stroke=MUTED, sw=1.4)
    s.line(px, py, px + 16, py + 34, stroke=MUTED, sw=1.4)
    s.path(f'M{px - 20} {py + 34} Q{px} {py + 50} {px + 20} {py + 34} Z', fill=tint(BLUE, 0.35), stroke=BLUE, sw=1.6)
    s.text(px, py + 70, lab, size=14, fill=INK2, anchor='middle', font=MATH, italic=True)
s.math(812, 222, 'Δ' + sub('DP', 5, 13) + '≤ τ', size=22)
s.math(812, 262, 'Δ' + sub('EO', 5, 13) + '≤ τ', size=22)
s.circle(824, 296, 12, GOOD)
s.path('M818 296.5 L822.5 301 L830.5 291.5', stroke='#ffffff', sw=2.8)
s.text(842, 302, 'verified', size=16, weight=600)
s.text(668, 336, 'demographic parity · equalized odds', size=14, fill=INK2)

# threats covered
s.rect(650, 364, 290, 144, fill=PANEL, stroke=AXIS, sw=2, rx=14)
s.text(668, 394, 'Threats covered', size=18, weight=700)
rows = ['only ciphertexts leave sites', 'attribute inference defended', 'malicious updates detected']
for j, t in enumerate(rows):
    yy = 428 + j * 30
    s.path(f'M676 {yy - 13} L686 {yy - 9} L686 {yy - 2} C686 {yy + 3} 682 {yy + 6} 676 {yy + 8} C670 {yy + 6} 666 {yy + 3} 666 {yy - 2} L666 {yy - 9} Z',
           fill=tint(BLUE, 0.35), stroke=BLUE, sw=1.5)
    s.text(698, yy + 3, t, size=15, fill=INK)

# results
tiles = [('0.231 → 0.031', 'demographic parity gap,', 'healthcare mortality task'),
         ('2.3×', 'compute overhead vs.', 'standard federated averaging'),
         ('O(n²) → O(n log n)', 'fairness verification with', 'the batched protocol')]
for i, (v, a, b) in enumerate(tiles):
    x = 20 + i * 310
    s.rect(x, 524, 300, 100, fill=PANEL, stroke=AXIS, sw=2, rx=14)
    if v.startswith('O('):
        s.math(x + 20, 562, v, size=25, weight=700)
    else:
        s.text(x + 20, 562, v, size=27, weight=700)
    s.text(x + 20, 590, a, size=15, fill=INK2)
    s.text(x + 20, 610, b, size=15, fill=INK2)
s.save('cryptofair-fl.svg')
