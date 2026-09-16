from dg import *
import math

s = SVG(960, 640, 'Hybrid GNN-QAOA pipeline for drug repurposing portfolio selection',
        'A graph neural network encodes the protein-drug interaction graph and molecular features into candidate scores; '
        'portfolio selection under therapeutic constraints is mapped to a QUBO and solved by QAOA, compiled to IBM 127-qubit '
        'heavy-hex topology with SWAP-aware routing to keep circuit depth low.')
PANEL = tint(INK2, 0.035)
Q = VIOLET

s.text(24, 46, 'GNN → QAOA<tspan font-size="23" font-weight="400" fill="#52514e">  ·  constrained drug repurposing on quantum hardware</tspan>', size=30, weight=800)

PN = [(20, 300, ('Protein–drug', 'graph')), (340, 250, ('GNN', 'encoder')), (610, 330, ('QAOA', 'on heavy-hex'))]
for i, (x, w, (a, b)) in enumerate(PN):
    s.rect(x, 74, w, 330, fill=PANEL, stroke=AXIS, sw=2, rx=16)
    s.badge(x + 30, 108, i + 1, BLUE)
    s.text(x + 56, 106, f'{a}\n{b}', size=20, weight=700, lh=1.12)
s.arrow([(322, 240), (338, 240)], color=INK2, sw=3, size=11)
s.arrow([(592, 240), (608, 240)], color=INK2, sw=3, size=11)

# 1 - bipartite protein-drug interaction graph
prot = [(80, 180), (80, 240), (80, 300)]
drug = [(250, 165), (250, 215), (250, 265), (250, 315)]
for i, p in enumerate(prot):
    for j, d in enumerate(drug):
        if (i + j) % 2 == 0 or j == 1:
            s.line(*p, *d, stroke='#d6d5cf', sw=1.6)
for cx, cy in prot:
    s.circle(cx, cy, 13, tint(AQUA, 0.35), stroke=AQUA, sw=2)
for cx, cy in drug:
    s.path(f'M{cx - 11} {cy} a11 11 0 0 1 22 0 a11 11 0 0 1 -22 0', fill=tint(BLUE, 0.3), stroke=BLUE, sw=2)
    s.line(cx - 11, cy, cx + 11, cy, stroke=BLUE, sw=1.6)
s.text(80, 340, 'proteins', size=15, fill=INK2, anchor='middle')
s.text(250, 340, 'drugs', size=15, fill=INK2, anchor='middle')
s.text(40, 378, 'molecular features + interaction edges', size=14, fill=INK2)

# 2 - GNN message passing to candidate scores
for k in range(3):
    x0 = 366 + k * 66
    for j, yy in enumerate((178, 226, 274)):
        s.circle(x0, yy, 9, '#ffffff', stroke=INK2, sw=1.6)
    if k < 2:
        for a in (178, 226, 274):
            for b in (178, 226, 274):
                s.line(x0 + 9, a, x0 + 57, b, stroke='#e1e0d9', sw=1.2)
s.text(432, 148, 'message passing', size=15, fill=INK2, anchor='middle')
s.arrow([(500, 226), (514, 226)], color=INK2, sw=2.2, size=10)
for j, h in enumerate([44, 30, 52]):
    s.rect(518, 200 + j * 26 - 9, h, 16, fill=BLUE, rx=4)
s.text(518, 178, 'scores', size=14, fill=INK2)
s.math(432, 320, 'H = GNN(A, X)', size=19, anchor='middle')
s.rect(360, 340, 210, 48, fill=tint(ORANGE, 0.1), stroke=ORANGE, sw=1.8, rx=8)
s.text(465, 360, 'therapeutic constraints', size=14, weight=700, anchor='middle')
s.text(465, 380, 'budget · coverage · toxicity', size=13, fill=INK2, anchor='middle')

# 3 - QUBO -> QAOA circuit -> heavy-hex compilation
s.rect(628, 150, 132, 42, fill='#ffffff', stroke=Q, sw=1.8, rx=8)
s.math(694, 178, 'QUBO', size=18, anchor='middle')
s.arrow([(694, 194), (694, 212)], color=Q, sw=2.2, size=10)
for k in range(3):
    s.line(632, 226 + k * 22, 756, 226 + k * 22, stroke=INK2, sw=1.6)
    s.rect(648 + k * 12, 218 + k * 22, 18, 16, fill=tint(Q, 0.35), stroke=Q, sw=1.5, rx=3)
    s.rect(706, 218 + k * 22, 18, 16, fill=tint(Q, 0.2), stroke=Q, sw=1.5, rx=3)
s.text(694, 306, 'QAOA layers: cost + mixer', size=14, fill=INK2, anchor='middle')
# heavy-hex lattice
cx0, cy0 = 850, 250
for r in range(3):
    for c in range(3):
        x = cx0 + (c - 1) * 46 + (r % 2) * 23
        y = cy0 + (r - 1) * 44
        s.circle(x, y, 7, tint(Q, 0.5), stroke=Q, sw=1.5)
        if c < 2:
            s.line(x + 7, y, x + 39, y, stroke=Q, sw=1.6)
        if r < 2:
            s.line(x, y + 7, x + (23 if r % 2 == 0 else -23), y + 37, stroke=Q, sw=1.6)
s.text(850, 168, 'IBM heavy-hex', size=15, weight=700, anchor='middle')
s.text(850, 358, 'topology-aware', size=14, fill=INK2, anchor='middle')
s.text(850, 378, 'gate compilation', size=14, fill=INK2, anchor='middle')
s.arrow([(768, 250), (800, 250)], color=Q, sw=2.4, size=11)

for i, (v, a, b) in enumerate([('127', 'qubit IBM hardware', 'heavy-hex lattice'), ('GNN + QAOA', 'hybrid quantum-', 'classical pipeline'),
                               ('SWAP-aware', 'routing keeps', 'circuit depth low'), ('ChemRxiv', 'preprint, 2026', 'drug repurposing')]):
    x = 20 + i * 235
    s.rect(x, 424, 225, 112, fill=PANEL, stroke=AXIS, sw=2, rx=14)
    s.text(x + 18, 466, v, size=24 if len(v) < 8 else 20, weight=700)
    s.text(x + 18, 494, a, size=14, fill=INK2)
    s.text(x + 18, 514, b, size=14, fill=INK2)
s.rect(20, 552, 920, 68, fill=tint(BLUE, 0.07), stroke=BLUE, sw=2, rx=14)
s.text(40, 580, 'Why quantum here:', size=17, weight=700)
s.text(214, 580, 'portfolio selection under therapeutic constraints is a constrained combinatorial problem;', size=16, fill=INK2)
s.text(40, 604, 'QAOA searches that space directly, while the GNN supplies the biology-aware objective it optimises.', size=16, fill=INK2)
s.save('gnn-qaoa.svg')
