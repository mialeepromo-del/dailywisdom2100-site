#!/usr/bin/env python3
"""Generate a daily Sudoku (unique solution) and render two cute, print-friendly
square PNGs: page 1 = puzzle, page 2 = answer key. All text in English.
High resolution (default 2400px) so it prints crisply and still fits Instagram.
Also saves a JSON archive.
Usage: python3 daily_sudoku.py [--date YYYY-MM-DD] [--size 2400]
Prints the two PNG paths on the last lines.
"""
import argparse, json, math, os, random
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont

SIZE = 2400
K = SIZE / 1080  # scale factor vs the 1080 layout space

def sc(v):
    return int(round(v * K))

BG = (255, 255, 255)
INK = (30, 30, 30)
GRAY_LINE = (205, 205, 205)
SUB = (120, 120, 120)
ANSWER_BLUE = (37, 99, 235)

# pastel palette for decorations
PASTEL_YELLOW = (255, 224, 138)
PASTEL_PINK = (249, 198, 211)
PASTEL_BLUE = (191, 217, 255)
PASTEL_MINT = (191, 232, 201)
PASTEL_LAVENDER = (217, 201, 242)
CAT_BODY = (246, 184, 140)
CAT_DARK = (138, 90, 43)
BUNNY_BODY = (185, 198, 255)
BUNNY_DARK = (70, 80, 140)
BLUSH = (244, 155, 180)
CLOUD = (220, 235, 255)

WEEKDAY_EN = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MONTH_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
            'August', 'September', 'October', 'November', 'December']

REGULAR_TTC = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD_TTC = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
# Fallback fonts for environments without Noto CJK (e.g. GitHub Actions runners).
# Design text is English-only, so DejaVu renders it fine.
FALLBACK_TTF = {
    True: '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    False: '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
}

def load_font(path, size, bold):
    size = sc(size)
    for p in (path, FALLBACK_TTF[bold]):
        cands = []
        for i in range(12):
            try:
                f = ImageFont.truetype(p, size, index=i)
            except Exception:
                continue
            name = ' '.join(f.getname())
            if 'Noto' in p or 'CJK' in p:
                if 'KR' not in name:
                    continue
                if ('Bold' in name) != bold:
                    continue
            cands.append(('Mono' in name, f))
        if cands:
            cands.sort(key=lambda x: x[0])
            return cands[0][1]
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

