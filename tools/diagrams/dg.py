"""Tiny SVG builder for the paper architecture diagrams (white paper-figure style)."""
import os

FONT = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MATH = "'Cambria Math','Times New Roman',Times,serif"

# Ink and chrome (dataviz reference palette, light mode)
INK, INK2, MUTED = '#0b0b0b', '#52514e', '#898781'
GRID, AXIS, NEUTRAL = '#e1e0d9', '#c3c2b7', '#f0efec'
# Categorical slots in fixed order
BLUE, ORANGE, AQUA, YELLOW = '#2a78d6', '#eb6834', '#1baf7a', '#eda100'
MAGENTA, GREEN, VIOLET, RED = '#e87ba4', '#008300', '#4a3aa7', '#e34948'
# Status (reserved meaning, always with icon + label)
GOOD, WARN, SERIOUS, CRIT = '#0ca30c', '#fab219', '#ec835a', '#d03b3b'

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'images', 'papers'))


def tint(hexc, a):
    """Blend a hex color over white at opacity a."""
    h = hexc.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = lambda c: round(255 - (255 - c) * a)
    return '#%02x%02x%02x' % (m(r), m(g), m(b))


def est(t, size, bold=False):
    """Rough rendered width of plain text in the sans stack."""
    return len(t) * size * (0.58 if bold else 0.54)


class SVG:
    def __init__(self, w, h, title, desc):
        self.w, self.h, self.title, self.desc = w, h, title, desc
        self.parts, self.markers = [], {}

    def add(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, fill='none', stroke=None, sw=2, rx=10, dash=None, op=None):
        a = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if op is not None:
            a += f' opacity="{op}"'
        self.add(a + '/>')

    def circle(self, cx, cy, r, fill, stroke=None, sw=2, op=None):
        a = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw}"'
        if op is not None:
            a += f' opacity="{op}"'
        self.add(a + '/>')

    def line(self, x1, y1, x2, y2, stroke=AXIS, sw=2, dash=None, cap='round'):
        a = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        self.add(a + '/>')

    def path(self, d, fill='none', stroke=None, sw=2, dash=None, op=None, join='round'):
        a = f'<path d="{d}" fill="{fill}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="{join}" stroke-linecap="round"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if op is not None:
            a += f' opacity="{op}"'
        self.add(a + '/>')

    def _marker(self, color, size):
        key = f'ah{len(self.markers)}'
        for k, v in self.markers.items():
            if v == (color, size):
                return k
        self.markers[key] = (color, size)
        return key

    def arrow(self, pts, color=INK2, sw=3, dash=None, size=15, both=False):
        """Polyline arrow through pts [(x, y), ...] with a head at the end."""
        mid = self._marker(color, size)
        d = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
        a = f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round" marker-end="url(#{mid})"'
        if both:
            a += f' marker-start="url(#{mid})"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        self.add(a + '/>')

    def carrow(self, d, color=INK2, sw=3, dash=None, size=15):
        """Arrow along an arbitrary path d."""
        mid = self._marker(color, size)
        a = f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" marker-end="url(#{mid})"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        self.add(a + '/>')

    def text(self, x, y, t, size=24, weight=400, fill=INK, anchor='start', font=FONT, italic=False, lh=1.22):
        """Text; '\\n' makes extra lines. Inline <tspan> markup is allowed (escape & and < yourself)."""
        a = f'font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"'
        if italic:
            a += ' font-style="italic"'
        lines = t.split('\n')
        if len(lines) == 1:
            self.add(f'<text x="{x}" y="{y}" {a}>{t}</text>')
            return
        spans = ''.join(
            f'<tspan x="{x}" dy="{0 if i == 0 else round(size * lh, 1)}">{ln}</tspan>' for i, ln in enumerate(lines))
        self.add(f'<text x="{x}" y="{y}" {a}>{spans}</text>')

    def math(self, x, y, t, size=26, fill=INK, anchor='start', weight=400):
        self.text(x, y, t, size=size, fill=fill, anchor=anchor, font=MATH, italic=True, weight=weight)

    def badge(self, cx, cy, n, color, r=17):
        self.circle(cx, cy, r, color)
        self.text(cx, cy + 7.5, str(n), size=21, weight=700, fill='#ffffff', anchor='middle')

    def chip(self, x, y, t, color, size=21, h=34, w=None, fill=None, tcolor=INK, weight=600):
        w = w or round(est(t, size, weight >= 600) + 24)
        self.rect(x, y, w, h, fill=fill or tint(color, 0.12), stroke=color, sw=1.6, rx=h / 2)
        self.text(x + w / 2, y + h / 2 + size * 0.36, t, size=size, weight=weight, fill=tcolor, anchor='middle')
        return w

    def panel(self, x, y, w, h, color, title=None, num=None, dash=None, a=0.07, tsize=26):
        self.rect(x, y, w, h, fill=tint(color, a), stroke=color, sw=2.4, rx=16, dash=dash)
        if title:
            tx = x + 18
            if num is not None:
                self.badge(x + 34, y + 34, num, color)
                tx = x + 60
            self.text(tx, y + 43, title, size=tsize, weight=700)

    def save(self, name):
        defs = ''.join(
            f'<marker id="{k}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="{s}" markerHeight="{s}" '
            f'markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0,0.8 L10,5 L0,9.2 z" fill="{c}"/></marker>'
            for k, (c, s) in self.markers.items())
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
               f'role="img" aria-labelledby="t d"><title id="t">{self.title}</title><desc id="d">{self.desc}</desc>'
               f'<defs>{defs}</defs><rect width="{self.w}" height="{self.h}" fill="#ffffff"/>' + '\n'.join(self.parts) + '</svg>')
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
            f.write(svg)
        print('wrote', name, len(svg), 'bytes')
