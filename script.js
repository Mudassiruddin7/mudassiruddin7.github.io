/* ══════════════════════════════════════════
   PORTFOLIO — SCRIPT
   Mohammed Mudassir Uddin · 2026
   ══════════════════════════════════════════ */

(function () {
    'use strict';

    const $ = (sel, ctx = document) => ctx.querySelector(sel);
    const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];
    const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

    // ══════════════════════════════════════════
    // TYPING ANIMATION
    // ══════════════════════════════════════════
    (function initTyping() {
        const line     = $('#typingLine');
        const cursor   = $('.typing-cursor');
        if (!line) return;

        const text     = "I  build  things\nthat  shouldn't\nexist  yet.";
        const chars    = [...text];
        let idx        = 0;
        let started    = false;

        function type() {
            if (idx >= chars.length) {
                // Hold cursor briefly then restart loop correctly
                setTimeout(() => {
                    if (cursor) {
                        cursor.style.animation = 'none';
                        cursor.style.opacity = '0';
                        setTimeout(() => {
                            line.innerHTML = '';
                            idx = 0;
                            cursor.style.animation = 'cursorBlink .85s step-end infinite';
                            cursor.style.opacity = '1';
                            started = false;
                            setTimeout(type, 300); // give it a small breath before re-typing
                        }, 600);
                    }
                }, 2800);
                return;
            }
            const ch = chars[idx];
            if (ch === '\n') {
                line.innerHTML += '<br>';
            } else {
                line.innerHTML += ch;
            }
            idx++;

            // Variable speed — faster mid-word, slight pause on punctuation
            let delay = 48;
            if (ch === ' ')  delay = 38;
            if (ch === '\n') delay = 120;
            if (ch === '.')  delay = 320;
            if (ch === "'")  delay = 30;
            if (ch === '!')  delay = 300;
            if (ch === '?')  delay = 280;
            if (ch === ',')  delay = 180;

            setTimeout(type, delay);
        }

        // Start typing after a brief delay
        setTimeout(() => {
            // Mark accent word so we can show it in gold after typing
            type();
        }, 600);
    })();

    // ══════════════════════════════════════════
    // CUSTOM CURSOR
    // ══════════════════════════════════════════
    if (!isTouch) {
        const cursor = $('#cursor');
        let cx = window.innerWidth / 2, cy = window.innerHeight / 2;
        let tx = cx, ty = cy;

        document.addEventListener('mousemove', (e) => { tx = e.clientX; ty = e.clientY; });

        (function lerpCursor() {
            const ease = 0.20;
            cx += (tx - cx) * ease;
            cy += (ty - cy) * ease;
            cursor.style.left = cx + 'px';
            cursor.style.top  = cy + 'px';
            requestAnimationFrame(lerpCursor);
        })();

        document.addEventListener('mouseover', (e) => {
            const el = e.target;
            if (el.closest('a, button, .project-card, .vision-cta, .cta-primary, .cta-ghost, .contact-email, .hm-sq')) {
                document.body.classList.add('cursor-link');
                document.body.classList.remove('cursor-text');
            } else if (el.matches('p, h1, h2, h3, li, .manifesto-line, .tl-body *')) {
                document.body.classList.add('cursor-text');
                document.body.classList.remove('cursor-link');
            } else {
                document.body.classList.remove('cursor-link', 'cursor-text');
            }
        });
    }

    // ══════════════════════════════════════════
    // NAVBAR
    // ══════════════════════════════════════════
    const navbar  = $('#navbar');
    const hero    = $('#hero');

    function syncNavbar() {
        if (!hero) return;
        const heroBottom = hero.getBoundingClientRect().bottom;
        navbar.classList.toggle('visible', heroBottom < 80);
    }
    window.addEventListener('scroll', syncNavbar, { passive: true });
    syncNavbar();

    // Active section
    const navLinks = $$('.nav-link');
    const sections = $$('section[id]');

    function updateActive() {
        const mid = window.scrollY + window.innerHeight * 0.4;
        let active = '';
        sections.forEach(s => { if (s.offsetTop <= mid) active = s.id; });
        navLinks.forEach(l => l.classList.toggle('active', l.dataset.section === active));
    }
    window.addEventListener('scroll', updateActive, { passive: true });
    updateActive();

    // Smooth scroll
    $$('a[href^="#"]').forEach(a => {
        a.addEventListener('click', e => {
            const t = $(a.getAttribute('href'));
            if (!t) return;
            e.preventDefault();
            t.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });

    // ══════════════════════════════════════════
    // SCROLL REVEAL
    // ══════════════════════════════════════════
    const revealObs = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.08, rootMargin: '0px 0px -56px 0px' });

    $$('.reveal, .journey-item').forEach(el => revealObs.observe(el));

    // Manifesto lines — sequential stagger
    const manifestoSection = $('.manifesto-lines');
    if (manifestoSection) {
        const manifestoObs = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                const lines = $$('.reveal-line', manifestoSection);
                lines.forEach((l, i) => setTimeout(() => l.classList.add('visible'), i * 120));
                manifestoObs.disconnect();
            });
        }, { threshold: 0.15 });
        manifestoObs.observe(manifestoSection);
    }

    // Paper entries
    $$('.paper-entry').forEach((el, i) => {
        el.style.cssText += `opacity:0;transform:translateX(-10px);transition:opacity .55s cubic-bezier(0.16,1,0.3,1) ${i * 55}ms,transform .55s cubic-bezier(0.16,1,0.3,1) ${i * 55}ms`;
    });
    new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) { e.target.style.opacity = '1'; e.target.style.transform = 'translateX(0)'; }
        });
    }, { threshold: 0.06, rootMargin: '0px 0px -24px 0px' }).observe($('#research') || document.body);

    const paperObs = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) { e.target.style.opacity = '1'; e.target.style.transform = 'translateX(0)'; }
        });
    }, { threshold: 0.05 });
    $$('.paper-entry').forEach(el => paperObs.observe(el));

    // ══════════════════════════════════════════
    // COUNTER ANIMATION
    // ══════════════════════════════════════════
    function easeOutElastic(t) {
        const c4 = (2 * Math.PI) / 3;
        if (t === 0) return 0;
        if (t === 1) return 1;
        return Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * c4) + 1;
    }

    function animateCounter(el) {
        const target   = parseInt(el.dataset.target, 10);
        const prefix   = el.dataset.prefix  || '';
        const suffix   = el.dataset.suffix  || '';
        const duration = 1600;
        const startTS  = performance.now();
        function tick(now) {
            const raw    = Math.min((now - startTS) / duration, 1);
            const eased  = easeOutElastic(raw);
            el.textContent = prefix + Math.round(target * eased).toLocaleString('en-IN') + suffix;
            if (raw < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
    }

    const numbersSection = $('#numbers');
    if (numbersSection) {
        new IntersectionObserver((entries) => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    $$('.stat-num', e.target).forEach(animateCounter);
                    e.target._counterDone = true;
                    // Unobserve to prevent re-firing
                    entries.forEach(() => {});
                }
            });
        }, { threshold: 0.2 }).observe(numbersSection);
    }

    // ══════════════════════════════════════════
    // GITHUB HEATMAP
    // ══════════════════════════════════════════
    (function buildHeatmap() {
        const grid = $('#heatmap');
        if (!grid) return;
        for (let w = 0; w < 52; w++) {
            for (let d = 0; d < 7; d++) {
                const sq = document.createElement('div');
                sq.className = 'hm-sq';
                const isWeekend = d === 0 || d === 6;
                const r = Math.random();
                const level = isWeekend
                    ? (r < .45 ? 0 : r < .65 ? 1 : r < .80 ? 2 : r < .92 ? 3 : 4)
                    : (r < .10 ? 0 : r < .28 ? 1 : r < .50 ? 2 : r < .75 ? 3 : 4);
                sq.classList.add('l' + level);
                sq.style.cssText = `opacity:0;transform:scale(0);transition:opacity .4s ease ${(w*7+d)*2}ms,transform .4s cubic-bezier(0.34,1.56,0.64,1) ${(w*7+d)*2}ms`;
                grid.appendChild(sq);
            }
        }
        new IntersectionObserver((entries) => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    $$('.hm-sq', grid).forEach(sq => {
                        sq.style.opacity = '1';
                        sq.style.transform = 'scale(1)';
                    });
                }
            });
        }, { threshold: 0.1 }).observe(grid);
    })();

    // ══════════════════════════════════════════
    // PROJECT CARD 3D TILT
    // ══════════════════════════════════════════
    if (!isTouch) {
        $$('.project-card').forEach(card => {
            card.addEventListener('mousemove', e => {
                const r = card.getBoundingClientRect();
                const mx = ((e.clientX - r.left) / r.width  - 0.5) * 2;
                const my = ((e.clientY - r.top)  / r.height - 0.5) * 2;
                card.style.transform = `translateY(-6px) scale(1.01) perspective(800px) rotateX(${my * -4}deg) rotateY(${mx * 4}deg)`;
            });
            card.addEventListener('mouseleave', () => {
                card.style.transition = 'transform .55s cubic-bezier(0.175,0.885,0.32,1.275), box-shadow .35s ease, border-color .35s ease';
                card.style.transform = '';
            });
            card.addEventListener('mouseenter', () => {
                card.style.transition = 'transform .12s ease, box-shadow .35s ease, border-color .35s ease';
            });
        });
    }

    // ══════════════════════════════════════════
    // TIMELINE DOT HIGHLIGHT
    // ══════════════════════════════════════════
    new IntersectionObserver((entries) => {
        entries.forEach(e => {
            const dot = e.target.querySelector('.tl-dot');
            if (!dot) return;
            if (e.isIntersecting) {
                dot.style.background = 'var(--gold)';
                dot.style.boxShadow = '0 0 0 5px rgba(139,107,20,0.12)';
            } else if (!dot.classList.contains('gold-dot')) {
                dot.style.background = '';
                dot.style.boxShadow = '';
            }
        });
    }, { threshold: 0.5 }).observe(document.body);

    $$('.tl-item').forEach(item => {
        new IntersectionObserver((entries) => {
            entries.forEach(e => {
                const dot = e.target.querySelector('.tl-dot');
                if (!dot) return;
                if (e.isIntersecting) {
                    dot.style.background = 'var(--gold)';
                    dot.style.boxShadow = '0 0 0 5px rgba(139,107,20,0.12)';
                } else if (!dot.classList.contains('gold-dot')) {
                    dot.style.background = '';
                    dot.style.boxShadow = '';
                }
            });
        }, { threshold: 0.5 }).observe(item);
    });

    // ══════════════════════════════════════════
    // SCROLL VELOCITY — headline weight
    // ══════════════════════════════════════════
    let lastY = window.scrollY;
    (function velocityLoop() {
        const y   = window.scrollY;
        const vel = Math.abs(y - lastY);
        lastY = y;
        const weight = Math.round(Math.max(300, 700 - vel * 7));
        const hl = $('.hero-headline');
        if (hl) hl.style.fontWeight = weight;
        requestAnimationFrame(velocityLoop);
    })();

    // ══════════════════════════════════════════
    // INIT
    // ══════════════════════════════════════════
    syncNavbar();
    updateActive();

})();