# ---------- puzzle generation ----------
def solve_count(grid, limit=2):
    best = None
    for i in range(81):
        if grid[i] == 0:
            r, c = divmod(i, 9)
            used = set()
            for k in range(9):
                used.add(grid[r*9+k]); used.add(grid[k*9+c])
            br, bc = 3*(r//3), 3*(c//3)
            for dr in range(3):
                for dc in range(3):
                    used.add(grid[(br+dr)*9+bc+dc])
            cands = [n for n in range(1, 10) if n not in used]
            if not cands:
                return 0
            if best is None or len(cands) < len(best[1]):
                best = (i, cands)
                if len(cands) == 1:
                    break
    if best is None:
        return 1
    i, cands = best
    total = 0
    for n in cands:
        grid[i] = n
        total += solve_count(grid, limit - total)
        grid[i] = 0
        if total >= limit:
            break
    return total

def fill(grid):
    for i in range(81):
        if grid[i] == 0:
            r, c = divmod(i, 9)
            used = set()
            for k in range(9):
                used.add(grid[r*9+k]); used.add(grid[k*9+c])
            br, bc = 3*(r//3), 3*(c//3)
            for dr in range(3):
                for dc in range(3):
                    used.add(grid[(br+dr)*9+bc+dc])
            nums = [n for n in range(1, 10) if n not in used]
            random.shuffle(nums)
            for n in nums:
                grid[i] = n
                if fill(grid):
                    return True
            grid[i] = 0
            return False
    return True

def generate(target_givens=32):
    full = [0]*81
    fill(full)
    solution = full[:]
    puzzle = full[:]
    cells = list(range(81))
    random.shuffle(cells)
    givens = 81
    for i in cells:
        if givens <= target_givens:
            break
        bak = puzzle[i]
        puzzle[i] = 0
        if solve_count(puzzle[:]) != 1:
            puzzle[i] = bak
        else:
            givens -= 1
    return puzzle, solution

def difficulty(givens):
    if givens >= 36: return ('EASY', PASTEL_MINT)
    if givens >= 30: return ('MEDIUM', PASTEL_YELLOW)
    return ('HARD', PASTEL_PINK)

# ---------- cute decorations ----------
def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for k in range(10):
        r = r_out if k % 2 == 0 else r_in
        a = math.radians(rot + k*36)
        pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
    return pts

def draw_star(d, cx, cy, r, color):
    d.polygon(star_points(cx, cy, r, r*0.45), fill=color)

def draw_heart(d, cx, cy, s, color):
    d.ellipse([cx-s, cy-s*0.55, cx, cy+s*0.45], fill=color)
    d.ellipse([cx, cy-s*0.55, cx+s, cy+s*0.45], fill=color)
    d.polygon([(cx-s*0.92, cy), (cx+s*0.92, cy), (cx, cy+s*0.85)], fill=color)

def draw_cloud(d, x, y, s):
    d.ellipse([x, y+s*0.35, x+s*0.45, y+s*0.8], fill=CLOUD)
    d.ellipse([x+s*0.28, y, x+s*0.72, y+s*0.55], fill=CLOUD)
    d.ellipse([x+s*0.58, y+s*0.35, x+s, y+s*0.8], fill=CLOUD)
    d.rectangle([x+s*0.12, y+s*0.5, x+s*0.88, y+s*0.8], fill=CLOUD)

def draw_cat(d, x, y, s):
    d.polygon([(x+s*0.10, y+s*0.30), (x+s*0.16, y-s*0.10), (x+s*0.40, y+s*0.20)], fill=CAT_BODY)
    d.polygon([(x+s*0.90, y+s*0.30), (x+s*0.84, y-s*0.10), (x+s*0.60, y+s*0.20)], fill=CAT_BODY)
    d.polygon([(x+s*0.17, y+s*0.24), (x+s*0.20, y+s*0.02), (x+s*0.33, y+s*0.18)], fill=BLUSH)
    d.polygon([(x+s*0.83, y+s*0.24), (x+s*0.80, y+s*0.02), (x+s*0.67, y+s*0.18)], fill=BLUSH)
    d.ellipse([x, y, x+s, y+s], fill=CAT_BODY)
    d.arc([x+s*0.20, y+s*0.36, x+s*0.38, y+s*0.54], start=0, end=180, fill=CAT_DARK, width=sc(5))
    d.arc([x+s*0.62, y+s*0.36, x+s*0.80, y+s*0.54], start=0, end=180, fill=CAT_DARK, width=sc(5))
    d.arc([x+s*0.40, y+s*0.58, x+s*0.50, y+s*0.68], start=0, end=180, fill=CAT_DARK, width=sc(4))
    d.arc([x+s*0.50, y+s*0.58, x+s*0.60, y+s*0.68], start=0, end=180, fill=CAT_DARK, width=sc(4))
    d.ellipse([x+s*0.12, y+s*0.55, x+s*0.26, y+s*0.65], fill=BLUSH)
    d.ellipse([x+s*0.74, y+s*0.55, x+s*0.88, y+s*0.65], fill=BLUSH)
    for t in (0.52, 0.60, 0.68):
        d.line([x-s*0.14, y+s*t, x+s*0.10, y+s*(t+0.03)], fill=CAT_DARK, width=sc(3))
        d.line([x+s*0.90, y+s*(t+0.03), x+s*1.14, y+s*t], fill=CAT_DARK, width=sc(3))

def draw_bunny(d, x, y, s):
    d.ellipse([x+s*0.12, y-s*0.28, x+s*0.34, y+s*0.30], fill=BUNNY_BODY)
    d.ellipse([x+s*0.66, y-s*0.28, x+s*0.88, y+s*0.30], fill=BUNNY_BODY)
    d.ellipse([x+s*0.18, y-s*0.14, x+s*0.28, y+s*0.20], fill=BLUSH)
    d.ellipse([x+s*0.72, y-s*0.14, x+s*0.82, y+s*0.20], fill=BLUSH)
    d.ellipse([x, y+s*0.10, x+s, y+s*1.10], fill=BUNNY_BODY)
    d.ellipse([x+s*0.30, y+s*0.48, x+s*0.38, y+s*0.56], fill=BUNNY_DARK)
    d.ellipse([x+s*0.62, y+s*0.48, x+s*0.70, y+s*0.56], fill=BUNNY_DARK)
    d.arc([x+s*0.42, y+s*0.62, x+s*0.50, y+s*0.70], start=0, end=180, fill=BUNNY_DARK, width=sc(4))
    d.arc([x+s*0.50, y+s*0.62, x+s*0.58, y+s*0.70], start=0, end=180, fill=BUNNY_DARK, width=sc(4))
    d.ellipse([x+s*0.14, y+s*0.60, x+s*0.28, y+s*0.70], fill=BLUSH)
    d.ellipse([x+s*0.72, y+s*0.60, x+s*0.86, y+s*0.70], fill=BLUSH)

def decorate(d):
    draw_cat(d, sc(34), sc(40), sc(108))
    draw_bunny(d, sc(936), sc(52), sc(100))
    draw_star(d, sc(218), sc(108), sc(20), PASTEL_YELLOW)
    draw_star(d, sc(862), sc(112), sc(16), PASTEL_PINK)
    draw_heart(d, sc(72), sc(220), sc(46), PASTEL_PINK)
    draw_cloud(d, sc(886), sc(208), sc(84))
    draw_star(d, sc(78), sc(1002), sc(16), PASTEL_BLUE)
    draw_heart(d, sc(1002), sc(1000), sc(40), PASTEL_PINK)
    draw_star(d, sc(962), sc(962), sc(15), PASTEL_YELLOW)

# ---------- rendering ----------
def center_text(d, cx, y, text, font, fill):
    bbox = d.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    d.text((cx - w/2, y), text, font=font, fill=fill)

def render_page(puzzle, solution, date_line, kind):
    img = Image.new('RGB', (SIZE, SIZE), BG)
    d = ImageDraw.Draw(img)
    decorate(d)

    f_title = load_font(BOLD_TTC, 62, True)
    f_sub = load_font(REGULAR_TTC, 32, False)
    f_badge = load_font(BOLD_TTC, 26, True)
    f_num = load_font(BOLD_TTC, 54, True)
    f_ans = load_font(REGULAR_TTC, 54, False)
    f_foot = load_font(REGULAR_TTC, 30, False)

    givens = sum(1 for p in puzzle if p)
    label, pill_color = difficulty(givens)

    center_text(d, SIZE/2, sc(58), "Today's Sudoku", f_title, INK)

    sub = date_line if kind == 'puzzle' else date_line + '  ·  Answer Key'
    sb = d.textbbox((0, 0), sub, font=f_sub)
    sub_w = sb[2] - sb[0]
    pb = d.textbbox((0, 0), label, font=f_badge)
    pill_tw = pb[2] - pb[0]
    pill_w, pill_h, gap = pill_tw + sc(44), sc(46), sc(18)
    row_w = sub_w + gap + pill_w
    x0 = (SIZE - row_w)/2
    d.text((x0, sc(142)), sub, font=f_sub, fill=SUB)
    px0 = x0 + sub_w + gap
    py0 = sc(138)
    d.rounded_rectangle([px0, py0, px0+pill_w, py0+pill_h], radius=sc(23), fill=pill_color)
    center_text(d, px0+pill_w/2, py0+sc(9), label, f_badge, INK)

    gs = sc(780)
    gx, gy = (SIZE-gs)/2, sc(235)
    cell = gs/9
    d.rectangle([gx, gy, gx+gs, gy+gs], fill=BG)
    for i in range(81):
        r, c = divmod(i, 9)
        x = gx + c*cell + cell/2
        y = gy + r*cell + cell/2
        if puzzle[i]:
            f, col, txt = f_num, INK, str(puzzle[i])
        elif kind == 'solution':
            f, col, txt = f_ans, ANSWER_BLUE, str(solution[i])
        else:
            continue
        bbox = d.textbbox((0, 0), txt, font=f)
        w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
        d.text((x-w/2-bbox[0], y-h/2-bbox[1]), txt, font=f, fill=col)
    for k in range(10):
        w = sc(8) if k in (0, 9) else (sc(4) if k % 3 == 0 else sc(2))
        col = INK if k % 3 == 0 else GRAY_LINE
        x = gx + k*cell
        d.line([x, gy, x, gy+gs], fill=col, width=w)
        y = gy + k*cell
        d.line([gx, y, gx+gs, y], fill=col, width=w)

    if kind == 'puzzle':
        center_text(d, SIZE/2, sc(1028), 'Answer on the next page', f_foot, SUB)
    else:
        center_text(d, SIZE/2, sc(1028), 'See you tomorrow morning!', f_foot, SUB)
    return img

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--date', default=None)
    ap.add_argument('--size', type=int, default=2400)
    ap.add_argument('--seed', type=int, default=None)
    ap.add_argument('--outdir', default=None)
    args = ap.parse_args()
    global SIZE, K
    SIZE = args.size
    K = SIZE / 1080

    tz = ZoneInfo('America/Los_Angeles')
    today = args.date or datetime.now(tz).strftime('%Y-%m-%d')
    dt = datetime.strptime(today, '%Y-%m-%d')
    date_line = f'{WEEKDAY_EN[dt.weekday()]}, {MONTH_EN[dt.month-1]} {dt.day}, {dt.year}'

    seed = args.seed if args.seed is not None else int.from_bytes(os.urandom(8), 'big')
    random.seed(seed)
    puzzle, solution = generate(32)

    outdir = os.path.expanduser(args.outdir or '~/workspace/sudoku/daily')
    os.makedirs(outdir, exist_ok=True)
    p_path = os.path.join(outdir, f'{today}_puzzle.png')
    s_path = os.path.join(outdir, f'{today}_solution.png')
    j_path = os.path.join(outdir, f'{today}.json')

    render_page(puzzle, solution, date_line, 'puzzle').save(p_path)
    render_page(puzzle, solution, date_line, 'solution').save(s_path)
    with open(j_path, 'w') as f:
        json.dump({'date': today, 'seed': seed, 'puzzle': puzzle, 'solution': solution}, f)

    print('PUZZLE:' + p_path)
    print('SOLUTION:' + s_path)
    print('JSON:' + j_path)

if __name__ == '__main__':
    main()
