# mudassiruddin7.github.io

Personal academic homepage of **Mohammed Mudassir Uddin** — researcher, builder and founder from Hyderabad, India.

🌐 **Live site:** [mudassiruddin7.github.io](https://mudassiruddin7.github.io)

## Structure

```
index.html                 # the whole page: sidebar, nav and every section
assets/css/main.css        # compiled theme stylesheet (themes, layout, components)
assets/js/main.min.js      # theme JS (jQuery, smooth scroll, magnific popup)
assets/js/custom-scripts.js# theme switcher, sidebar pin, publication filter, news toggle
assets/fonts/              # Font Awesome 5 webfonts
images/profile.jpg         # sidebar photo (cropped from hero2.jpeg)
images/hero2.jpeg          # full-size photo, opened when the sidebar photo is clicked
images/papers/*.svg        # one architecture diagram per paper
images/favicon*, images/site.webmanifest
tools/diagrams/            # the scripts that generate images/papers/*.svg
agentcompress/  hagd/  pmp-dacis/  laf-yolov10/
                           # one project page per paper: index.html + og.png (link preview)
laf-yolov10/img/           # detection examples shown on the LAF-YOLOv10 page
assets/paper/paper.css     # shared styles for the project pages (light, dark, tinted themes)
assets/paper/paper.js      # theme sync, contents rail, BibTeX copy, and the SVG chart code
blog/                      # generated blog: index.html, one folder per post, feed.xml
assets/blog/blog.css       # blog layout on top of paper.css
tools/blog/                # build.py and the post sources in posts/
files/                     # the CV PDF linked from the sidebar and About Me
```

## Blog

Posts are written as plain HTML fragments in `tools/blog/posts/`, one file each, named
`YYYY-MM-NN-slug.html` (the month the post is filed under, its order inside the month, and its URL).
Each file starts with a comment holding `title`, `dek` and `tags`. Run `python tools/blog/build.py`
from the repository root to regenerate `blog/`, including the index and the RSS feed. Inside a post,
`{root}` points at the site root and `{blog}` at the blog root, and a `window.CHARTS` block draws charts
with the same code as the project pages.

## Project pages

Each paper has its own page at `mudassiruddin7.github.io/<name>/`, linked from its `paper-box` as
"Project page". A page is plain HTML with no build step:

- Text, tables and diagrams are written directly in the page's `index.html`. Diagrams are inline SVG and
  take their colours from the theme tokens in `paper.css`, so they follow light and dark mode.
- Charts are drawn by `paper.js` from the `window.CHARTS` specs at the bottom of each page. Change a number
  there and the chart, its tooltip and its "Show data" table all update.
- Equations are native MathML, so no maths library is loaded.
- The pages read and write the same `site-theme` setting as the homepage, so the chosen theme carries over.

## Editing content

All content lives in `index.html`, in the order it appears on the page. Each section starts with an
`<h1 id="-section-name">` that the top navigation links to:

| Section | What to edit |
|---|---|
| About Me | the three intro paragraphs, the quote, and the `app-cards` grid of projects |
| News | `<li>` items inside `#newsContent` — newest first, `<em>YYYY.MM:</em>` prefix |
| Publications | one `<div class="paper-box">` per paper; `data-core="true"` marks first-author work and shows the green badge |
| Honors, Hackathons, Education, Ventures, Certifications, Others | plain `<ul>` lists |

To add a paper: copy an existing `paper-box` block, swap the image, title, venue line, author list and links.
Wrap your own name in `<strong><span class="author-highlight">…</span></strong>`.

To change the navigation, edit the `<ul class="site-nav__links">` at the top and keep the `href` in sync with the
section's `id`.

## Credits

(MIT, see `LICENSE`), based on AcadHomepage and the Minimal Mistakes Jekyll theme.
