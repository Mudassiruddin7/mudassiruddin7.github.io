/* Research project pages: theme toggle, contents highlighting, BibTeX copy and charts.
   Each page defines window.CHARTS = { name: spec }, and every <div class="chart" data-chart="name">
   is drawn as plain SVG from that spec. Colours come from CSS tokens, so both themes work
   without redrawing. Every chart also gets a "Show data" table. */
(function () {
  'use strict';

  var doc = document, root = doc.documentElement, NS = 'http://www.w3.org/2000/svg';
  var FONT = '"IBM Plex Sans","Segoe UI",system-ui,-apple-system,sans-serif';

  /* ---------------- theme (shares the portfolio's "site-theme" key) ---------------- */
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function isDark() {
    var t = root.getAttribute('data-theme');
    if (t === 'dark') return true;
    if (t) return false;
    return !!(mq && mq.matches);
  }
  function syncToggle() {
    var b = doc.getElementById('theme-toggle');
    if (!b) return;
    var label = isDark() ? 'Switch to light theme' : 'Switch to dark theme';
    b.setAttribute('aria-label', label);
    b.title = label;
  }
  function toggleTheme() {
    var dark = !isDark();
    root.setAttribute('data-theme', dark ? 'dark' : 'light');
    try { localStorage.setItem('site-theme', dark ? 'dark' : 'white'); } catch (e) { /* storage blocked */ }
    syncToggle();
  }
  if (mq && mq.addEventListener) mq.addEventListener('change', syncToggle);

  /* ---------------- contents rail: highlight the section being read ---------------- */
  function initToc() {
    var links = [].slice.call(doc.querySelectorAll('.toc a[href^="#"]'));
    if (!links.length || !('IntersectionObserver' in window)) return;
    var seen = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { seen[e.target.id] = e.isIntersecting; });
      var current = null;
      links.forEach(function (a) { if (!current && seen[a.getAttribute('href').slice(1)]) current = a; });
      if (current) links.forEach(function (a) { a.classList.toggle('active', a === current); });
    }, { rootMargin: '-72px 0px -55% 0px' });
    links.forEach(function (a) {
      var s = doc.getElementById(a.getAttribute('href').slice(1));
      if (s) io.observe(s);
    });
  }

  /* ---------------- copy buttons ---------------- */
  function initCopy() {
    [].forEach.call(doc.querySelectorAll('[data-copy]'), function (btn) {
      var label = btn.textContent;
      btn.addEventListener('click', function () {
        var src = doc.getElementById(btn.getAttribute('data-copy'));
        if (!src) return;
        var done = function () { btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = label; }, 1600); };
        var fallback = function () {
          var r = doc.createRange(); r.selectNodeContents(src);
          var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
          try { if (doc.execCommand('copy')) done(); } catch (e) { /* leave text selected */ }
        };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(src.textContent).then(done, fallback);
        else fallback();
      });
    });
  }

  /* ---------------- small helpers ---------------- */
  function S(tag, attrs, parent) {
    var e = doc.createElementNS(NS, tag);
    if (attrs) for (var k in attrs) if (attrs[k] != null) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function minus(str) { return String(str).replace(/(^|[\s(])-(?=[\d.])/g, '$1−'); }
  function T(parent, x, y, str, cls, anchor, extra) {
    var a = { x: r2(x), y: r2(y), 'class': cls, 'text-anchor': anchor || 'start' };
    if (extra) for (var k in extra) a[k] = extra[k];
    var e = S('text', a, parent);
    e.textContent = minus(str);
    return e;
  }
  function H(tag, cls, parent, text) {
    var e = doc.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function r2(v) { return Math.round(v * 100) / 100; }
  function col(c) { return !c ? 'var(--deemph)' : (c.charAt(0) === '#' ? c : 'var(--' + c + ')'); }
  var mctx = null;
  function measure(str, size, weight) {
    if (!mctx) mctx = doc.createElement('canvas').getContext('2d');
    mctx.font = (weight || 400) + ' ' + (size || 12) + 'px ' + FONT;
    return mctx.measureText(String(str)).width;
  }
  function maxW(list, size, weight) { var m = 0; list.forEach(function (s) { m = Math.max(m, measure(s, size, weight)); }); return m; }
  function scale(d0, d1, r0, r1) { var k = (r1 - r0) / ((d1 - d0) || 1); return function (v) { return r0 + (v - d0) * k; }; }
  function niceTicks(lo, hi, n) {
    var span = hi - lo, raw = span / (n || 5), mag = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10)), f = raw / mag;
    var step = (f >= 7.5 ? 10 : f >= 3.5 ? 5 : f >= 1.5 ? 2 : 1) * mag, out = [];
    for (var v = Math.ceil(lo / step - 1e-9) * step; v <= hi + step * 1e-9; v += step) out.push(+v.toFixed(10));
    return out;
  }
  function fmtOf(spec, key) {
    var f = (key && spec[key] && spec[key].fmt) || spec.fmt;
    if (typeof f === 'function') return f;
    var d = typeof f === 'number' ? f : 1, unit = (key && spec[key] && spec[key].unit) || spec.unit || '';
    return function (v) { return (v < 0 ? '−' : '') + Math.abs(v).toFixed(d) + unit; };
  }
  function signed(f) { return function (v) { return (v > 0 ? '+' : '') + f(v); }; }
  function barPath(o, x0, x1, y, h, r) {
    // o: 'h' (bar grows along x) or 'v' (grows along y). x0 = baseline, x1 = data end.
    var len = Math.abs(x1 - x0); r = Math.max(0, Math.min(r, len, h / 2));
    var d = x1 >= x0 ? 1 : -1, e = x1 - d * r;
    if (o === 'h') {
      return 'M' + r2(x0) + ',' + r2(y) + 'H' + r2(e) + 'Q' + r2(x1) + ',' + r2(y) + ' ' + r2(x1) + ',' + r2(y + r) +
        'V' + r2(y + h - r) + 'Q' + r2(x1) + ',' + r2(y + h) + ' ' + r2(e) + ',' + r2(y + h) + 'H' + r2(x0) + 'Z';
    }
    // vertical: y is the left edge, h the width; x0/x1 are the pixel y of baseline and data end.
    return 'M' + r2(y) + ',' + r2(x0) + 'V' + r2(e) + 'Q' + r2(y) + ',' + r2(x1) + ' ' + r2(y + r) + ',' + r2(x1) +
      'H' + r2(y + h - r) + 'Q' + r2(y + h) + ',' + r2(x1) + ' ' + r2(y + h) + ',' + r2(e) + 'V' + r2(x0) + 'Z';
  }

  /* ---------------- tooltip ---------------- */
  var tip = null;
  function tipEl() {
    if (!tip) { tip = H('div', 'tip', doc.body); tip.setAttribute('role', 'tooltip'); tip.hidden = true; }
    return tip;
  }
  function fillTip(c) {
    var t = tipEl(); t.textContent = '';
    if (c.head) H('div', 't-head', t, c.head);
    (c.rows || []).forEach(function (r) {
      var row = H('div', 't-row', t);
      if (r.color) { var i = H('i', null, row); i.style.background = col(r.color); }
      H('span', 't-v', row, minus(r.v));
      if (r.k) H('span', 't-k', row, r.k);
    });
  }
  function placeTip(x, y) {
    var t = tipEl(); t.hidden = false;
    var w = t.offsetWidth, h = t.offsetHeight, vw = window.innerWidth, vh = window.innerHeight;
    var left = x + 14, top = y - h - 12;
    if (left + w > vw - 8) left = x - w - 14;
    if (left < 8) left = 8;
    if (top < 8) top = y + 18;
    if (top + h > vh - 8) top = Math.max(8, vh - h - 8);
    t.style.left = Math.round(left) + 'px'; t.style.top = Math.round(top) + 'px';
  }
  function hideTip() { if (tip) tip.hidden = true; }
  function tipText(c) { return [c.head].concat((c.rows || []).map(function (r) { return r.v + (r.k ? ' ' + r.k : ''); })).filter(Boolean).join(', '); }
  function bindTip(el, c, focusable) {
    if (focusable !== false) {
      el.setAttribute('tabindex', '0');
      el.setAttribute('role', 'img');
      el.setAttribute('aria-label', tipText(c));
    }
    el.addEventListener('pointerenter', function (e) { fillTip(c); placeTip(e.clientX, e.clientY); });
    el.addEventListener('pointermove', function (e) { placeTip(e.clientX, e.clientY); });
    el.addEventListener('pointerleave', hideTip);
    el.addEventListener('focus', function () { var b = el.getBoundingClientRect(); fillTip(c); placeTip(b.left + b.width / 2, b.top); });
    el.addEventListener('blur', hideTip);
  }
  window.addEventListener('scroll', hideTip, { passive: true });

  /* ---------------- legend and data table ---------------- */
  function legend(items) {
    var box = H('div', 'legend');
    items.forEach(function (it) {
      var s = H('span', null, box), i = H('i', it.kind || null, s);
      if (it.kind === 'ring') i.style.borderColor = col(it.color);
      else if (it.kind !== 'ref') i.style.background = col(it.color);
      s.appendChild(doc.createTextNode(it.label));
    });
    return box;
  }
  function dataTable(spec, open) {
    var d = spec.data;
    if (!d) return null;
    var det = H('details', 'chart-data'); if (open) det.open = true;
    H('summary', null, det, 'Show data');
    var wrap = H('div', 'tbl-wrap', det), tb = H('table', 'bt small', wrap);
    var tr = H('tr', null, H('thead', null, tb));
    d.cols.forEach(function (c, i) { var th = H('th', i === 0 ? 'l' : null, tr, c); th.scope = 'col'; });
    var body = H('tbody', null, tb);
    d.rows.forEach(function (row) {
      var r = H('tr', null, body);
      row.forEach(function (v, i) { H('td', i === 0 ? 'l' : null, r, v); });
    });
    return det;
  }

  /* ---------------- chart types ---------------- */
  var TYPES = {};

  // Horizontal bars. Rows: {label, value, err, hl, color}. Optional refs: [{value, label}].
  TYPES.hbar = function (svg, sp, W) {
    var f = fmtOf(sp), vf = sp.signed ? signed(f) : f;
    var rows = sp.rows, barH = sp.barH || 18, gap = sp.gap || 14;
    var narrow = W < (sp.narrowAt || 520);
    var labW = narrow ? 0 : Math.ceil(maxW(rows.map(function (r) { return r.label; }), 13, 500)) + 16;
    var valW = Math.ceil(maxW(rows.map(function (r) { return r.text || (vf(r.value) + (r.err ? ' ± ' + f(r.err) : '')); }), 12.5, 600)) + 10;
    var d0 = sp.domain[0], d1 = sp.domain[1], hasNeg = d0 < 0;
    var top = sp.refs ? 22 : 6, rowH = barH + gap + (narrow ? 18 : 0);
    var plotH = rows.length * rowH - gap + 4, bottom = 26 + (sp.axisLabel ? 20 : 0);
    var left = labW + (hasNeg && !narrow ? valW : 0), right = valW + 4;
    if (narrow) left = Math.max(hasNeg ? valW : 0, 12);
    var x = scale(d0, d1, left, W - right), H0 = top + plotH + bottom;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H0); svg.setAttribute('height', H0);
    var ticks = sp.ticks || niceTicks(d0, d1, narrow ? 4 : 6), tf = sp.tickFmt || f;
    ticks.forEach(function (t) {
      S('line', { x1: r2(x(t)) + 0.5, x2: r2(x(t)) + 0.5, y1: top - 2, y2: top + plotH, 'class': t === 0 ? 'c-zero' : 'c-grid' }, svg);
      T(svg, x(t), top + plotH + 17, tf(t), 'c-tick', 'middle');
    });
    if (sp.axisLabel) T(svg, (left + W - right) / 2, H0 - 4, sp.axisLabel, 'c-title', 'middle');
    (sp.refs || []).forEach(function (rf) {
      var rx = x(rf.value);
      S('line', { x1: r2(rx), x2: r2(rx), y1: top - 4, y2: top + plotH, 'class': 'c-ref' }, svg);
      var anchor = rf.anchor || (rx > (left + W - right) * 0.6 ? 'end' : 'start');
      T(svg, anchor === 'end' ? rx - 5 : rx + 5, top - 8, rf.label, 'c-ref-t', anchor);
    });
    rows.forEach(function (r, i) {
      var y0 = top + i * rowH + (narrow ? 18 : 0);
      var c = r.color || (r.hl ? 'accent' : sp.signColors ? (r.value < 0 ? sp.signColors.neg : sp.signColors.pos) : (sp.color || 'deemph'));
      if (narrow) T(svg, left, y0 - 6, r.label, r.hl ? 'c-lab-b' : 'c-lab', 'start');
      else T(svg, labW - 12, y0 + barH / 2 + 4.5, r.label, r.hl ? 'c-lab-b' : 'c-lab', 'end');
      var base = x(Math.max(d0, Math.min(0, d1))), end = x(r.value);
      var p = S('path', { d: barPath('h', base, end, y0, barH, 4), style: 'fill:' + col(c), 'class': 'mark' }, svg);
      if (r.err) {
        var e0 = x(r.value - r.err), e1 = x(r.value + r.err), ym = y0 + barH / 2;
        S('line', { x1: r2(e0), x2: r2(e1), y1: r2(ym), y2: r2(ym), 'class': 'c-err' }, svg);
        S('line', { x1: r2(e0), x2: r2(e0), y1: r2(ym - 4), y2: r2(ym + 4), 'class': 'c-err' }, svg);
        S('line', { x1: r2(e1), x2: r2(e1), y1: r2(ym - 4), y2: r2(ym + 4), 'class': 'c-err' }, svg);
      }
      var lab = r.text || (vf(r.value) + (r.err ? ' ± ' + f(r.err) : ''));
      var tail = r.err ? x(r.value + (r.value < 0 ? -r.err : r.err)) : end;
      T(svg, r.value < 0 ? tail - 6 : tail + 6, y0 + barH / 2 + 4.5, lab, r.hl ? 'c-val-b' : 'c-val', r.value < 0 ? 'end' : 'start');
      bindTip(p, { head: r.label, rows: [{ v: lab, k: sp.valueName || '', color: c }].concat(r.tip ? [{ v: r.tip }] : []) });
    });
  };

  // Grouped vertical columns. categories + series[{name, color, values}].
  TYPES.cols = function (svg, sp, W) {
    var f = fmtOf(sp), cats = sp.categories, ser = sp.series, n = ser.length;
    var d0 = sp.domain[0], d1 = sp.domain[1], ticks = sp.ticks || niceTicks(d0, d1, 5), tf = sp.tickFmt || f;
    var left = Math.ceil(maxW(ticks.map(tf), 12)) + 12 + (sp.yLabel ? 18 : 0), right = 4, top = 20;
    var bottom = 26 + (sp.catNotes ? 16 : 0), plotH = sp.height || 240, H0 = top + plotH + bottom;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H0); svg.setAttribute('height', H0);
    var y = scale(d0, d1, top + plotH, top), gw = (W - left - right) / cats.length;
    var bw = Math.min(24, (gw * 0.72 - 2 * (n - 1)) / n);
    ticks.forEach(function (t) {
      S('line', { x1: left, x2: W - right, y1: r2(y(t)) + 0.5, y2: r2(y(t)) + 0.5, 'class': t === d0 ? 'c-axis' : 'c-grid' }, svg);
      T(svg, left - 8, y(t) + 4, tf(t), 'c-tick', 'end');
    });
    if (sp.yLabel) T(svg, 12, top + plotH / 2, sp.yLabel, 'c-title', 'middle', { transform: 'rotate(-90 12 ' + r2(top + plotH / 2) + ')' });
    cats.forEach(function (cat, ci) {
      var gx = left + gw * ci + gw / 2, x0 = gx - (n * bw + (n - 1) * 2) / 2;
      var rows = ser.map(function (s) { return { v: f(s.values[ci]), k: s.name, color: s.color }; });
      ser.forEach(function (s, si) {
        var bx = x0 + si * (bw + 2), v = s.values[ci];
        var p = S('path', { d: barPath('v', y(Math.max(d0, 0)), y(v), bx, bw, 4), style: 'fill:' + col(s.color), 'class': 'mark' }, svg);
        if (sp.valueLabels !== false) T(svg, bx + bw / 2, y(v) - 6, f(v), 'c-val', 'middle');
        bindTip(p, { head: cat, rows: rows });
      });
      T(svg, gx, top + plotH + 18, cat, 'c-lab', 'middle');
      if (sp.catNotes && sp.catNotes[cat]) T(svg, gx, top + plotH + 33, sp.catNotes[cat], 'c-note', 'middle');
    });
  };

  // Scatter with optional error bars and direct labels. points[{label, x, y, ex, ey, hl, ring, lx, ly, anchor}].
  TYPES.scatter = function (svg, sp, W) {
    var fx = fmtOf(sp, 'x'), fy = fmtOf(sp, 'y');
    var xt = sp.x.ticks || niceTicks(sp.x.domain[0], sp.x.domain[1], 5), yt = sp.y.ticks || niceTicks(sp.y.domain[0], sp.y.domain[1], 5);
    var xtf = sp.x.tickFmt || fx, ytf = sp.y.tickFmt || fy;
    var left = Math.ceil(maxW(yt.map(ytf), 12)) + 14 + (sp.y.label ? 20 : 0), right = sp.right || 16, top = 12;
    var plotH = sp.height || 300, bottom = 28 + (sp.x.label ? 20 : 0), H0 = top + plotH + bottom;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H0); svg.setAttribute('height', H0);
    var x = scale(sp.x.domain[0], sp.x.domain[1], left, W - right), y = scale(sp.y.domain[0], sp.y.domain[1], top + plotH, top);
    yt.forEach(function (t) {
      S('line', { x1: left, x2: W - right, y1: r2(y(t)) + 0.5, y2: r2(y(t)) + 0.5, 'class': 'c-grid' }, svg);
      T(svg, left - 8, y(t) + 4, ytf(t), 'c-tick', 'end');
    });
    xt.forEach(function (t) {
      S('line', { x1: r2(x(t)) + 0.5, x2: r2(x(t)) + 0.5, y1: top, y2: top + plotH, 'class': 'c-grid' }, svg);
      T(svg, x(t), top + plotH + 18, xtf(t), 'c-tick', 'middle');
    });
    S('line', { x1: left, x2: W - right, y1: top + plotH + 0.5, y2: top + plotH + 0.5, 'class': 'c-axis' }, svg);
    if (sp.x.label) T(svg, (left + W - right) / 2, H0 - 4, sp.x.label, 'c-title', 'middle');
    if (sp.y.label) T(svg, 12, top + plotH / 2, sp.y.label, 'c-title', 'middle', { transform: 'rotate(-90 12 ' + r2(top + plotH / 2) + ')' });
    (sp.annotations || []).forEach(function (a) { T(svg, x(a.x), y(a.y), a.text, a.cls || 'c-note', a.anchor || 'start'); });
    sp.points.forEach(function (p) {
      var px = x(p.x), py = y(p.y), c = p.color || (p.hl ? 'accent' : 'deemph');
      if (p.ex) { S('line', { x1: r2(x(p.x - p.ex)), x2: r2(x(p.x + p.ex)), y1: r2(py), y2: r2(py), 'class': 'c-err' }, svg); }
      if (p.ey) { S('line', { x1: r2(px), x2: r2(px), y1: r2(y(p.y - p.ey)), y2: r2(y(p.y + p.ey)), 'class': 'c-err' }, svg); }
      var g = S('g', { 'class': 'mark' }, svg);
      S('circle', { cx: r2(px), cy: r2(py), r: 14, 'class': 'hit' }, g);
      if (p.ring) S('circle', { cx: r2(px), cy: r2(py), r: 5.5, style: 'fill:var(--surface);stroke:' + col(c) + ';stroke-width:2.5' }, g);
      else S('circle', { cx: r2(px), cy: r2(py), r: p.hl ? 7 : 5.5, style: 'fill:' + col(c) + ';stroke:var(--surface);stroke-width:2' }, g);
      var lx = p.lx != null ? p.lx : 10, ly = p.ly != null ? p.ly : -10;
      T(svg, px + lx, py + ly, p.label, p.hl ? 'c-lab-b' : 'c-lab', p.anchor || 'start');
      if (p.sub) T(svg, px + lx, py + ly + 15, p.sub, 'c-note', p.anchor || 'start');
      bindTip(g, { head: p.label, rows: [
        { v: fx(p.x) + (p.ex ? ' ± ' + fx(p.ex) : ''), k: sp.x.name || '' },
        { v: fy(p.y) + (p.ey ? ' ± ' + fy(p.ey) : ''), k: sp.y.name || '' }] });
    });
  };

  // Heatmap with binned sequential colour. rows x cols, values[r][c].
  TYPES.heatmap = function (svg, sp, W) {
    var f = fmtOf(sp), bins = sp.bins, rows = sp.rows, cols = sp.cols;
    var left = Math.ceil(maxW(rows, 13)) + 14, top = 26, cellH = sp.cellH || 30;
    var cw = Math.min(sp.maxCell || 130, (W - left) / cols.length), gridW = cw * cols.length;
    var H0 = top + rows.length * cellH + 4;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H0); svg.setAttribute('height', H0);
    cols.forEach(function (c, j) { T(svg, left + cw * j + cw / 2, 14, c, 'c-lab-b', 'middle'); });
    rows.forEach(function (rl, i) {
      var yy = top + i * cellH;
      T(svg, left - 10, yy + cellH / 2 + 4.5, rl, 'c-lab', 'end');
      cols.forEach(function (c, j) {
        var v = sp.values[i][j], b = 0;
        while (b < bins.length && v >= bins[b]) b++;
        var rect = S('rect', { x: r2(left + cw * j), y: yy, width: r2(cw), height: cellH, 'class': 'hm-cell mark hm-' + b }, svg);
        T(svg, left + cw * j + cw / 2, yy + cellH / 2 + 4.5, f(v), 'hm-t ' + (b === 4 ? 'mid' : b < 4 ? 'lo' : 'hi'), 'middle');
        bindTip(rect, { head: rl, rows: [{ v: f(v), k: sp.valueName ? sp.valueName + ' · ' + c : c }] });
      });
    });
    void gridW;
  };

  // Lines. series[{name, color, points:[[x,y]], markers, labels}], refs[{y, label}].
  TYPES.line = function (svg, sp, W) {
    var fx = fmtOf(sp, 'x'), fy = fmtOf(sp, 'y');
    var xt = sp.x.ticks || niceTicks(sp.x.domain[0], sp.x.domain[1], W < 520 ? 4 : 6), yt = sp.y.ticks || niceTicks(sp.y.domain[0], sp.y.domain[1], 5);
    var xtf = sp.x.tickFmt || fx, ytf = sp.y.tickFmt || fy;
    var endW = sp.endLabels ? Math.ceil(maxW(sp.series.map(function (s) { return s.name; }), 12.5, 500)) + 14 : 0;
    var left = Math.ceil(maxW(yt.map(ytf), 12)) + 14 + (sp.y.label ? 20 : 0), right = Math.max(sp.right || 14, endW), top = 14;
    var plotH = sp.height || 260, bottom = 28 + (sp.x.label ? 20 : 0), H0 = top + plotH + bottom;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H0); svg.setAttribute('height', H0);
    var x = scale(sp.x.domain[0], sp.x.domain[1], left, W - right), y = scale(sp.y.domain[0], sp.y.domain[1], top + plotH, top);
    yt.forEach(function (t) {
      S('line', { x1: left, x2: W - right, y1: r2(y(t)) + 0.5, y2: r2(y(t)) + 0.5, 'class': t === sp.y.domain[0] ? 'c-axis' : 'c-grid' }, svg);
      T(svg, left - 8, y(t) + 4, ytf(t), 'c-tick', 'end');
    });
    xt.forEach(function (t) { T(svg, x(t), top + plotH + 18, xtf(t), 'c-tick', 'middle'); });
    if (sp.x.label) T(svg, (left + W - right) / 2, H0 - 4, sp.x.label, 'c-title', 'middle');
    if (sp.y.label) T(svg, 12, top + plotH / 2, sp.y.label, 'c-title', 'middle', { transform: 'rotate(-90 12 ' + r2(top + plotH / 2) + ')' });
    (sp.refs || []).forEach(function (rf) {
      var ry = y(rf.y);
      S('line', { x1: left, x2: W - right, y1: r2(ry), y2: r2(ry), 'class': 'c-ref' }, svg);
      T(svg, rf.anchor === 'start' ? left + 6 : W - right - 4, ry - 7, rf.label, 'c-ref-t', rf.anchor || 'end');
    });
    var xs = [];
    sp.series.forEach(function (s) {
      var d = s.points.map(function (p, i) { if (xs.indexOf(p[0]) < 0) xs.push(p[0]); return (i ? 'L' : 'M') + r2(x(p[0])) + ',' + r2(y(p[1])); }).join('');
      if (!s.noLine) S('path', { d: d, style: 'fill:none;stroke:' + col(s.color) + ';stroke-width:' + (s.width || 2) + ';stroke-linejoin:round;stroke-linecap:round' }, svg);
      if (s.markers) s.points.forEach(function (p, i) {
        var g = S('g', { 'class': 'mark' }, svg);
        S('circle', { cx: r2(x(p[0])), cy: r2(y(p[1])), r: 12, 'class': 'hit' }, g);
        S('circle', { cx: r2(x(p[0])), cy: r2(y(p[1])), r: s.hl && s.hl.indexOf(i) >= 0 ? 6 : 4.5, style: 'fill:' + col(s.color) + ';stroke:var(--surface);stroke-width:2' }, g);
        if (s.labels && s.labels[i]) {
          var L = s.labels[i];
          T(svg, x(p[0]) + (L.dx || 0), y(p[1]) + (L.dy != null ? L.dy : -12), L.t, L.b ? 'c-val-b' : 'c-val', L.anchor || 'middle');
        }
        bindTip(g, { head: sp.x.name ? sp.x.name + ' ' + fx(p[0]) : fx(p[0]), rows: [{ v: fy(p[1]), k: s.name, color: s.color }] });
      });
      if (sp.endLabels) {
        var last = s.points[s.points.length - 1];
        T(svg, x(last[0]) + 8, y(last[1]) + 4.5, s.name, 'c-lab', 'start');
      }
    });
    if (sp.crosshair !== false) {
      xs.sort(function (a, b) { return a - b; });
      var cross = S('line', { x1: 0, x2: 0, y1: top, y2: top + plotH, 'class': 'c-cross', visibility: 'hidden' }, svg);
      var ov = S('rect', { x: left, y: top, width: W - left - right, height: plotH, 'class': 'hit' }, svg);
      if (sp.series.some(function (s) { return s.markers; })) svg.insertBefore(ov, svg.querySelector('.mark'));
      ov.addEventListener('pointermove', function (e) {
        var b = svg.getBoundingClientRect(), vx = (e.clientX - b.left) * (W / b.width), best = xs[0];
        xs.forEach(function (v) { if (Math.abs(x(v) - vx) < Math.abs(x(best) - vx)) best = v; });
        cross.setAttribute('x1', r2(x(best))); cross.setAttribute('x2', r2(x(best))); cross.setAttribute('visibility', 'visible');
        var rows = [];
        sp.series.forEach(function (s) { s.points.forEach(function (p) { if (p[0] === best) rows.push({ v: fy(p[1]), k: s.name, color: s.color }); }); });
        fillTip({ head: (sp.x.name ? sp.x.name + ' ' : '') + fx(best), rows: rows }); placeTip(e.clientX, e.clientY);
      });
      ov.addEventListener('pointerleave', function () { cross.setAttribute('visibility', 'hidden'); hideTip(); });
    }
  };

  // Dumbbell: before -> after per row. a/b = {name, color}; rows[{label, a, b}].
  TYPES.dumbbell = function (svg, sp, W) {
    var f = fmtOf(sp), df = signed(sp.deltaFmt ? fmtOf({ fmt: sp.deltaFmt }) : f), rows = sp.rows.slice();
    if (sp.sort === 'delta') rows.sort(function (p, q) { return (p.b - p.a) - (q.b - q.a); });
    var labW = Math.ceil(maxW(rows.map(function (r) { return r.label; }), 13)) + 14;
    var dW = Math.ceil(maxW(rows.map(function (r) { return df(r.b - r.a); }), 12.5, 600)) + 14;
    var rowH = sp.rowH || 30, top = 8, plotH = rows.length * rowH, H0 = top + plotH + 28;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H0); svg.setAttribute('height', H0);
    var x = scale(sp.domain[0], sp.domain[1], labW, W - dW), ticks = sp.ticks || niceTicks(sp.domain[0], sp.domain[1], W < 520 ? 4 : 6);
    ticks.forEach(function (t) {
      S('line', { x1: r2(x(t)) + 0.5, x2: r2(x(t)) + 0.5, y1: top, y2: top + plotH, 'class': 'c-grid' }, svg);
      T(svg, x(t), top + plotH + 18, (sp.tickFmt || f)(t), 'c-tick', 'middle');
    });
    T(svg, W - 2, top - 0, sp.deltaTitle || 'Δ', 'c-note', 'end');
    rows.forEach(function (r, i) {
      var cy = top + i * rowH + rowH / 2, xa = x(r.a), xb = x(r.b);
      T(svg, labW - 12, cy + 4.5, r.label, 'c-lab', 'end');
      var g = S('g', { 'class': 'mark' }, svg);
      S('rect', { x: r2(Math.min(xa, xb) - 10), y: r2(cy - rowH / 2), width: r2(Math.abs(xb - xa) + 20), height: rowH, 'class': 'hit' }, g);
      S('line', { x1: r2(xa), x2: r2(xb), y1: r2(cy), y2: r2(cy), 'class': 'c-conn' }, g);
      S('circle', { cx: r2(xa), cy: r2(cy), r: 5, style: 'fill:' + col(sp.a.color) + ';stroke:var(--surface);stroke-width:2' }, g);
      S('circle', { cx: r2(xb), cy: r2(cy), r: 6, style: 'fill:' + col(sp.b.color) + ';stroke:var(--surface);stroke-width:2' }, g);
      T(svg, W - 2, cy + 4.5, df(r.b - r.a), Math.abs(r.b - r.a) >= (sp.boldAt || Infinity) ? 'c-val-b' : 'c-val', 'end');
      bindTip(g, { head: r.label, rows: [{ v: f(r.a), k: sp.a.name, color: sp.a.color }, { v: f(r.b), k: sp.b.name, color: sp.b.color }, { v: df(r.b - r.a), k: 'change' }] });
    });
  };

  // Waterfall of a stacked build-up, with a dashed "prediction" track.
  // steps[0] = {label, value}; then {label, delta, alone}. Measured level = running sum of delta,
  // predicted level = running sum of alone.
  TYPES.waterfall = function (svg, sp, W) {
    var f = fmtOf(sp), sf = signed(f), steps = sp.steps, n = steps.length;
    var ticks = sp.ticks || niceTicks(sp.domain[0], sp.domain[1], 5);
    var left = Math.ceil(maxW(ticks.map(f), 12)) + 14 + (sp.yLabel ? 20 : 0), right = sp.right || 120, top = 22;
    var narrow = W < 560; if (narrow) right = 64;
    var plotH = sp.height || 280, bottom = narrow ? 44 : 30, H0 = top + plotH + bottom;
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H0); svg.setAttribute('height', H0);
    var y = scale(sp.domain[0], sp.domain[1], top + plotH, top), sw = (W - left - right) / n, bw = Math.min(40, sw * 0.46);
    ticks.forEach(function (t) {
      S('line', { x1: left, x2: W - right, y1: r2(y(t)) + 0.5, y2: r2(y(t)) + 0.5, 'class': 'c-grid' }, svg);
      T(svg, left - 8, y(t) + 4, f(t), 'c-tick', 'end');
    });
    if (sp.yLabel) T(svg, 12, top + plotH / 2, sp.yLabel, 'c-title', 'middle', { transform: 'rotate(-90 12 ' + r2(top + plotH / 2) + ')' });
    var meas = [steps[0].value], pred = [steps[0].value];
    for (var i = 1; i < n; i++) { meas.push(meas[i - 1] + steps[i].delta); pred.push(pred[i - 1] + steps[i].alone); }
    // prediction track
    var pd = pred.map(function (v, i) { return (i ? 'L' : 'M') + r2(left + sw * i + sw / 2) + ',' + r2(y(v)); }).join('');
    S('path', { d: pd, 'class': 'c-ref' }, svg);
    steps.forEach(function (st, i) {
      var cx = left + sw * i + sw / 2, bx = cx - bw / 2;
      var lab = narrow ? (st.short || st.label) : st.label;
      T(svg, cx, top + plotH + 18, lab, i === 0 ? 'c-lab' : 'c-lab', 'middle');
      if (i === 0) {
        S('line', { x1: r2(bx - 6), x2: r2(bx + bw + 6), y1: r2(y(st.value)), y2: r2(y(st.value)), style: 'stroke:var(--ink);stroke-width:2.5;stroke-linecap:round' }, svg);
        T(svg, cx, y(st.value) - 10, f(st.value), 'c-val-b', 'middle');
        return;
      }
      var a = meas[i - 1], b = meas[i], c = st.delta < 0 ? 'neg' : 'pos';
      S('line', { x1: r2(left + sw * (i - 1) + sw / 2 + bw / 2), x2: r2(bx), y1: r2(y(a)), y2: r2(y(a)), 'class': 'c-conn' }, svg);
      var yt0 = Math.min(y(a), y(b)), yh = Math.abs(y(a) - y(b));
      var g = S('g', { 'class': 'mark' }, svg);
      S('rect', { x: r2(bx - 6), y: r2(Math.min(yt0, y(pred[i])) - 10), width: r2(bw + 12), height: r2(Math.max(yh, Math.abs(y(pred[i]) - yt0)) + 20), 'class': 'hit' }, g);
      S('rect', { x: r2(bx), y: r2(yt0), width: r2(bw), height: r2(Math.max(yh, 1.5)), rx: 3, style: 'fill:' + col(c) }, g);
      S('circle', { cx: r2(cx), cy: r2(y(pred[i])), r: 5, style: 'fill:var(--surface);stroke:var(--ink-2);stroke-width:1.8' }, g);
      var below = st.delta < 0;
      T(svg, cx, below ? y(b) + 22 : y(b) - 12, sf(st.delta), 'c-val-b', 'middle');
      bindTip(g, { head: st.label, rows: [
        { v: sf(st.delta) + ' → ' + f(b), k: 'added in sequence', color: c },
        { v: sf(st.alone) + ' → ' + f(pred[i]), k: 'if it behaved as alone' }] });
    });
    // end annotations
    var ex = W - right + 10, lm = meas[n - 1], lp = pred[n - 1];
    T(svg, ex, y(lp) + 4, (narrow ? '' : 'predicted ') + f(lp), 'c-ref-t', 'start');
    T(svg, ex, y(lm) + 4, (narrow ? '' : 'measured ') + f(lm), 'c-val-b', 'start');
    if (sp.gapLabel && !narrow) {
      var gy = (y(lp) + y(lm)) / 2;
      S('line', { x1: r2(ex - 4), x2: r2(ex - 4), y1: r2(y(lp) + 8), y2: r2(y(lm) - 10), style: 'stroke:var(--neg);stroke-width:1.5' }, svg);
      T(svg, ex + 2, gy + 4, sp.gapLabel, 'c-note', 'start');
    }
  };

  /* ---------------- render all charts ---------------- */
  function render(el, force) {
    var spec = (window.CHARTS || {})[el.getAttribute('data-chart')];
    if (!spec || !TYPES[spec.type]) return;
    var w = Math.floor(el.clientWidth);
    if (!w || (!force && el._w === w)) return;
    el._w = w;
    var wasOpen = !!el.querySelector('details[open]');
    el.textContent = '';
    if (spec.legend) el.appendChild(legend(spec.legend));
    var svg = S('svg', { role: 'img', 'aria-label': spec.aria || '', width: w }, el);
    TYPES[spec.type](svg, spec, w);
    if (spec.scaleLegend) el.appendChild(spec.scaleLegend());
    var t = dataTable(spec, wasOpen);
    if (t) el.appendChild(t);
  }
  function renderAll(force) { [].forEach.call(doc.querySelectorAll('.chart[data-chart]'), function (el) { render(el, force); }); }

  function init() {
    var b = doc.getElementById('theme-toggle');
    if (b) b.addEventListener('click', toggleTheme);
    syncToggle();
    initToc();
    initCopy();
    renderAll(true);
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(function () { renderAll(true); });
    var timer = null;
    window.addEventListener('resize', function () { clearTimeout(timer); timer = setTimeout(function () { renderAll(false); }, 120); });
  }
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', init); else init();

  window.PaperCharts = { render: renderAll, helpers: { H: H } };
})();
