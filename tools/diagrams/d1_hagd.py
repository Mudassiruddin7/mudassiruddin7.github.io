from dg import *

s = SVG(960, 640, 'HAGD: Hierarchical Attribution Graph Decomposition',
        'Four stages: cross-layer transcoders produce sparse features, gradient-times-activation builds an attribution graph, '
        'normalized-Laplacian spectral clustering coarsens it into a hierarchy of supernodes, and a graph attention network '
        'guides a coarse-to-fine search whose candidate circuit is verified by activation patching.')
EDGE, NODE_OFF = '#d6d5cf', '#ffffff'
sub = lambda t, dy=6, fs=15: f'<tspan dy="{dy}" font-size="{fs}">{t}</tspan><tspan dy="{-dy}"> </tspan>'

s.text(24, 48, 'HAGD<tspan font-size="24" font-weight="400" fill="#52514e">  ·  Hierarchical Attribution Graph Decomposition</tspan>', size=31, weight=800)

Y0, PH, PW = 76, 398, 206
xs = [20, 258, 496, 734]
titles = [('Cross-layer', 'transcoders'), ('Attribution', 'graph'), ('Spectral', 'coarsening'), ('GNN-guided', 'traversal')]
for i, x in enumerate(xs):
    s.rect(x, Y0, PW, PH, fill=tint(INK2, 0.035), stroke=AXIS, sw=2, rx=16)
    s.badge(x + 32, Y0 + 34, i + 1, BLUE)
    s.text(x + 58, Y0 + 32, f'{titles[i][0]}\n{titles[i][1]}', size=21, weight=700, lh=1.12)
    if i < 3:
        s.arrow([(x + PW + 3, 292), (x + PW + 30, 292)], color=INK2, sw=3, size=14)

# 1 - transcoders: layer states -> sparse feature rows, cross-layer prediction W_P
x = xs[0]
lit = [{1, 4}, {0, 3}, {2, 5}]
rows = [195, 290, 385]
for r, yc in enumerate(rows):
    s.rect(x + 14, yc - 17, 62, 34, fill='#ffffff', stroke=INK2, sw=1.6, rx=7)
    s.math(x + 45, yc + 8, 'h' + sub('ℓ+%d' % r if r else 'ℓ'), size=22, anchor='middle')
    s.arrow([(x + 80, yc), (x + 98, yc)], color=MUTED, sw=2, size=10)
    for k in range(6):
        on = k in lit[r]
        s.circle(x + 110 + k * 16, yc, 6.5, BLUE if on else NODE_OFF, stroke=None if on else AXIS, sw=1.6)
    if r < 2:
        s.arrow([(x + 150, yc + 13), (x + 150, rows[r + 1] - 13)], color=BLUE, sw=2.6, size=11)
        s.math(x + 160, (yc + rows[r + 1]) / 2 + 7, 'W' + sub('P', 5, 14), size=20)
s.text(x + PW / 2, 440, 'TopK sparse features', size=18, fill=INK2, anchor='middle')

# 2 - attribution graph: dense edges, top-k strong path highlighted
x = xs[1]
cols, rys = [x + 38, x + 103, x + 168], [178, 230, 282, 334]
strong = {((0, 1), (1, 2)), ((0, 3), (1, 2)), ((1, 2), (2, 0)), ((1, 2), (2, 3))}
for c in range(2):
    for a in range(4):
        for b in range(4):
            if ((c, a), (c + 1, b)) not in strong:
                s.line(cols[c], rys[a], cols[c + 1], rys[b], stroke=EDGE, sw=1.3)
for (c, a), (c2, b) in strong:
    s.line(cols[c], rys[a], cols[c2], rys[b], stroke=BLUE, sw=3.4)
on_nodes = {n for e in strong for n in e}
for c in range(3):
    for a in range(4):
        on = (c, a) in on_nodes
        s.circle(cols[c], rys[a], 9, BLUE if on else '#ffffff', stroke='#ffffff' if on else INK2, sw=2 if on else 1.6)
s.math(x + PW / 2, 392, 'A' + sub('i→j') + '= ∂f' + sub('j') + '/ ∂f' + sub('i') + '· f' + sub('i'), size=21, anchor='middle')
s.text(x + PW / 2, 440, 'keep top-k edges', size=18, fill=INK2, anchor='middle')

# 3 - spectral coarsening: G0 dots -> G1 supernodes -> G2
x = xs[2]
g0 = [x + 22 + i * 18.2 for i in range(10)]
groups = [(0, 3), (3, 5), (5, 8), (8, 10)]
g1 = [(sum(g0[a:b]) / (b - a)) for a, b in groups]
g2 = [(g1[0] + g1[1]) / 2, (g1[2] + g1[3]) / 2]
for gi, (a, b) in enumerate(groups):
    for k in range(a, b):
        s.line(g0[k], 345, g1[gi], 262, stroke=AXIS, sw=1.5)
