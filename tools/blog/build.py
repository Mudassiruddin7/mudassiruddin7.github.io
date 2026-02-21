"""Build the blog: blog/index.html, one page per post, and blog/feed.xml.

Posts live in tools/blog/posts/, one file each, named YYYY-MM-NN-slug.html:
YYYY-MM is the month the post is filed under, NN orders posts inside a month,
and slug becomes the URL (/blog/slug/). Each file starts with a metadata comment:

    <!--
    title: Four validated upgrades that don't add up
    dek: One sentence shown under the title and on the index.
    tags: paper, computer vision
    -->

and the rest of the file is the post body in plain HTML. Inside the body,
{root} expands to the site root and {blog} to the blog root, so
<img src="{root}images/papers/hagd.svg"> and <a href="{blog}hagd-audit/"> work
from any post. A post can define window.CHARTS in a <script> block; paper.js
draws every <div class="chart" data-chart="name"> from it.

Run from the repository root:  python tools/blog/build.py
"""
import html
import pathlib
import re
from datetime import datetime, timezone
from email.utils import format_datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "tools" / "blog" / "posts"
OUT = ROOT / "blogs"
SITE = "https://mudassiruddin7.github.io"
AUTHOR = "Mohammed Mudassir Uddin"

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

THEME_BOOT = ("<script>(function(){var t=null;try{t=localStorage.getItem('site-theme')}catch(e){}"
              "var r=document.documentElement;if(t==='dark')r.setAttribute('data-theme','dark');"
              "else if(t==='yellow'||t==='blue')r.setAttribute('data-theme',t);"
              "else if(t==='white')r.setAttribute('data-theme','light');})();</script>")

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500'
         '&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;'
         '0,8..60,600;1,8..60,400&display=swap">')

THEME_BTN = ('<button class="theme" id="theme-toggle" type="button" aria-label="Switch theme">'
             '<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.2" fill="none" '
             'stroke="currentColor" stroke-width="1.4"/><path d="M8 1.8a6.2 6.2 0 0 1 0 12.4z" '
             'fill="currentColor"/></svg></button>')


def month_label(ym):
    y, m = ym.split("-")
    return f"{MONTHS[int(m) - 1]} {y}"


def load_posts():
    posts = []
    for f in sorted(SRC.glob("*.html")):
        m = re.match(r"(\d{4}-\d{2})-(\d{2})-(.+)\.html$", f.name)
        if not m:
            raise SystemExit(f"bad post filename: {f.name}")
        text = f.read_text(encoding="utf-8")
        meta_m = re.match(r"\s*<!--(.*?)-->", text, flags=re.S)
        if not meta_m:
            raise SystemExit(f"missing metadata comment: {f.name}")
        meta = {}
        for line in meta_m.group(1).strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        for key in ("title", "dek"):
            if key not in meta:
                raise SystemExit(f"{f.name}: missing '{key}'")
        posts.append({
            "month": m.group(1), "order": int(m.group(2)), "slug": m.group(3),
            "title": meta["title"], "dek": meta["dek"],
            "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
            "body": text[meta_m.end():].strip(),
        })
    posts.sort(key=lambda p: (p["month"], p["order"]))
    return posts


def topbar(root, current):
    links = [("Blog", f"{root}blogs/", current == "index"),
             ("Research", f"{root}#-publications", False),
             ("CV", "https://drive.google.com/file/d/1gz7MvatR6PW-qhG1u03cm1_K6LDS6_O4/view", False)]
    current_attr = ' aria-current="page"'
    nav = "".join(
        f'<a href="{href}"{current_attr if cur else ""}>{name}</a>' for name, href, cur in links)
    return (f'<header class="topbar">\n  <div class="wrap topbar-in">\n'
            f'    <a class="home" href="{root}"><span class="back" aria-hidden="true">&larr;</span>{AUTHOR}</a>\n'
            f'    <nav class="papers" aria-label="Site">{nav}</nav>\n'
            f'    {THEME_BTN}\n  </div>\n</header>')


def footer(root):
    return (f'<footer class="foot">\n  <div class="wrap foot-in">\n'
            f'    <span><a href="{root}">{AUTHOR}</a> &middot; Blog</span>\n'
            f'    <nav aria-label="More"><a href="{root}blogs/">All posts</a><a href="{root}blogs/feed.xml">RSS</a>'
            f'<a href="{root}#-publications">Research</a><a href="https://github.com/Mudassiruddin7">GitHub</a></nav>\n'
            f'  </div>\n</footer>')


def head(title, desc, url, root, og_type):
    return (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<title>{html.escape(title)}</title>\n'
            f'<meta name="description" content="{html.escape(desc)}">\n'
            f'<meta name="author" content="{AUTHOR}">\n'
            f'<link rel="canonical" href="{url}">\n'
            f'<meta property="og:type" content="{og_type}">\n'
            f'<meta property="og:site_name" content="{AUTHOR}">\n'
            f'<meta property="og:title" content="{html.escape(title)}">\n'
            f'<meta property="og:description" content="{html.escape(desc)}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{SITE}/images/profile.jpg">\n'
            f'<meta name="twitter:card" content="summary">\n'
            f'<link rel="alternate" type="application/rss+xml" title="{AUTHOR}: blog" href="{SITE}/blogs/feed.xml">\n'
            f'<link rel="icon" href="{root}images/favicon.ico">\n'
            f'<link rel="icon" type="image/png" sizes="32x32" href="{root}images/favicon-32x32.png">\n'
            f'<link rel="apple-touch-icon" sizes="180x180" href="{root}images/apple-touch-icon.png">\n'
            f'{THEME_BOOT}\n{FONTS}\n'
            f'<link rel="stylesheet" href="{root}assets/paper/paper.css">\n'
            f'<link rel="stylesheet" href="{root}assets/blog/blog.css">\n</head>')


