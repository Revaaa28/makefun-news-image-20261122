#!/usr/bin/env python3
"""Draw the news-image-20261122 entry: a one-day broadsheet for Sunday 22 November 2026.

Built in-session for make.fun news-image-20261122. Follows the winning
broadsheet pattern of the previous editions (cream broadsheet, full-date
masthead, stat strip, 3 hero stories with flat illustrations, brief cards,
numbered world map + index, DATE CHECK box) with all stories verified
against reporting dated Sunday 22 November 2026 (or overnight into it).

Run: python3 draw.py [out.png]  -> writes a 1024x1024 PNG.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---------- palette ----------
CREAM   = (246, 239, 221)   # page
PAPER   = (250, 245, 232)   # card paper
INK     = (26, 26, 26)
MUTED   = (90, 84, 72)
RULE    = (60, 55, 45)
RED     = (168, 30, 26)     # hero header / date check
REDBG   = (178, 34, 30)
DARK    = (32, 40, 56)      # night sky
GOLD    = (198, 122, 26)
BLUE    = (31, 78, 121)
TEAL    = (14, 124, 123)
GREEN   = (46, 125, 50)
PURPLE  = (106, 61, 154)
PINK    = (194, 24, 91)
BROWN   = (141, 110, 0)
MAPLAND = (232, 220, 192)
MAPLINE = (180, 168, 140)

REGION_COLORS = [
    ("Middle East", 11, RED),
    ("Europe",       8, BLUE),
    ("South Asia",   7, GOLD),
    ("Africa",       2, GREEN),
    ("North America", 3, PURPLE),
    ("East Asia",    2, TEAL),
    ("Oceania",      1, BROWN),
    ("South America", 1, PINK),
]

# ---------- fonts ----------
FDIR = "/usr/share/fonts/truetype"
SERIF      = f"{FDIR}/liberation/LiberationSerif-Regular.ttf"
SERIF_B    = f"{FDIR}/liberation/LiberationSerif-Bold.ttf"
SERIF_I    = f"{FDIR}/liberation/LiberationSerif-Italic.ttf"
SANS       = f"{FDIR}/dejavu/DejaVuSans.ttf"
SANS_B     = f"{FDIR}/dejavu/DejaVuSans-Bold.ttf"
SANS_OB    = f"{FDIR}/dejavu/DejaVuSans-BoldOblique.ttf" if False else SANS_B

def font(path, size):
    return ImageFont.truetype(path, size)

# ---------- text helpers ----------
def wrap_text(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def centered(draw, text, cx, y, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)

# ---------- data ----------
DECK = ("Iran hits US bases in Bahrain overnight  ·  COP31 runs into a second "
        "Sunday with no deal  ·  Nepal's PM lands in Delhi")

STATS = [
    ("14",   "Day of COP31, no deal yet"),
    ("4",    "Iran attacks on Bahrain in 9 days"),
    ("2",    "US bases hit in Bahrain (IRGC)"),
    ("0",    "injuries in the Bahrain fire"),
    ("$2bn", "Nepal's reconstruction ask"),
    ("2",    "days of Shah's state visit"),
]

HEROES = [
    {
        "kicker": "GULF: IRAN HITS BAHRAIN AGAIN",
        "headline": "Missiles and drones hit two US bases overnight",
        "body": ("Iran's Revolutionary Guards say they struck US positions at "
                 "al-Riffa and Awali and destroyed two Patriot radars. Bahrain "
                 "says a civilian industrial site was hit and set on fire; no "
                 "injuries were reported. US Central Command says the drones "
                 "were intercepted."),
        "tag": "IRGC · Fars · Bahrain MOI · CENTCOM",
        "scene": "gulf",
    },
    {
        "kicker": "COP31: NO DEAL — DAY 14",
        "headline": "Climate talks drag into a second Sunday with no deal",
        "body": ("Negotiators in Antalya are still deadlocked over a draft that "
                 "strips out every mention of fossil fuels. The EU and Panama "
                 "are making a last-ditch effort to restore the reference, and "
                 "a $120bn adaptation-finance target has been dropped."),
        "tag": "Reuters · Health Policy Watch · BBC",
        "scene": "cop",
    },
    {
        "kicker": "NEPAL: SHAH IN DELHI",
        "headline": "PM Balendra Shah begins a two-day state visit to India",
        "body": ("Nepal's prime minister arrives in Delhi for a two-day state "
                 "visit, his first as PM, with a US$2bn reconstruction "
                 "assistance request and new air-entry routes on the agenda."),
        "tag": "ICN Nepal",
        "scene": "nepal",
    },
]

BRIEFS = [
    ("PENTAGON — US–CANADA CURB",
     "Hegseth limits US–Canada military ties",
     "A Pentagon memo tells US troops to curb informal gatherings with "
     "Canadian counterparts.",
     "Reported Sun 00:10 UTC"),
    ("LEBANON — UN RESOLUTION",
     "France and US draft a post-UNIFIL resolution",
     "Paris and Washington are drafting a UN resolution for the vacuum "
     "left as UNIFIL winds down.",
     "Reported Sun 00:02 UTC"),
    ("NIGERIA — BOAT SINKS",
     "24 dead as a boat capsizes on the way to a funeral",
     "A boat carrying mourners capsized in Nigeria, killing 24 people, "
     "Arab News reports.",
     "Arab News"),
    ("SOUTH AFRICA — ANC RACE",
     "ANC hunts coalition partners before 27 Nov deadline",
     "After its worst result since 1994 (31%), the ANC scrambles for "
     "power-sharing deals in most cities.",
     "BBC"),
    ("BAHRAIN — INTERCEPTOR CRASH",
     "Bahrain probes a Patriot interceptor crash",
     "IRNA says a US interceptor from the Fifth Fleet base crashed on "
     "Sitra Island and set it ablaze.",
     "IRNA · ToI"),
    ("STRAIT — QESHM BLASTS",
     "Iran: Qeshm blasts were US munitions disposal",
     "Tehran says the Qeshm Island blasts were US munitions disposal, "
     "not a fresh attack.",
     "ToI"),
    ("INDIA — AKVAN RAIN",
     "Cyclone Akvan's rain lingers into Sunday",
     "The storm's remnants bring more rain to Bengal on Sunday, after "
     "20 flights were axed at Ranchi.",
     "IMD"),
    ("WELLINGTON — TEST, DAY 4",
     "India resume 486/4, 118 ahead, on day four",
     "KL Rahul's 136 and Gill's 98 put India in charge at the Basin Reserve; "
     "play resumes on Sunday.",
     "Cricinfo"),
    ("KOREA — EXAM BOUNTY",
     "Seoul repeats a $75,000 bounty for exam-cheating tips",
     "South Korea again offers $75,000 for reports of cheating in its "
     "college entrance exams.",
     "Reported Sun"),
    ("BAHRAIN — UN DEMAND",
     "Bahrain asks the UN to act on Iran's attacks",
     "Manama demands UN action and damages over the Iranian attacks on "
     "its soil.",
     "Reported Sun 01:05 UTC"),
]

INDEX = [
    "Las Vegas GP under lights, 04:00 UTC",
    "France: 6th weekend of protests, turnout lower",
    "Israel: ex-PM backs Eisenkot, snubs Netanyahu",
    "India: cricketer Chahal joins BJP",
    "Blair: UK rejoin EU only if it innovates",
    "Zelensky: China summit 'very unsuccessful'",
    "Brazil: town clears rubble after deadly storm",
    "West Bank: man shot dead by settler guards",
    "EU budget: chair proposes cuts, digital tax",
    "Basra: power-plant fire kills 4, injures 35",
    "US–China military talks end in Shanghai",
    "Russia names reporter Panov 'foreign agent'",
    "Lieberman: toppling Netanyahu is the goal",
    "Trump: chief of staff 'could run for president'",
    "COP31: AI pledge draws no big US tech firms",
    "IFFI adds animation section, five films",
    "Snooker: Advani, Ramachandran win openers",
    "US backs 'strong, united' Kurdistan",
    "IDF strikes south Lebanese areas",
    "Trump: Putin 'wants peace'; Moscow balks",
    "Chennai book fair set for 16–18 January",
    "ICMR: 100 tech transfers, 20 licences",
]

DATE_CHECK = (
    "DATE CHECK — Left out: not Sunday's news.  "
    "Peru quake M6.7, Junín (Sat 21 Nov, 00:09 UTC) · Houthi missiles over Saudi (Sat) · "
    "Sparta II drone strike, Baltic (Sat) · Trump: 'permanent' Iran deal (Sat, Fox) · "
    "Riemann proof verified (Sat) · Bolsonaro to ICU (Sat) · 'El Chapo Isidro' captured, "
    "11 killed (Fri–Sat) · Australia beat England, T20 (Sat) · Rahul 136, Wellington (Sat) · "
    "Nitish Setu opened (Sat) · Russia's 400-drone barrage (Fri 20 Nov) · Estonia border "
    "decision (Fri 20 Nov) · Gupta sentenced, 235 months (Fri 20 Nov) · Japan–India "
    "live-fire deal (Thu 19 Nov) · FBI al-Qaeda airline warning (Thu 19 Nov)"
)

FOOTER = ("Every story here happened, or was first reported, on Sunday 22 November 2026. "
          "Officials' counts and claims are attributed.  Sources: Reuters · AP · AFP · BBC · "
          "Fars · IRNA · Bahrain MOI · US CENTCOM · ABC · NDTV · India Today · Cricinfo · IMD.")

# map dots: index number -> (x, y) in the map box (spread out; no Levant cluster)
MAP_DOTS = {
    1: (28, 52), 2: (182, 40), 4: (282, 64), 5: (176, 30),
    6: (212, 36), 7: (122, 152), 11: (308, 58),
    12: (232, 26), 14: (52, 42), 15: (206, 50), 16: (272, 78),
    21: (278, 84),
}

CONTINENTS = [
    # North America
    [(8, 28), (40, 14), (75, 12), (105, 22), (118, 38), (112, 58), (95, 72),
     (88, 92), (70, 88), (58, 70), (35, 62), (18, 48), (6, 38)],
    # South America
    [(98, 102), (125, 98), (142, 112), (138, 140), (122, 172), (110, 178),
     (102, 150), (96, 122)],
    # Europe
    [(168, 30), (185, 18), (205, 16), (218, 26), (214, 42), (200, 50),
     (185, 52), (172, 44)],
    # Africa
    [(172, 62), (200, 56), (225, 62), (238, 80), (232, 105), (218, 135),
     (205, 142), (192, 120), (180, 95), (170, 75)],
    # Asia
    [(220, 18), (260, 10), (305, 14), (322, 30), (318, 55), (300, 72),
     (285, 82), (262, 78), (245, 62), (228, 48), (220, 32)],
    # Australia
    [(282, 142), (318, 138), (326, 152), (312, 168), (288, 164), (280, 152)],
]

# ---------- scenes ----------
def scene_gulf(d, x, y, w, h):
    # night sky, sea, base, missile arcs, fire glow
    d.rectangle([x, y, x + w, y + h], fill=DARK)
    # stars
    for sx, sy in [(18, 12), (52, 8), (90, 16), (140, 10), (180, 14), (230, 8),
                   (270, 18), (300, 10), (36, 26), (160, 26), (250, 26)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(240, 240, 220))
    # moon
    d.ellipse([x + w - 52, y + 8, x + w - 22, y + 38], fill=(240, 230, 190))
    d.ellipse([x + w - 46, y + 6, x + w - 20, y + 32], fill=DARK)
    # sea
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(24, 52, 84))
    d.line([x + 8, y + h - 18, x + 60, y + h - 18], fill=(90, 130, 180), width=2)
    d.line([x + 200, y + h - 14, x + 290, y + h - 14], fill=(90, 130, 180), width=2)
    # base buildings
    bx, by = x + 22, y + h - 58
    d.rectangle([bx, by, bx + 46, y + h - 26], fill=(52, 58, 74))
    d.rectangle([bx + 56, by + 10, bx + 96, y + h - 26], fill=(44, 50, 64))
    for wx in range(bx + 6, bx + 44, 12):
        d.rectangle([wx, by + 8, wx + 6, by + 14], fill=(255, 214, 130))
    # radar dish
    d.line([bx + 76, by + 10, bx + 76, by - 6], fill=(200, 200, 200), width=3)
    d.arc([bx + 66, by - 16, bx + 86, by + 4], 200, 340, fill=(220, 220, 220), width=3)
    # fire glow + smoke
    d.ellipse([x + 150, y + h - 66, x + 210, y + h - 20], fill=(255, 122, 26))
    d.ellipse([x + 162, y + h - 56, x + 198, y + h - 26], fill=(255, 190, 60))
    d.ellipse([x + 168, y + h - 78, x + 192, y + h - 58], fill=(120, 120, 120))
    d.ellipse([x + 176, y + h - 92, x + 196, y + h - 74], fill=(150, 150, 150))
    # missile arcs (white dotted trails with orange heads)
    d.arc([x + 120, y - 30, x + 260, y + 60], 200, 300, fill=(255, 255, 255), width=2)
    d.ellipse([x + 236, y + 22, x + 244, y + 30], fill=(255, 140, 40))
    d.arc([x + 40, y - 40, x + 170, y + 40], 220, 310, fill=(255, 255, 255), width=2)
    d.ellipse([x + 148, y + 8, x + 156, y + 16], fill=(255, 140, 40))
    # ground line
    d.line([x, y + h - 26, x + w, y + h - 26], fill=(16, 20, 30), width=2)

def scene_cop(d, x, y, w, h):
    # pale sky, globe, thermometer, clock, flags row
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    # sun
    d.ellipse([x + w - 58, y + 8, x + w - 28, y + 38], fill=(240, 190, 60))
    # globe
    cx, cy, r = x + 62, y + 52, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 180))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 60, 90), width=2)
    for poly in [[(cx - 30, cy - 18), (cx - 8, cy - 26), (cx + 6, cy - 12), (cx - 12, cy - 2), (cx - 32, cy - 4)],
                 [(cx + 10, cy + 8), (cx + 30, cy + 2), (cx + 34, cy + 18), (cx + 14, cy + 26), (cx + 4, cy + 16)],
                 [(cx - 26, cy + 14), (cx - 10, cy + 22), (cx - 22, cy + 34), (cx - 34, cy + 26)]]:
        d.polygon(poly, fill=(90, 160, 90))
    d.arc([cx - r, cy - r, cx + r, cy + r], 0, 360, fill=(30, 60, 90), width=2)
    # thermometer
    tx = x + 138
    d.rounded_rectangle([tx, y + 12, tx + 16, y + 78], radius=8, fill=(255, 255, 255),
                        outline=(120, 40, 30), width=2)
    d.ellipse([tx - 4, y + 72, tx + 20, y + 92], fill=(200, 40, 30))
    d.rectangle([tx + 5, y + 34, tx + 11, y + 80], fill=(200, 40, 30))
    d.text((tx + 24, y + 16), "+1.8°C", font=font(SANS_B, 13), fill=(120, 40, 30))
    d.text((tx + 24, y + 34), "October", font=font(SANS, 11), fill=INK)
    # clock (overtime)
    kx, ky, kr = x + 240, y + 42, 30
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 255, 255),
              outline=(30, 30, 30), width=2)
    d.line([kx, ky, kx, ky - 20], fill=INK, width=2)
    d.line([kx, ky, kx + 15, ky + 8], fill=INK, width=2)
    d.text((kx - 26, ky + 32), "OVERTIME", font=font(SANS_B, 11), fill=RED)
    # ground
    d.rectangle([x, y + h - 6, x + w, y + h], fill=(150, 170, 150))

def scene_nepal(d, x, y, w, h):
    # sky, Himalayas, India Gate arch, two flags
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 240))
    # sun
    d.ellipse([x + 20, y + 10, x + 46, y + 36], fill=(240, 190, 60))
    # mountains
    d.polygon([(x + 10, y + h - 30), (x + 70, y + 18), (x + 130, y + h - 30)], fill=(120, 140, 170))
    d.polygon([(x + 58, y + 30), (x + 70, y + 18), (x + 84, y + 32), (x + 70, y + 40)], fill=(255, 255, 255))
    d.polygon([(x + 110, y + h - 30), (x + 175, y + 30), (x + 240, y + h - 30)], fill=(96, 120, 155))
    d.polygon([(x + 164, y + 40), (x + 175, y + 30), (x + 188, y + 42), (x + 175, y + 48)], fill=(255, 255, 255))
    d.polygon([(x + 215, y + h - 30), (x + 265, y + 44), (x + 315, y + h - 30)], fill=(120, 140, 170))
    # ground
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(120, 150, 110))
    # India Gate style arch (right side)
    ax, ay = x + w - 92, y + h - 30
    d.rectangle([ax, ay - 52, ax + 56, ay], fill=(190, 150, 90))
    d.pieslice([ax + 8, ay - 66, ax + 48, ay - 6], 180, 360, fill=(222, 232, 240))
    d.rectangle([ax + 20, ay - 34, ax + 36, ay], fill=(222, 232, 240))
    # flags: Nepal double-pennant + India tricolour
    # Nepal flag (crimson double pennant)
    nx, ny = x + 18, y + h - 78
    d.polygon([(nx, ny), (nx + 26, ny + 8), (nx, ny + 14)], fill=(220, 20, 60))
    d.polygon([(nx, ny + 14), (nx + 22, ny + 20), (nx, ny + 26)], fill=(220, 20, 60))
    d.line([nx, ny - 4, nx, ny + 30], fill=INK, width=2)
    # India flag
    ix, iy = x + 56, y + h - 74
    d.line([ix, iy - 4, ix, iy + 30], fill=INK, width=2)
    d.rectangle([ix, iy, ix + 30, iy + 8], fill=(255, 153, 51))
    d.rectangle([ix, iy + 8, ix + 30, iy + 16], fill=(255, 255, 255))
    d.rectangle([ix, iy + 16, ix + 30, iy + 24], fill=(19, 136, 8))
    d.ellipse([ix + 11, iy + 8, ix + 19, iy + 16], outline=(0, 0, 128), width=1)

SCENES = {"gulf": scene_gulf, "cop": scene_cop, "nepal": scene_nepal}

# ---------- build ----------
def build(out_path):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    MX = 12  # side margin

    # top rule + kicker
    d.line([MX, 6, W - MX, 6], fill=RULE, width=2)
    f_kick = font(SANS_B, 13)
    d.text((MX, 12), "THE WORLD IN ONE DAY", font=f_kick, fill=INK)
    kick_r = "35 STORIES  ·  8 REGIONS  ·  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    wkr = d.textlength(kick_r, font=f_kick)
    d.text((W - MX - wkr, 12), kick_r, font=f_kick, fill=INK)
    d.line([MX, 32, W - MX, 32], fill=RULE, width=2)

    # masthead
    f_mast = font(SERIF_B, 60)
    centered(d, "Sunday 22 November 2026", W // 2, 38, f_mast, INK)
    f_deck = font(SERIF_I, 17)
    centered(d, DECK, W // 2, 104, f_deck, INK)
    d.line([MX, 128, W - MX, 128], fill=RULE, width=2)

    # stat strip
    f_num = font(SERIF_B, 30)
    f_lab = font(SANS, 10)
    sx, sy, sw = MX, 134, (W - 2 * MX) // 6
    for i, (num, lab) in enumerate(STATS):
        cx = sx + i * sw
        if i:
            d.line([cx, sy + 2, cx, sy + 44], fill=MAPLINE, width=1)
        nw = d.textlength(num, font=f_num)
        d.text((cx + (sw - nw) / 2, sy), num, font=f_num, fill=RED)
        for j, ll in enumerate(lab.split("\n")):
            lw = d.textlength(ll, font=f_lab)
            d.text((cx + (sw - lw) / 2, sy + 32 + j * 12), ll, font=f_lab, fill=MUTED)
    d.line([MX, 182, W - MX, 182], fill=RULE, width=1)

    # region bar with labels inside the segments
    bx, by, bw, bh = MX, 188, W - 2 * MX, 12
    total = sum(c for _, c, _ in REGION_COLORS)
    f_leg = font(SANS, 8)
    x = bx
    short = {"Middle East": "Middle East", "Europe": "Europe", "South Asia": "South Asia",
             "Africa": "Africa", "North America": "N. America", "East Asia": "E. Asia",
             "Oceania": "Oceania", "South America": "S. America"}
    for name, count, col in REGION_COLORS:
        seg = bw * count / total
        d.rectangle([x, by, x + seg - 1, by + bh], fill=col)
        lab = f"{short[name]} {count}"
        if d.textlength(lab, font=f_leg) <= seg - 4:
            d.text((x + 3, by + 2), lab, font=f_leg, fill=(255, 255, 255))
        elif seg > 16:
            t = str(count)
            d.text((x + (seg - d.textlength(t, font=f_leg)) / 2, by + 2), t,
                   font=f_leg, fill=(255, 255, 255))
        x += seg

    # heroes
    hy, hh = 222, 250
    hw = (W - 2 * MX - 2 * 10) // 3
    f_hkick = font(SANS_B, 13)
    f_hhead = font(SERIF_B, 18)
    f_hbody = font(SANS, 11)
    f_htag = font(SANS_B, 9)
    for i, hero in enumerate(HEROES):
        hx = MX + i * (hw + 10)
        # header band
        d.rectangle([hx, hy, hx + hw, hy + 26], fill=REDBG)
        kw = d.textlength(hero["kicker"], font=f_hkick)
        d.text((hx + (hw - kw) / 2, hy + 5), hero["kicker"], font=f_hkick, fill=(255, 255, 255))
        # scene
        SCENES[hero["scene"]](d, hx, hy + 26, hw, 92)
        # headline
        hlines = wrap_text(d, hero["headline"], f_hhead, hw - 8)
        yy = draw_lines(d, hlines, hx + 4, hy + 124, f_hhead, INK, 20)
        # body
        blines = wrap_text(d, hero["body"], f_hbody, hw - 8)
        yy = draw_lines(d, blines, hx + 4, yy + 4, f_hbody, INK, 14)
        # source tag
        d.text((hx + 4, hy + hh - 16), hero["tag"], font=f_htag, fill=MUTED)
        # divider between heroes
        if i:
            d.line([hx - 5, hy, hx - 5, hy + hh], fill=MAPLINE, width=1)

    # briefs: 2 rows x 5
    by0 = 482
    brow_h = 116
    bgap = 8
    bw5 = (W - 2 * MX - 4 * bgap) // 5
    f_bkick = font(SANS_B, 10)
    f_bhead = font(SANS_B, 12)
    f_bbody = font(SANS, 11)
    f_btag = font(SANS, 9)
    for r in range(2):
        for c in range(5):
            idx = r * 5 + c
            kicker, headline, body, tag = BRIEFS[idx]
            bx0 = MX + c * (bw5 + bgap)
            byy = by0 + r * (brow_h + bgap)
            d.rectangle([bx0, byy, bx0 + bw5, byy + brow_h], fill=PAPER)
            d.rectangle([bx0, byy, bx0 + bw5, byy + 17], fill=RED)
            kw = d.textlength(kicker, font=f_bkick)
            if kw > bw5 - 6:
                # shrink to fit
                f2 = font(SANS_B, 9)
                kw = d.textlength(kicker, font=f2)
                d.text((bx0 + (bw5 - kw) / 2, byy + 3), kicker, font=f2, fill=(255, 255, 255))
            else:
                d.text((bx0 + (bw5 - kw) / 2, byy + 2), kicker, font=f_bkick, fill=(255, 255, 255))
            hl = wrap_text(d, headline, f_bhead, bw5 - 10)
            yy = draw_lines(d, hl, bx0 + 5, byy + 21, f_bhead, INK, 14)
            bl = wrap_text(d, body, f_bbody, bw5 - 10)
            yy = draw_lines(d, bl, bx0 + 5, yy + 2, f_bbody, INK, 13)
            d.text((bx0 + 5, byy + brow_h - 13), tag, font=f_btag, fill=MUTED)

    # section header: map + index
    sy0 = 730
    f_sec = font(SANS_B, 13)
    d.text((MX, sy0), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    idx_title = "ALSO ON SUNDAY 22 NOVEMBER 2026 — 22 MORE STORIES"
    iw = d.textlength(idx_title, font=f_sec)
    d.text((W - MX - iw, sy0), idx_title, font=f_sec, fill=INK)
    d.line([MX, sy0 + 18, W - MX, sy0 + 18], fill=RULE, width=2)

    # map (left) + index (right, 2 cols)
    map_x, map_y, map_w, map_h = MX, sy0 + 26, 330, 176
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(238, 230, 208))
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], outline=MAPLINE, width=1)
    for poly in CONTINENTS:
        pts = [(map_x + px, map_y + py) for px, py in poly]
        d.polygon(pts, fill=MAPLAND, outline=MAPLINE)
    f_dot = font(SANS_B, 8)
    for num, (dx, dy) in MAP_DOTS.items():
        cx, cy = map_x + dx, map_y + dy
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255), width=1)
        t = str(num)
        tw = d.textlength(t, font=f_dot)
        d.text((cx - tw / 2, cy - 5), t, font=f_dot, fill=(255, 255, 255))
    # index columns
    ix0 = map_x + map_w + 16
    icol_w = (W - MX - ix0 - 12) // 2
    f_idx = font(SANS, 10)
    for col in range(2):
        for row in range(11):
            n = col * 11 + row
            txt = f"{n + 1}. {INDEX[n]}"
            # shrink if needed
            f = f_idx
            if d.textlength(txt, font=f) > icol_w:
                f = font(SANS, 9)
            d.text((ix0 + col * (icol_w + 12), map_y + 4 + row * 16), txt, font=f, fill=INK)
    # DATE CHECK box
    dy0 = 938
    d.rectangle([MX, dy0, W - MX, dy0 + 52], fill=(255, 244, 238), outline=RED, width=2)
    f_dc = font(SANS, 10)
    dclines = wrap_text(d, DATE_CHECK, f_dc, W - 2 * MX - 16)
    draw_lines(d, dclines, MX + 8, dy0 + 5, f_dc, INK, 13)

    # footer
    f_ft = font(SANS, 9)
    flines = wrap_text(d, FOOTER, f_ft, W - 2 * MX)
    draw_lines(d, flines, MX, dy0 + 58, f_ft, MUTED, 12)

    img.save(out_path, "PNG", optimize=True)
    return out_path

if __name__ == "__main__":
    import sys, os
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(out)
    print(out, os.path.getsize(out), "bytes")
