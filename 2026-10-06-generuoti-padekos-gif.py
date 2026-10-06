# GLAUBIC padėkos GIF: „Ačiū!“ / „Thank you!“ su konfeti prekės ženklo spalvomis.
import sys, math, random
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
S = '/tmp/claude-0/-home-user-glaubic-svetaine-redesign/887ceb9f-3b64-59f9-a0d4-d9f0311a4264/scratchpad/fonts/'
FILES = [S + 'manrope-latin-800-normal.ttf', S + 'manrope-latin-ext-800-normal.ttf']
CMAPS = [TTFont(f).getBestCmap() for f in FILES]
W, H = 1072, 400
VIOLET, INK, CORAL, YELLOW, WHITE, V100 = (154, 162, 230), (50, 40, 56), (255, 106, 61), (255, 237, 0), (255, 255, 255), (236, 238, 251)

def font_for(ch, size):
    for f, cm in zip(FILES, CMAPS):
        if ord(ch) in cm: return ImageFont.truetype(f, size)
    return ImageFont.truetype(FILES[0], size)

def draw_text(d, text, size, cx, cy, fill):
    fonts = [font_for(c, size) for c in text]
    widths = [f.getlength(c) for f, c in zip(fonts, text)]
    x = cx - sum(widths) / 2
    for c, f, w in zip(text, fonts, widths):
        d.text((x, cy), c, font=f, fill=fill, anchor='ls'); x += w

def make(text, sub, out):
    random.seed(7)
    N = 28
    pieces = [dict(x=random.uniform(0, W), y0=random.uniform(-H, H), sp=random.uniform(0.6, 1.4), r=random.uniform(7, 14),
                   col=random.choice([CORAL, YELLOW, WHITE, INK, CORAL, YELLOW]), shape=random.choice(['dot', 'bar']),
                   rot=random.uniform(0, math.pi)) for _ in range(46)]
    frames = []
    for i in range(N):
        im = Image.new('RGB', (W, H), VIOLET); d = ImageDraw.Draw(im)
        t = i / N
        for pc in pieces:
            y = (pc['y0'] + t * H * 2 * pc['sp']) % (H + 60) - 30
            x = pc['x'] + 14 * math.sin(t * 2 * math.pi + pc['rot'] * 3)
            if pc['shape'] == 'dot':
                d.ellipse([x - pc['r'] / 2, y - pc['r'] / 2, x + pc['r'] / 2, y + pc['r'] / 2], fill=pc['col'])
            else:
                a = pc['rot'] + t * 2 * math.pi * pc['sp']; L = pc['r'] * 1.4
                dx, dy = math.cos(a) * L / 2, math.sin(a) * L / 2
                d.line([x - dx, y - dy, x + dx, y + dy], fill=pc['col'], width=6)
        # tekstas: įšoka per pirmus 6 kadrus, paskui švelniai pulsuoja
        k = min(1, i / 6)
        scale = (0.6 + 0.48 * k - 0.08 * max(0, k - 0.85) / 0.15) if i < 7 else 1 + 0.025 * math.sin((i - 7) / (N - 7) * 2 * math.pi)
        size = int(150 * scale)
        draw_text(d, text, size, W / 2, H / 2 + size * 0.28, INK)
        if sub:
            draw_text(d, sub, 38, W / 2, H / 2 + 120, INK)
        frames.append(im.convert('P', palette=Image.ADAPTIVE, colors=32))
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=90, loop=0, optimize=True, disposal=1)

make(sys.argv[1], sys.argv[2], sys.argv[3])