for gi, cx in enumerate(g1):
    s.line(cx, 262, g2[gi // 2], 184, stroke=AXIS, sw=2)
for cx in g0:
    s.circle(cx, 345, 6.5, '#ffffff', stroke=INK2, sw=1.6)
for cx in g1:
    s.circle(cx, 262, 14, tint(BLUE, 0.22), stroke=BLUE, sw=2)
for cx in g2:
    s.circle(cx, 184, 21, tint(BLUE, 0.45), stroke=BLUE, sw=2.4)
for yy, lab in [(190, '(2)'), (268, '(1)'), (351, '(0)')]:
    pass
s.math(x + PW / 2, 392, 'L = I − D' + '<tspan dy="-9" font-size="14">−½</tspan><tspan dy="9"> A D</tspan>'
       + '<tspan dy="-9" font-size="14">−½</tspan>', size=22, anchor='middle')
s.text(x + PW / 2, 440, 'supernode hierarchy', size=18, fill=INK2, anchor='middle')

# 4 - GNN-guided traversal: descend only into high-scoring supernodes, then patch-verify
x = xs[3]
top = [(x + 62, 178, True), (x + 150, 178, False)]
mid = [(x + 36, 238, True, 0), (x + 88, 238, False, 0), (x + 128, 238, False, 1), (x + 174, 238, False, 1)]
leaves = [(x + 18, 290, True, 0), (x + 36, 290, True, 0), (x + 54, 290, True, 0), (x + 80, 290, False, 1),
          (x + 98, 290, False, 1), (x + 122, 290, False, 2), (x + 140, 290, False, 2), (x + 166, 290, False, 3), (x + 184, 290, False, 3)]
for mx, my, on, p in mid:
    s.line(top[p][0], top[p][1], mx, my, stroke=BLUE if on else EDGE, sw=3.2 if on else 1.6)
for lx, ly, on, p in leaves:
    s.line(mid[p][0], mid[p][1], lx, ly, stroke=BLUE if on else EDGE, sw=3 if on else 1.4)
for tx, ty, on in top:
    s.circle(tx, ty, 19, BLUE if on else tint(BLUE, 0.12), stroke=None if on else AXIS, sw=1.6)
for mx, my, on, p in mid:
    s.circle(mx, my, 12, BLUE if on else tint(BLUE, 0.12), stroke=None if on else AXIS, sw=1.4)
for lx, ly, on, p in leaves:
    s.circle(lx, ly, 6, BLUE if on else '#ffffff', stroke=None if on else AXIS, sw=1.4)
# extracted circuit, verified
s.rect(x + 14, 318, 178, 50, fill='#ffffff', stroke=GOOD, sw=2, rx=10)
cn = [(x + 34, 343), (x + 70, 331), (x + 70, 355), (x + 106, 343)]
for a, b in [(0, 1), (0, 2), (1, 3), (2, 3)]:
    s.line(*cn[a], *cn[b], stroke=BLUE, sw=2.6)
for cx, cy in cn:
    s.circle(cx, cy, 6, BLUE)
s.circle(x + 164, 343, 13, GOOD)
s.path(f'M{x + 157} {343.5} L{x + 162} {348.5} L{x + 171} {338}', stroke='#ffffff', sw=3.2)
s.text(x + 128, 350, 'C*', size=19, weight=700, fill=INK, anchor='middle')
s.math(x + 70, 403, 'φ(C) =', size=21, anchor='end')
s.math(x + 132, 392, 'Acc(patched)', size=17, anchor='middle')
s.line(x + 80, 398, x + 184, 398, stroke=INK, sw=1.4)
s.math(x + 132, 416, 'Acc(clean)', size=17, anchor='middle')
s.text(x + PW / 2, 446, 'activation patching', size=18, fill=INK2, anchor='middle')

# bottom: what the hierarchy changes
s.rect(20, 494, 436, 128, fill=tint(ORANGE, 0.07), stroke=ORANGE, sw=2, rx=16)
s.text(42, 532, 'Flat circuit search', size=24, weight=700)
s.text(42, 562, 'scores candidate subgraphs of the whole graph', size=19, fill=INK2)
s.math(42, 604, 'O(2<tspan dy="-12" font-size="22">n</tspan><tspan dy="12">)</tspan>', size=34, weight=700)
s.arrow([(462, 558), (498, 558)], color=INK2, sw=3, size=14)
s.rect(504, 494, 436, 128, fill=tint(BLUE, 0.08), stroke=BLUE, sw=2, rx=16)
s.text(526, 532, 'HAGD: coarse to fine', size=24, weight=700)
s.text(526, 562, 'expands only supernodes the GNN ranks high', size=19, fill=INK2)
s.math(526, 604, 'O(n<tspan dy="-12" font-size="22">2</tspan><tspan dy="12"> log n)</tspan>', size=34, weight=700)
s.save('hagd.svg')
