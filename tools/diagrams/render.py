"""Render paper SVGs to PNG (full size and a 330px thumbnail) with headless Chrome."""
import glob, os, re, subprocess, sys

CHROME = os.environ.get("CHROME", r"C:\Program Files\Google\Chrome\Application\chrome.exe")
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'images', 'papers'))
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_previews')
os.makedirs(R, exist_ok=True)


def shot(url, w, h, png):
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                    f'--window-size={w},{h}', f'--screenshot={png}', url], capture_output=True, timeout=60)


names = sys.argv[1:] or [os.path.basename(p) for p in glob.glob(os.path.join(OUT, '*.svg'))]
for n in names:
    svg = os.path.join(OUT, n)
    w, h = map(int, re.search(r'width="(\d+)" height="(\d+)"', open(svg, encoding='utf-8').read()).groups())
    url = 'file:///' + svg.replace('\\', '/')
    shot(url, w, h, os.path.join(R, n.replace('.svg', '.png')))
    tw, th = 330, round(330 * h / w)
    page = os.path.join(R, 'thumb_' + n.replace('.svg', '.html'))
    with open(page, 'w', encoding='utf-8') as f:
        f.write(f'<html><body style="margin:0;background:#fff"><img src="{url}" style="width:{tw}px;display:block"></body></html>')
    shot('file:///' + page.replace('\\', '/'), tw, th, os.path.join(R, 'thumb_' + n.replace('.svg', '.png')))
    print('rendered', n, f'{w}x{h}')