def render_post(p, prev_p, next_p):
    root, blog = "../../", "../"
    body = p["body"].replace("{root}", root).replace("{blog}", blog)
    url = f"{SITE}/blogs/{p['slug']}/"
    tags = "".join(f"<span>{html.escape(t)}</span>" for t in p["tags"])
    nav = ['  <nav class="post-nav" aria-label="More posts">']
    nav.append(f'<a class="prev" href="{blog}{prev_p["slug"]}/"><span class="pn-l">Earlier</span>'
               f'<span class="pn-t">{html.escape(prev_p["title"])}</span></a>' if prev_p else "<span></span>")
    nav.append(f'<a class="next" href="{blog}{next_p["slug"]}/"><span class="pn-l">Later</span>'
               f'<span class="pn-t">{html.escape(next_p["title"])}</span></a>' if next_p else "<span></span>")
    nav.append("</nav>")
    return "\n".join([
        head(f"{p['title']} | {AUTHOR}", p["dek"], url, root, "article"),
        '<body class="acc-blue">',
        '<a class="skip" href="#main">Skip to content</a>',
        topbar(root, "post"),
        '<div class="wrap">',
        '  <header class="post-hero">',
        f'    <p class="eyebrow"><span class="name"><a href="{blog}">Blog</a></span>'
        f'<span>{month_label(p["month"])}</span>{tags}</p>',
        f'    <h1 class="title">{html.escape(p["title"])}</h1>',
        f'    <p class="subtitle">{html.escape(p["dek"])}</p>',
        '  </header>',
        f'  <main id="main" class="post">\n{body}\n  </main>',
        "\n".join(nav),
        '</div>',
        footer(root),
        f'<script src="{root}assets/paper/paper.js" defer></script>',
        '</body>\n</html>\n',
    ])


def render_index(posts):
    root = "../"
    groups = {}
    for p in posts:
        groups.setdefault(p["month"], []).append(p)
    parts = []
    for ym in sorted(groups, reverse=True):
        items = []
        for p in sorted(groups[ym], key=lambda q: q["order"], reverse=True):
            tags = "".join(f"<span>{html.escape(t)}</span>" for t in p["tags"])
            items.append(f'      <li class="post-item"><a class="t" href="{p["slug"]}/">{html.escape(p["title"])}</a>'
                         f'<p class="d">{html.escape(p["dek"])}</p><p class="tags">{tags}</p></li>')
        parts.append(f'  <section class="month" aria-labelledby="m-{ym}">\n'
                     f'    <h2 id="m-{ym}">{month_label(ym)}</h2>\n    <ul class="post-list">\n'
                     + "\n".join(items) + "\n    </ul>\n  </section>")
    desc = "Short notes, month by month, on what I built, what broke and what I learned."
    return "\n".join([
        head(f"Blog | {AUTHOR}", desc, f"{SITE}/blogs/", root, "website"),
        '<body class="acc-blue">',
        '<a class="skip" href="#main">Skip to content</a>',
        topbar(root, "index"),
        '<div class="wrap">',
        '  <header class="blog-hero">',
        f'    <p class="eyebrow"><span class="name">Blog</span><span>{len(posts)} posts</span>'
        f'<span>{month_label(posts[0]["month"])} to {month_label(posts[-1]["month"])}</span></p>',
        '    <h1 class="title">What I built, what broke, what I learned</h1>',
        f'    <p class="subtitle">{desc} Papers, hackathons, tools and the occasional audit of my own work.</p>',
        '    <p class="blog-note">Most of these were written up in September 2026 from my notes, commits and '
        'posts at the time, and are filed under the month they describe.</p>',
        '  </header>',
        '  <main id="main" class="blog-index">\n' + "\n".join(parts) + '\n  </main>',
        '</div>',
        footer(root),
        f'<script src="{root}assets/paper/paper.js" defer></script>',
        '</body>\n</html>\n',
    ])


def render_feed(posts):
    items = []
    for p in sorted(posts, key=lambda q: (q["month"], q["order"]), reverse=True):
        y, m = p["month"].split("-")
        when = format_datetime(datetime(int(y), int(m), 1, tzinfo=timezone.utc))
        url = f"{SITE}/blogs/{p['slug']}/"
        items.append(f"  <item>\n    <title>{html.escape(p['title'])}</title>\n    <link>{url}</link>\n"
                     f"    <guid>{url}</guid>\n    <pubDate>{when}</pubDate>\n"
                     f"    <description>{html.escape(p['dek'])}</description>\n  </item>")
    return ('<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0">\n<channel>\n'
            f"  <title>{AUTHOR}: blog</title>\n  <link>{SITE}/blogs/</link>\n"
            "  <description>What I built, what broke, what I learned.</description>\n"
            "  <language>en</language>\n" + "\n".join(items) + "\n</channel>\n</rss>\n")


def main():
    posts = load_posts()
    OUT.mkdir(exist_ok=True)
    for i, p in enumerate(posts):
        d = OUT / p["slug"]
        d.mkdir(exist_ok=True)
        prev_p = posts[i - 1] if i > 0 else None
        next_p = posts[i + 1] if i + 1 < len(posts) else None
        (d / "index.html").write_text(render_post(p, prev_p, next_p), encoding="utf-8", newline="\n")
    (OUT / "index.html").write_text(render_index(posts), encoding="utf-8", newline="\n")
    (OUT / "feed.xml").write_text(render_feed(posts), encoding="utf-8", newline="\n")
    print(f"built {len(posts)} posts into {OUT}")


if __name__ == "__main__":
    main()
