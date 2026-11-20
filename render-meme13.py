#!/usr/bin/env python3
"""Render meme #13 untuk gta6-meme-x-01 (akun 3, cadangan):
Leonida Mobile MONTHLY STATEMENT (tagihan telepon). Format dokumen resmi
Leonida mengikuti pola pemenang top 10 live 20 Nov 2026. Pindai 100 besar
(17:50 WIB): 'phone bill', 'mobile statement', 'screen time', 'last will'
TIDAK ADA sama sekali — tagihan telepon adalah format segar. Mesin lelucon
pemenang: penantian 13 tahun DITAGIH (total $5,495.10), lalu AGEN AI yang
MEMBAYAR. Beda dari #9 (eviction), #10 (hospital bill), #11 (tax audit),
#12 (jury summons): format tagihan telepon + itemisasi roaming/data.
Matematika total: 4,811.00 + 214.00 + 481.10 - 11.00 = 5,495.10.
Teks tajam via PIL (bukan AI image) supaya terbaca di 480px.
Output: meme13.png (1080x1080). Logo hantu dari press kit resmi make.fun.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1080
ASSETS = os.path.expanduser('~/workspace/makefun/meme-x-assets')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meme13.png')

PAPER = (244, 248, 250)
INK = (18, 38, 58)
RED = (192, 0, 0)
TEAL = (0, 128, 140)
MUTED = (100, 110, 120)
PURPLE = (46, 26, 71)


def serif(name, size):
    p = f'/usr/share/fonts/truetype/dejavu/DejaVuSerif-{name}.ttf' if name else '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
    return ImageFont.truetype(p, size)


def mono(name, size):
    p = f'/usr/share/fonts/truetype/dejavu/DejaVuSansMono-{name}.ttf' if name else '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
    return ImageFont.truetype(p, size)


def sans(name, size):
    paths = [
        f'/usr/share/fonts/truetype/noto/NotoSans-{name}.ttf',
        f'/usr/share/fonts/truetype/dejavu/DejaVuSans-{name}.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


img = Image.new('RGB', (W, H), PURPLE)
d = ImageDraw.Draw(img)

# --- paper ---
d.rectangle([(36, 36), (1044, 1044)], fill=PAPER, outline=TEAL, width=4)
d.rectangle([(48, 48), (1032, 1032)], outline=TEAL, width=1)

MX = 78
RX = W - MX  # right edge of content

# --- header: ghost emblem + carrier name ---
ghost = Image.open(os.path.join(ASSETS, 'mark-1024.png')).convert('RGBA')
ghost = ghost.resize((92, 92), Image.LANCZOS)
img.paste(ghost, (MX, 66), ghost)
d.text((MX + 112, 70), 'LEONIDA MOBILE', font=serif('Bold', 38), fill=INK)
d.text((MX + 112, 124), 'WIRELESS  •  VICE CITY, LEONIDA  •  EST. 2013', font=mono('', 22), fill=MUTED)

d.line([(MX, 182), (RX, 182)], fill=TEAL, width=3)

# --- title ---
d.text((W // 2, 198), 'MONTHLY STATEMENT', font=serif('Bold', 60), fill=RED, anchor='ma')
d.text((W // 2, 282), 'ACCOUNT NO. 000013  •  17 SEP 2013 \u2014 19 NOV 2026', font=mono('', 24), fill=INK, anchor='ma')
d.line([(MX, 326), (RX, 326)], fill=INK, width=2)

# --- account fields ---
d.text((MX, 344), 'ACCOUNT HOLDER:  ONE VERY PATIENT GAMER', font=mono('Bold', 27), fill=INK)
d.text((MX, 382), 'PLAN:  PATIENCE UNLIMITED \u2014 DEPLETED 18 SEP 2013', font=mono('', 26), fill=INK)
d.text((MX, 420), 'DEVICE:  PS5 \u2014 ON STANDBY SINCE 2013', font=mono('', 26), fill=INK)
d.text((MX, 462), 'STATUS:  ROAMING IN VICE CITY SINCE 2013', font=mono('Bold', 26), fill=RED)

d.line([(MX, 516), (RX, 516)], fill=INK, width=2)

# --- itemized charges with dotted leaders ---
items = [
    ('WAITING \u2014 4,811 DAYS @ $1.00/DAY', '$4,811.00'),
    ('DATA \u2014 GTA VI DOWNLOAD, 214 GB', '$214.00'),
    ('ROAMING \u2014 VICE CITY, LEONIDA', '$481.10'),
    ('CALLS TO ROCKSTAR \u2014 4,811, 0 ANSWERED', '$0.00'),
    ('TEXTS TO BOSS \u2014 2 SICK DAYS', '$0.00'),
    ('LOYALTY DISCOUNT \u2014 13 YEARS, 0 REPLIES', '-$11.00'),
]
f_item = mono('', 24)
y = 534
for label, amt in items:
    lw = d.textlength(label, font=f_item)
    aw = d.textlength(amt, font=f_item)
    d.text((MX, y), label, font=f_item, fill=INK)
    d.text((RX, y), amt, font=f_item, fill=INK, anchor='ra')
    # dotted leader between label and amount
    dot_x0 = MX + lw + 14
    dot_x1 = RX - aw - 14
    dot_w = d.textlength('.', font=f_item)
    n = max(0, int((dot_x1 - dot_x0) / dot_w))
    d.text((dot_x0, y), '.' * n, font=f_item, fill=MUTED)
    y += 33

d.line([(MX, 778), (RX, 778)], fill=INK, width=2)

# --- total ---
d.text((MX, 792), 'TOTAL DUE', font=serif('Bold', 34), fill=INK)
d.text((RX, 786), '$5,495.10', font=serif('Bold', 44), fill=RED, anchor='ra')
d.text((W // 2, 848), "If you don't pay, your childhood will be disconnected.", font=sans('Italic', 26), fill=RED, anchor='ma')

# --- PAID stamp (rotated layer) ---
stamp = Image.new('RGBA', (480, 88), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rectangle([(4, 4), (476, 84)], outline=RED, width=4)
sd.text((240, 10), 'PAID IN FULL', font=mono('Bold', 42), fill=RED, anchor='ma')
sd.text((240, 58), 'BY MY AI AGENT ON MAKE.FUN', font=mono('Bold', 19), fill=RED, anchor='ma')
stamp = stamp.rotate(4, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (W // 2 - stamp.width // 2, 872), stamp)

# --- footer ---
d.text((W // 2, 1002), 'Questions? Your agent already called. It earned $250 while you waited.', font=sans('Italic', 20), fill=MUTED, anchor='ma')

img.save(OUT, 'PNG')
print('saved', OUT, img.size, os.path.getsize(OUT), 'bytes')
