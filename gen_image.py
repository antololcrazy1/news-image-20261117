#!/usr/bin/env python3
"""Render the 17 November 2026 world-news summary image (1024x1024 PNG).

All content is hard-coded from the day's reporting (BBC, CNN, Al Jazeera, AFP,
Dawn, France 24, 17 Nov 2026). No network, no randomness: the output is fully
deterministic. Run: python3 gen_image.py  ->  entry.png (next to this file).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (18, 38, 74)
NAVY2 = (28, 56, 104)
RED = (176, 30, 36)
GOLD = (201, 162, 39)
GREY = (90, 88, 82)
CARD = (255, 255, 255)
LINE = (200, 194, 178)

FD = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FD + name, size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning list of lines fitting max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines

def para(draw, x, y, text, fnt, max_w, fill=INK, leading=None, align="left"):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        if align == "center":
            lx = x + (max_w - draw.textlength(ln, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), ln, font=fnt, fill=fill)
        y += lh
    return y

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 128], fill=NAVY)
d.rectangle([0, 128, W, 134], fill=GOLD)
d.text((32, 18), "THE WORLD IN ONE DAY", font=F_SERIF_B(58), fill=(250, 248, 240))
d.text((32, 88), "TUESDAY  17  NOVEMBER  2026", font=F_SANS_B(26), fill=GOLD)
d.text((W - 32, 88), "WORLD NEWS  •  ONE IMAGE", font=F_SANS_B(20), fill=(190, 200, 220), anchor="ra")

# ---------------------------------------------------------------- hero: Kerch Bridge
HX, HY, HW, HH = 32, 152, 600, 280
d.rectangle([HX, HY, HX + HW, HY + HH], fill=(214, 228, 238))
# sky
d.rectangle([HX, HY, HX + HW, HY + 130], fill=(168, 196, 220))
# sun + clouds
d.ellipse([HX + 470, HY + 22, HX + 520, HY + 72], fill=(244, 214, 130))
for cx, cy, r in [(110, 60, 26), (150, 52, 32), (190, 62, 24), (420, 44, 22), (455, 38, 28)]:
    d.ellipse([HX + cx - r, HY + cy - r, HX + cx + r, HY + cy + r], fill=(235, 240, 244))
# sea
d.rectangle([HX, HY + 130, HX + HW, HY + HH], fill=(52, 96, 140))
for wy in (165, 205, 248):
    for wx in range(20, HW - 20, 90):
        d.arc([HX + wx, HY + wy, HX + wx + 56, HY + wy + 18], 0, 180, fill=(140, 180, 210), width=4)
# smoke plume over the break
for sx, sy, r, c in [(300, 108, 34, (120, 120, 118)), (330, 84, 42, (105, 105, 103)),
                     (366, 102, 30, (130, 130, 128)), (352, 64, 24, (96, 96, 94))]:
    d.ellipse([HX + sx - r, HY + sy - r, HX + sx + r, HY + sy + r], fill=c)
# bridge: deck left + right, collapsed middle span dipping into the sea
d.rectangle([HX, HY + 130, HX + 258, HY + 146], fill=(70, 70, 74))
d.rectangle([HX + 342, HY + 130, HX + HW, HY + 146], fill=(70, 70, 74))
# pylons
for px in (90, 200, 400, 510):
    d.rectangle([HX + px, HY + 76, HX + px + 12, HY + 130], fill=(88, 88, 92))
    d.polygon([(HX + px - 4, HY + 76), (HX + px + 16, HY + 76), (HX + px + 6, HY + 58)], fill=(88, 88, 92))
# suspension cables
for x0, x1 in [(90, 200), (400, 510)]:
    d.line([HX + x0 + 6, HY + 64, HX + (x0 + x1) // 2 + 6, HY + 128], fill=(120, 120, 124), width=3)
    d.line([HX + (x0 + x1) // 2 + 6, HY + 128, HX + x1 + 6, HY + 64], fill=(120, 120, 124), width=3)
# collapsed span: broken deck pieces sinking
d.polygon([(HX + 258, HY + 130), (HX + 300, HY + 130), (HX + 296, HY + 194), (HX + 268, HY + 206)],
          fill=(70, 70, 74))
d.polygon([(HX + 342, HY + 130), (HX + 300, HY + 130), (HX + 306, HY + 198), (HX + 330, HY + 204)],
          fill=(70, 70, 74))
d.ellipse([HX + 288, HY + 194, HX + 322, HY + 212], fill=(140, 180, 210))
# explosion starburst at the break
cx, cy = HX + 300, HY + 112
for ang in range(0, 360, 30):
    import math
    x2 = cx + 26 * math.cos(math.radians(ang))
    y2 = cy + 26 * math.sin(math.radians(ang))
    d.line([cx, cy, x2, y2], fill=(255, 176, 32), width=5)
d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 196, 66))
# hero caption bar
d.rectangle([HX, HY + HH - 34, HX + HW, HY + HH], fill=(18, 38, 74))
d.text((HX + 12, HY + HH - 28), "KERCH STRAIT  •  THE BRIDGE TO CRIMEA, AFTER THE STRIKE",
       font=F_SANS_B(15), fill=(255, 255, 255))

# hero text, right of image
TX = HX + HW + 24
TW = W - 32 - TX
d.text((TX, HY + 2), "TOP STORY", font=F_SANS_B(20), fill=RED)
y = para(d, TX, HY + 30, "Ukraine hits Kerch Bridge — span falls into the sea",
         F_SERIF_B(28), TW, leading=34)
y = para(d, TX, y + 8,
         "Zelenskyy hails an “unprecedented” attack, the second day running. "
         "Russia says it downed a record 1,441 drones.",
         F_SANS(19), TW, leading=25, fill=(40, 40, 40))
d.rectangle([TX, HY + HH - 44, TX + TW, HY + HH - 40], fill=GOLD)
d.text((TX, HY + HH - 32), "UKRAINE  •  WAR IN EUROPE", font=F_SANS_B(16), fill=GREY)

# ---------------------------------------------------------------- story cards
def card(x, y, w, h, kicker, kcolor, headline, body, icon):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD, outline=LINE, width=2)
    d.rounded_rectangle([x, y, x + w, y + 34], radius=10, fill=kcolor)
    d.rectangle([x, y + 20, x + w, y + 34], fill=kcolor)
    d.text((x + 12, y + 7), kicker, font=F_SANS_B(15), fill=(255, 255, 255))
    icon(x + w - 46, y + 44)
    ty = para(d, x + 14, y + 44, headline, F_SERIF_B(21), w - 66, leading=25)
    para(d, x + 14, ty + 4, body, F_SANS(16), w - 28, leading=21, fill=(50, 50, 50))

def icon_ship(x, y):
    d.polygon([(x, y + 22), (x + 34, y + 22), (x + 28, y + 34), (x + 6, y + 34)], fill=(52, 96, 140))
    d.rectangle([x + 10, y + 6, x + 14, y + 22], fill=(70, 70, 74))
    d.rectangle([x + 14, y + 10, x + 26, y + 22], fill=(176, 30, 36))
    d.ellipse([x + 28, y + 2, x + 40, y + 14], fill=(255, 176, 32))

def icon_plane(x, y):
    d.polygon([(x + 4, y + 16), (x + 36, y + 16), (x + 40, y + 20), (x + 4, y + 20)], fill=NAVY2)
    d.polygon([(x + 16, y + 4), (x + 22, y + 4), (x + 24, y + 16), (x + 14, y + 16)], fill=NAVY2)
    d.polygon([(x + 16, y + 20), (x + 22, y + 20), (x + 20, y + 32), (x + 14, y + 32)], fill=NAVY2)

def icon_megaphone(x, y):
    d.polygon([(x + 4, y + 12), (x + 28, y + 4), (x + 28, y + 28), (x + 4, y + 20)], fill=RED)
    d.rectangle([x + 2, y + 14, x + 8, y + 26], fill=(70, 70, 74))
    d.arc([x + 28, y + 8, x + 40, y + 24], -60, 60, fill=RED, width=3)

def icon_cross(x, y):
    d.rectangle([x + 4, y + 4, x + 36, y + 36], outline=RED, width=3)
    d.rectangle([x + 17, y + 9, x + 23, y + 31], fill=RED)
    d.rectangle([x + 9, y + 17, x + 31, y + 23], fill=RED)

def icon_gavel(x, y):
    d.rectangle([x + 6, y + 6, x + 30, y + 14], fill=(90, 60, 30))
    d.rectangle([x + 16, y + 14, x + 22, y + 30], fill=(90, 60, 30))
    d.rectangle([x + 8, y + 30, x + 32, y + 36], fill=(120, 84, 44))

def icon_virus(x, y):
    d.ellipse([x + 8, y + 8, x + 32, y + 32], fill=(110, 60, 130))
    for ang in range(0, 360, 45):
        import math
        x1 = x + 20 + 13 * math.cos(math.radians(ang))
        y1 = y + 20 + 13 * math.sin(math.radians(ang))
        x2 = x + 20 + 19 * math.cos(math.radians(ang))
        y2 = y + 20 + 19 * math.sin(math.radians(ang))
        d.line([x1, y1, x2, y2], fill=(110, 60, 130), width=3)

CY = 448
CH = 228
CW = 310
GX = [32, 356, 680]
card(GX[0], CY, CW, CH, "MIDDLE EAST  •  US–IRAN", RED,
     "Fourth tanker hit by a mine in the Strait of Hormuz",
     "Iran says the ship struck a naval mine in 24 hours of attacks. The US confirms a strike on an IRGC launch site on Qeshm Island.",
     icon_ship)
card(GX[1], CY, CW, CH, "ASIA  •  TRUMP ABROAD", NAVY2,
     "Trump lands in Manila for Quad summit",
     "On an Asia tour before talks with Xi and Putin in Shenzhen. A new US chip-export rule follows the Nvidia spy scandal.",
     icon_plane)
card(GX[2], CY, CW, CH, "FRANCE  •  STRIKE", (150, 90, 20),
     "France hit by second nationwide strike in a month",
     "146,000 march across the country as unions demand higher wages and action on the cost of living.",
     icon_megaphone)
card(GX[0], CY + CH + 14, CW, CH, "GAZA  •  AID", (30, 120, 80),
     "West to Israel: open Gaza crossings for aid now",
     "UK, Australia, Canada and Italy call the situation “catastrophic”. Strikes kill three in a Gaza tent camp.",
     icon_cross)
card(GX[1], CY + CH + 14, CW, CH, "FRANCE  •  COURT", (70, 70, 74),
     "Depardieu drops appeal and admits sex-assault charge",
     "The French film star withdraws his challenge before a Paris court, ending years of denial.",
     icon_gavel)
card(GX[2], CY + CH + 14, CW, CH, "USA  •  HEALTH", (110, 60, 130),
     "US loses measles-free status after 26 years",
     "More than 5,400 cases and 10 deaths — the worst outbreak since the early 1990s.",
     icon_virus)

# ---------------------------------------------------------------- bottom briefs strip
BY = CY + 2 * CH + 14 + 16
d.rectangle([0, BY, W, BY + 66], fill=NAVY)
d.text((32, BY + 6), "ALSO ON 17 NOVEMBER", font=F_SANS_B(16), fill=GOLD)
briefs = ("Russian An-12 crashes in Kemerovo, all 19 killed  •  "
          "Japan scrambles jets as Russian planes enter its airspace  •  "
          "Houthis advance in Yemen  •  COP31 draft: $120bn climate finance  •  "
          "Nvidia bumper earnings  •  Pope Leo struck by a rosary in Lima")
para(d, 32, BY + 28, briefs, F_SANS(15), W - 64, leading=19, fill=(225, 228, 235))

# ---------------------------------------------------------------- footer
FY = BY + 66
d.text((32, FY + 6), "Sources: BBC, CNN, Al Jazeera, AFP, Dawn, France 24 — reporting of 17 November 2026.",
       font=F_SANS(14), fill=GREY)
d.text((W - 32, FY + 6), "17 NOV 2026", font=F_SANS_B(14), fill=GREY, anchor="ra")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
