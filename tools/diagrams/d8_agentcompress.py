from dg import *
import math

s = SVG(960, 640, 'AgentCompress: task-aware compression for LLM agents',
        'A controller reads the first 32 tokens of each agent task, predicts its cognitive load, and picks a quantization, '
        'attention-pruning and sparsity policy, serving the task from a cache of FP16, INT8, INT4 and INT2 model variants. '
        'Compute drops 68.3% while task success stays at 96.2%, with about 12 ms of routing overhead.')
sub = lambda t, dy=5, fs=13: f'<tspan dy="{dy}" font-size="{fs}">{t}</tspan><tspan dy="{-dy}"> </tspan>'
PANEL = tint(INK2, 0.035)

s.text(24, 46, 'AgentCompress<tspan font-size="23" font-weight="400" fill="#52514e">  ·  full precision only where the task needs it</tspan>', size=30, weight=800)

# workflow tasks with different difficulty
s.rect(20, 72, 190, 288, fill=PANEL, stroke=AXIS, sw=2, rx=14)
s.text(36, 100, 'Agent workflow', size=18, weight=700)
s.math(36, 124, 'W = {τ₁ … τₙ}', size=17)
tasks = [('multi-step reasoning', 3), ('evidence synthesis', 3), ('unit conversion', 1), ('citation formatting', 1)]
for i, (t, hard) in enumerate(tasks):
    y = 140 + i * 46
    s.rect(30, y, 170, 38, fill='#ffffff', stroke=AXIS, sw=1.6, rx=8)
    s.text(42, y + 24, t, size=13)
    for k in range(3):
        s.circle(160 + k * 12, y + 10, 4, BLUE if k < hard else tint(INK2, 0.2))
s.text(36, 344, 'difficulty varies per task', size=13, fill=INK2)

PN = [(228, ('Task', 'encoder')), (418, ('Cognitive', 'load')), (608, ('Compression', 'policy')), (798, ('Variant', 'cache'))]
for i, (x, (a, b)) in enumerate(PN):
    w = 142 if i == 3 else 172
    s.rect(x, 72, w, 288, fill=PANEL, stroke=AXIS, sw=2, rx=14)
    s.badge(x + 28, 104, i + 1, BLUE)
    s.text(x + 52, 102, f'{a}\n{b}', size=18, weight=700, lh=1.12)
    if i:
        s.arrow([(x - 16, 216), (x - 3, 216)], color=INK2, sw=2.6, size=11)
s.arrow([(210, 216), (225, 216)], color=INK2, sw=2.6, size=11)

# 1 - encoder over the first 32 tokens
x = 228
for k in range(8):
    s.rect(x + 16 + k * 18, 158, 14, 20, fill=BLUE if k < 4 else tint(INK2, 0.16), rx=3)
s.text(x + 16, 196, 'first 32 tokens only', size=13, fill=INK2)
s.rect(x + 16, 210, 140, 34, fill='#ffffff', stroke=AXIS, sw=1.6, rx=8)
s.text(x + 86, 232, 'frozen LLaMA', size=14, anchor='middle')
s.arrow([(x + 86, 246), (x + 86, 258)], color=MUTED, sw=2, size=9)
s.rect(x + 16, 260, 140, 34, fill='#ffffff', stroke=AXIS, sw=1.6, rx=8)
s.text(x + 86, 282, '6-layer transformer', size=14, anchor='middle')
s.math(x + 86, 326, 'e' + sub('τ', 4, 12) + '∈ ℝ⁵¹²', size=18, anchor='middle')

# 2 - cognitive load predictor
x = 418
s.rect(x + 16, 158, 140, 32, fill='#ffffff', stroke=AXIS, sw=1.6, rx=8)
s.text(x + 86, 179, '4-head attention', size=14, anchor='middle')
s.rect(x + 16, 198, 140, 32, fill='#ffffff', stroke=AXIS, sw=1.6, rx=8)
s.text(x + 86, 219, 'MLP 256→128→1', size=14, anchor='middle')
cx, cy, r = x + 86, 306, 46
s.path(f'M{cx - r} {cy} A{r} {r} 0 0 1 {cx + r} {cy}', stroke=tint(INK2, 0.18), sw=10)
ang = math.pi * (1 - 0.78)
s.path(f'M{cx - r} {cy} A{r} {r} 0 0 1 {cx + r * math.cos(ang):.1f} {cy - r * math.sin(ang):.1f}', stroke=BLUE, sw=10)
s.line(cx, cy, cx + (r - 12) * math.cos(ang), cy - (r - 12) * math.sin(ang), stroke=INK, sw=3)
s.circle(cx, cy, 5, INK)
s.math(cx, cy + 26, 'c ∈ [0,1]', size=17, anchor='middle')
s.text(cx, cy + 46, 'predicted difficulty', size=13, fill=INK2, anchor='middle')

