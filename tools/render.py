"""Render an HTML timeline (window.render(t)) to PNG frames / stills with Playwright.
usage: python3 render.py <html> <outdir> <duration> [fps]        -> frames
       python3 render.py <html> <out.png> --still <t>             -> one still
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

html = pathlib.Path(sys.argv[1]).resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--font-render-hinting=none"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    pg.goto(html); pg.wait_for_timeout(400)
    if "--still" in sys.argv:
        t = float(sys.argv[sys.argv.index("--still") + 1])
        pg.evaluate(f"render({t})"); pg.screenshot(path=sys.argv[2])
    else:
        out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
        dur = float(sys.argv[3]); fps = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        for i in range(int(dur * fps)):
            pg.evaluate(f"render({i / fps})")
            pg.screenshot(path=str(out / f"f{i:05d}.png"))
    b.close()
