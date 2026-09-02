"""LinkedIn company banner for Citetome.

Replaces the old banner, which still carried "AI visibility audits for
multilingual SMBs. Findable. Citeable. Trustworthy in AI search." That is the
positioning the site moved off on 24 August.

Design follows img/og-card.png: cream #F3EEE2, ink #0F0E0C, gold #B8915E, the
three-bar mark with its heavy underline, a serif italic wordmark, and tracked
mono uppercase in gold for the small marks. Georgia stands in for EB Garamond,
which is the site's own declared fallback in --serif.

Type is fitted by measurement rather than guessed, so the headline cannot
overflow the right edge or collide with the mono column.

Rendered at 2x LinkedIn's 1128x191 so it survives their downscale.
"""

from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw, ImageFont

S = 2
W, H = 1128 * S, 191 * S

BG = (243, 238, 226)
INK = (15, 14, 12)
GOLD = (184, 145, 94)
RULE = (222, 212, 189)

FONTS = pathlib.Path("C:/Windows/Fonts")
GEORGIA = str(FONTS / "georgia.ttf")
GEORGIA_I = str(FONTS / "georgiai.ttf")
CONSOLA = str(FONTS / "consola.ttf")

im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
cy = H // 2

MARGIN = 56 * S
MONO_TRACK = 2 * S


def tracked_width(text, font):
    return sum(d.textlength(c, font=font) + MONO_TRACK for c in text) - MONO_TRACK


def draw_tracked(xy, text, font, fill):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + MONO_TRACK


# --- mark: three bars, middle gold and taller, on a heavy underline ---------
bw, gap = 13 * S, 8 * S
h_outer, h_mid = 44 * S, 56 * S
base = cy + 22 * S
mx = MARGIN

for i, (h, colour) in enumerate([(h_outer, INK), (h_mid, GOLD), (h_outer, INK)]):
    x0 = mx + i * (bw + gap)
    d.rectangle([x0, base - h, x0 + bw, base], fill=colour)

bars_w = 3 * bw + 2 * gap
d.rectangle(
    [mx - 5 * S, base + 6 * S, mx + bars_w + 5 * S, base + 10 * S], fill=INK
)
mark_right = mx + bars_w + 5 * S

# --- wordmark ---------------------------------------------------------------
wordmark = ImageFont.truetype(GEORGIA_I, 54 * S)
wx = mark_right + 26 * S
wa, wd = wordmark.getbbox("citetome")[1], wordmark.getbbox("citetome")[3]
d.text((wx, cy - (wa + wd) / 2), "citetome", font=wordmark, fill=INK)
word_right = wx + d.textlength("citetome", font=wordmark)

# --- mono column, right ------------------------------------------------------
mono = ImageFont.truetype(CONSOLA, 11 * S)
est = "EST. COPENHAGEN 2026"
url = "citetome.com"
mono_left = W - MARGIN - max(tracked_width(est, mono), tracked_width(url, mono))
draw_tracked((W - MARGIN - tracked_width(est, mono), 34 * S), est, mono, GOLD)
draw_tracked((W - MARGIN - tracked_width(url, mono), H - 46 * S), url, mono, GOLD)

# --- divider -----------------------------------------------------------------
rx = int(word_right + 40 * S)
d.rectangle([rx, cy - 40 * S, rx + S, cy + 40 * S], fill=RULE)

# --- headline, fitted --------------------------------------------------------
LINES = ("Evidence-led organic growth", "for Google and AI search.")
hx = rx + 40 * S
# The mono marks sit at the top and bottom edges; the headline occupies the
# vertical middle, so they share the right side without ever overlapping.
# Fitting to the margin rather than to the mono column buys real type size.
available = W - MARGIN - hx

size = 46 * S
while size > 14 * S:
    roman = ImageFont.truetype(GEORGIA, size)
    italic = ImageFont.truetype(GEORGIA_I, size)
    widest = max(
        d.textlength(LINES[0], font=roman), d.textlength(LINES[1], font=italic)
    )
    if widest <= available:
        break
    size -= S

leading = int(size * 1.28)
top = cy - leading + int(size * 0.30)
d.text((hx, top), LINES[0], font=roman, fill=INK)
d.text((hx, top + leading), LINES[1], font=italic, fill=INK)

out = pathlib.Path(
    r"C:\Users\benza\AppData\Local\Temp\claude"
    r"\C--Users-benza-OneDrive----------"
    r"\22210507-f925-4b02-93ad-5b2500f5916b\scratchpad\citetome-linkedin-banner.png"
)
im.save(out, "PNG")
print(f"headline fitted at {size // S}px (1x), available {available // S}px")
print(f"{out}  {im.size[0]}x{im.size[1]}  {out.stat().st_size // 1024} KB")