# 3 - policy heads
x = 608
s.text(x + 16, 168, 'quantization head', size=13, fill=INK2)
for k, q in enumerate(['FP16', 'INT8', 'INT4', 'INT2']):
    on = q == 'INT8'
    s.rect(x + 16 + k * 37, 178, 33, 26, fill=BLUE if on else '#ffffff', stroke=BLUE if on else AXIS, sw=1.6, rx=6)
    s.text(x + 32 + k * 37, 196, q, size=12, weight=700, fill='#ffffff' if on else INK2, anchor='middle')
for j, (lab, frac) in enumerate([('attention pruning ρ ≤ 0.75', 0.62), ('sparsity ≤ 0.9', 0.45)]):
    yy = 234 + j * 54
    s.text(x + 16, yy, lab, size=13, fill=INK2)
    s.line(x + 16, yy + 18, x + 156, yy + 18, stroke=tint(INK2, 0.2), sw=6)
    s.line(x + 16, yy + 18, x + 16 + 140 * frac, yy + 18, stroke=BLUE, sw=6)
    s.circle(x + 16 + 140 * frac, yy + 18, 8, '#ffffff', stroke=BLUE, sw=3)
s.text(x + 16, 344, 'Gumbel-softmax in training', size=13, fill=INK2)

# 4 - cached model variants, thickness = bit width
x = 798
for j, (q, gb, th) in enumerate([('FP16 · 140 GB', 140, 16), ('INT8 · 70 GB', 70, 11), ('INT4 · 35 GB', 35, 7), ('INT2 · 17.5 GB', 17.5, 4)]):
    yy = 168 + j * 46
    on = j == 1
    s.text(x + 16, yy, q, size=13, weight=700 if on else 400, fill=INK if on else INK2)
    s.rect(x + 16, yy + 8, 110, th, fill=BLUE if on else tint(INK2, 0.22), rx=2)
s.text(x + 16, 332, 'one variant resident', size=12, fill=INK2)
s.text(x + 16, 348, '94% reuse next task', size=12, fill=INK2)

# bottom left: cost vs quality
s.rect(20, 380, 450, 244, fill=PANEL, stroke=AXIS, sw=2, rx=16)
s.text(38, 410, 'Cost vs quality, 290 workflows', size=19, weight=700)
PX0, PX1, PY0, PY1 = 92, 440, 430, 574
s.line(PX0, PY1, PX1, PY1, stroke=AXIS, sw=1.5)
s.line(PX0, PY0, PX0, PY1, stroke=AXIS, sw=1.5)
fx = lambda c: PX0 + (c - 700) / 2250 * (PX1 - PX0)
fy = lambda q: PY1 - (q - 60) / 42 * (PY1 - PY0)
for q in (70, 90):
    s.line(PX0, fy(q), PX1, fy(q), stroke=GRID, sw=1)
    s.text(PX0 - 8, fy(q) + 5, str(q), size=12, fill=MUTED, anchor='end')
pts = [('Uniform FP16', 2847, 98.2, 0), ('Uniform INT8', 1644, 87.5, 0), ('Static INT4', 820, 63.8, 0),
       ('Oracle', 794, 98.7, 0), ('AgentCompress', 902, 96.2, 1)]
for name, c, q, hi in pts:
    s.circle(fx(c), fy(q), 7 if hi else 6, BLUE if hi else MUTED, stroke='#ffffff', sw=2)
for name, c, q, hi, ax, ay, an in [('Uniform FP16', 2847, 98.2, 0, -12, 5, 'end'), ('Uniform INT8', 1644, 87.5, 0, 0, 22, 'middle'),
                                   ('Static INT4', 820, 63.8, 0, 12, 5, 'start'), ('Oracle', 794, 98.7, 0, 4, -14, 'start'),
                                   ('AgentCompress', 902, 96.2, 1, 14, 6, 'start')]:
    s.text(fx(c) + ax, fy(q) + ay, name, size=13, weight=700 if hi else 400, fill=INK if hi else INK2, anchor=an)
s.text(266, 600, 'compute cost (TFLOPs) →', size=13, fill=MUTED, anchor='middle')
s.add(f'<text transform="translate(58 502) rotate(-90)" font-family="{FONT}" font-size="13" fill="{MUTED}" text-anchor="middle">task success (%)</text>')

# bottom right: results
for i, (v, a, b) in enumerate([('−68.3%', 'compute cost', '2,847 → 902 TFLOPs'), ('96.2%', 'task success', 'vs 98.2% at FP16'),
                               ('12 ms', 'routing overhead', 'per task decision'), ('94%', 'of consecutive tasks', 'reuse the loaded variant')]):
    x, y = 490 + (i % 2) * 230, 380 + (i // 2) * 124
    s.rect(x, y, 220, 114, fill=PANEL, stroke=AXIS, sw=2, rx=14)
    s.text(x + 18, y + 48, v, size=28, weight=700)
    s.text(x + 18, y + 76, a, size=15, fill=INK2)
    s.text(x + 18, y + 96, b, size=14, fill=MUTED)
s.save('agentcompress.svg')
