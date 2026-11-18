#!/usr/bin/env python3
"""Build high-resolution circled coin masters for the Coins & Money pack.

Why: the shared _img_circle helper downsamples every picture to
280x280 px. The largest coins in the pack are drawn 96pt across, so
they printed at only ~210 PPI, below the 300 PPI print standard, and
looked soft. These masters are 900x900 px, so even the largest coin
(104pt across) prints at over 600 PPI.

Method mirrors _img_circle's zoom path (same disc detection,
1.06x square crop instead of its 1.14x, so the margin ring
is thin) so the relative sizes and framing stay identical;
only the resolution changes. The square is padded with the
background color at alpha 0, so the margin stays
transparent and the panel or page shows through, with no
dark ring around the penny and no white halo around the
silver coins. A circular alpha mask keeps the corners
transparent. The builder draws these masters directly
with drawImage plus the same light border ring.
"""
import os

from PIL import Image as PILImage
from PIL import ImageDraw as _ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "assets", "coins-and-money")
OUT = os.path.join(SRC, "hi")
SIZE = 900

COINS = {
    "penny": "coin-penny.png",
    "nickel": "coin-nickel.jpg",
    "dime": "coin-dime.jpg",
    "quarter": "coin-quarter.jpg",
}


def build(name, src_path, out_path):
    im = PILImage.open(src_path).convert("RGBA")
    # Disc detection on a 200px copy (same threshold as _img_circle).
    small = im.convert("RGB").resize((200, 200), PILImage.BILINEAR)
    px = small.load()
    corners = [px[2, 2], px[197, 2], px[2, 197], px[197, 197]]
    bg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))
    minx, miny, maxx, maxy = 200, 200, -1, -1
    for yy in range(200):
        for xx in range(200):
            r, g, b = px[xx, yy]
            if max(abs(r - bg[0]), abs(g - bg[1]),
                   abs(b - bg[2])) > 24:
                minx, maxx = min(minx, xx), max(maxx, xx)
                miny, maxy = min(miny, yy), max(maxy, yy)
    W, H = im.size
    x0, x1 = minx * W / 200.0, (maxx + 1) * W / 200.0
    y0, y1 = miny * H / 200.0, (maxy + 1) * H / 200.0
    side = int(max(x1 - x0, y1 - y0) * 1.06)
    ccx, ccy = (x0 + x1) / 2, (y0 + y1) / 2
    sx0, sy0 = int(ccx - side / 2), int(ccy - side / 2)
    # Fill with the background color at alpha 0 (not plain
    # transparent black): the LANCZOS resize below blends
    # neighbouring pixels, and transparent-black pixels
    # would darken the margin into a black ring. The RGB
    # of a fully transparent pixel does not show; only
    # its blend into the edge matters.
    canvas = PILImage.new("RGBA", (side, side), bg + (0,))
    ix0, iy0 = max(0, sx0), max(0, sy0)
    ix1, iy1 = min(W, sx0 + side), min(H, sy0 + side)
    canvas.paste(im.crop((ix0, iy0, ix1, iy1)), (ix0 - sx0, iy0 - sy0))
    canvas = canvas.resize((SIZE, SIZE), PILImage.LANCZOS)
    mask = PILImage.new("L", (SIZE, SIZE), 0)
    _ImageDraw.Draw(mask).ellipse((0, 0, SIZE, SIZE), fill=255)
    # Keep the canvas's own alpha inside the circle (the
    # margin stays transparent so the panel or page shows
    # through) and only cut the corners off. putalpha(mask)
    # would force the whole circle opaque and resurrect
    # the background as a ring.
    from PIL import ImageChops
    canvas.putalpha(ImageChops.darker(canvas.split()[3], mask))
    canvas.save(out_path)
    print("%s: %s -> %s (%s, disc %.2f x %.2f of frame)"
          % (name, im.size, canvas.size,
             os.path.getsize(out_path),
             (maxx - minx + 1) / 200.0 * 1.0,
             (maxy - miny + 1) / 200.0 * 1.0))


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fname in COINS.items():
        build(name, os.path.join(SRC, fname),
              os.path.join(OUT, "coin-%s-900.png" % name))


if __name__ == "__main__":
    main()
