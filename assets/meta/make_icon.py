# Meta app icon, made in code (PIL only). python3 assets/meta/make_icon.py -> app-icon-1024-a.png, -b.png
# Palette from hud.css: --red #E10600, panel black, privacy-page navy #0b0f17. No crests, no Instagram/Meta marks.
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

S, OUT = 4096, Path(__file__).parent          # draw 4x, downscale = smooth edges
RED, DARK, NAVY, WHITE, GOLD = (225, 6, 0), (10, 10, 10), (11, 15, 23), (244, 245, 247), (245, 181, 46)

def save(img, name):
    img.resize((1024, 1024), Image.LANCZOS).convert('RGB').save(OUT / name)

def glow(base, box, color, r):
    g = Image.new('RGBA', base.size, (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse(box, fill=color + (150,))
    base.alpha_composite(g.filter(ImageFilter.GaussianBlur(r)))

def globe(base, cx, cy, R, w):
    """Red Earth disc with a dark lat/long grid, clipped to the disc."""
    g = Image.new('RGBA', base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=RED)
    for k in (-2, -1, 0, 1, 2): d.line((cx - R, cy + k * R / 3, cx + R, cy + k * R / 3), fill=DARK, width=w)
    for f in (0.35, 0.72): d.ellipse((cx - R * f, cy - R, cx + R * f, cy + R), outline=DARK, width=w)
    d.line((cx, cy - R, cx, cy + R), fill=DARK, width=w)
    m = Image.new('L', base.size, 0); ImageDraw.Draw(m).ellipse((cx - R, cy - R, cx + R, cy + R), fill=255)
    g.putalpha(m); base.alpha_composite(g)

# A: the Earth inside a stadium ring (bowl seen at an angle, like a planet ring)
a = Image.new('RGBA', (S, S), NAVY + (255,)); da = ImageDraw.Draw(a)
cx, cy, R = S / 2, S / 2, 1050
glow(a, (cx - R * 1.4, cy - R * 1.4, cx + R * 1.4, cy + R * 1.4), RED, 260)
ring = Image.new('RGBA', (S, S), (0, 0, 0, 0)); dr = ImageDraw.Draw(ring)
rw, rh = 1780, 620
dr.ellipse((cx - rw, cy - rh, cx + rw, cy + rh), outline=WHITE, width=200)            # bowl
dr.ellipse((cx - rw + 260, cy - rh + 110, cx + rw - 260, cy + rh - 110), outline=RED, width=70)  # inner tier
for i in range(48):                                                                   # seat rows: dark ticks across the bowl
    t = 2 * math.pi * i / 48; x, y = cx + rw * math.cos(t), cy + rh * math.sin(t)
    dr.line((x - 0.06 * rw * math.cos(t), y - 0.16 * rh * math.sin(t), x + 0.06 * rw * math.cos(t), y + 0.16 * rh * math.sin(t)), fill=NAVY, width=34)
back = ring.crop((0, 0, S, int(cy))); front = ring.crop((0, int(cy), S, S))
a.alpha_composite(back, (0, 0)); da = ImageDraw.Draw(a)
globe(a, cx, cy, R, 70)
a.alpha_composite(front, (0, int(cy)))
for sx, sy, sr in ((640, 700, 40), (3380, 820, 30), (3500, 3300, 44), (560, 3200, 28), (2900, 420, 24)):
    ImageDraw.Draw(a).ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill=GOLD)
save(a, 'app-icon-1024-a.png')

# B: stadium from above, the Earth as the centre circle
b = Image.new('RGBA', (S, S), DARK + (255,)); db = ImageDraw.Draw(b)
cx, cy = S / 2, S / 2
ow, oh = 1820, 1500
for i, c in enumerate((RED, DARK, RED, DARK, RED)):                                   # seat tiers
    k = i * 150; db.rounded_rectangle((cx - ow + k, cy - oh + k, cx + ow - k, cy + oh - k), radius=1300 - k * 0.8, fill=c)
pw, ph = 1050, 760                                                                     # pitch
db.rectangle((cx - pw, cy - ph, cx + pw, cy + ph), fill=NAVY, outline=WHITE, width=56)
db.line((cx, cy - ph, cx, cy + ph), fill=WHITE, width=56)
for sgn in (-1, 1):                                                                    # boxes
    x0 = cx + sgn * pw; x1 = x0 - sgn * 300
    db.rectangle((min(x0, x1), cy - 380, max(x0, x1), cy + 380), outline=WHITE, width=56)
db.ellipse((cx - 470, cy - 470, cx + 470, cy + 470), fill=WHITE)
globe(b, cx, cy, 410, 46)
save(b, 'app-icon-1024-b.png')
