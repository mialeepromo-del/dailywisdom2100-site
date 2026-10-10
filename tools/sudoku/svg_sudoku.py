#!/usr/bin/env python3
"""Render the daily Sudoku as SVG (vector, text-based) with the same cute design.
Reads puzzle/solution from the daily JSON. Outputs two .svg files.
Usage: python3 svg_sudoku.py [--date YYYY-MM-DD] [--outdir DIR]
"""
import argparse, json, math, os
from datetime import datetime

WEEKDAY_EN = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MONTH_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
            'August', 'September', 'October', 'November', 'December']
FONT = "DM Sans, Arial, Helvetica, sans-serif"

INK = "#1e1e1e"; SUB = "#787878"; BLUE = "#2563eb"
PYELLOW = "#ffe08a"; PPINK = "#f9c6d3"; PBLUE = "#bfd9ff"; PMINT = "#bfe8c9"
CAT = "#f6b88c"; CATD = "#8a5a2b"; BUN = "#b9c6ff"; BUND = "#46508c"
BLUSH = "#f49bb4"; CLOUD = "#dcebff"

def star_points(cx, cy, r):
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.45
        a = math.radians(-90 + k * 36)
        pts.append(f"{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a):.1f}")
    return " ".join(pts)

def decorations():
    s = []
    # cat (top-left), head center ~ (88, 94), size 108
    x, y, sz = 34, 40, 108
    cx, cy = x + sz/2, y + sz/2
    s.append(f'<polygon points="{x+sz*0.10:.0f},{y+sz*0.30:.0f} {x+sz*0.16:.0f},{y-sz*0.10:.0f} {x+sz*0.40:.0f},{y+sz*0.20:.0f}" fill="{CAT}"/>')
    s.append(f'<polygon points="{x+sz*0.90:.0f},{y+sz*0.30:.0f} {x+sz*0.84:.0f},{y-sz*0.10:.0f} {x+sz*0.60:.0f},{y+sz*0.20:.0f}" fill="{CAT}"/>')
    s.append(f'<polygon points="{x+sz*0.17:.0f},{y+sz*0.24:.0f} {x+sz*0.20:.0f},{y+sz*0.02:.0f} {x+sz*0.33:.0f},{y+sz*0.18:.0f}" fill="{BLUSH}"/>')
    s.append(f'<polygon points="{x+sz*0.83:.0f},{y+sz*0.24:.0f} {x+sz*0.80:.0f},{y+sz*0.02:.0f} {x+sz*0.67:.0f},{y+sz*0.18:.0f}" fill="{BLUSH}"/>')
    s.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{sz/2:.0f}" ry="{sz/2:.0f}" fill="{CAT}"/>')
    # happy eyes (U shapes via quadratic curves)
    for ex in (0.20, 0.62):
        x1, x2 = x+sz*ex, x+sz*(ex+0.18); yy = y+sz*0.44
        s.append(f'<path d="M {x1:.0f} {yy:.0f} Q {(x1+x2)/2:.0f} {yy+11:.0f} {x2:.0f} {yy:.0f}" stroke="{CATD}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    # mouth w
    mx = x+sz*0.5; my = y+sz*0.62
    s.append(f'<path d="M {mx-10:.0f} {my:.0f} Q {mx-5:.0f} {my+9:.0f} {mx:.0f} {my:.0f} Q {mx+5:.0f} {my+9:.0f} {mx+10:.0f} {my:.0f}" stroke="{CATD}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    # blush
    s.append(f'<ellipse cx="{x+sz*0.19:.0f}" cy="{y+sz*0.60:.0f}" rx="{sz*0.07:.0f}" ry="{sz*0.05:.0f}" fill="{BLUSH}"/>')
    s.append(f'<ellipse cx="{x+sz*0.81:.0f}" cy="{y+sz*0.60:.0f}" rx="{sz*0.07:.0f}" ry="{sz*0.05:.0f}" fill="{BLUSH}"/>')
    # whiskers
    for t in (0.52, 0.60, 0.68):
        s.append(f'<line x1="{x-sz*0.14:.0f}" y1="{y+sz*t:.0f}" x2="{x+sz*0.10:.0f}" y2="{y+sz*(t+0.03):.0f}" stroke="{CATD}" stroke-width="3" stroke-linecap="round"/>')
        s.append(f'<line x1="{x+sz*0.90:.0f}" y1="{y+sz*(t+0.03):.0f}" x2="{x+sz*1.14:.0f}" y2="{y+sz*t:.0f}" stroke="{CATD}" stroke-width="3" stroke-linecap="round"/>')

    # bunny (top-right), x=936 y=52 s=100
    x, y, sz = 936, 52, 100
    s.append(f'<ellipse cx="{x+sz*0.23:.0f}" cy="{y+sz*0.01:.0f}" rx="{sz*0.11:.0f}" ry="{sz*0.29:.0f}" fill="{BUN}"/>')
    s.append(f'<ellipse cx="{x+sz*0.77:.0f}" cy="{y+sz*0.01:.0f}" rx="{sz*0.11:.0f}" ry="{sz*0.29:.0f}" fill="{BUN}"/>')
    s.append(f'<ellipse cx="{x+sz*0.23:.0f}" cy="{y+sz*0.03:.0f}" rx="{sz*0.05:.0f}" ry="{sz*0.17:.0f}" fill="{BLUSH}"/>')
    s.append(f'<ellipse cx="{x+sz*0.77:.0f}" cy="{y+sz*0.03:.0f}" rx="{sz*0.05:.0f}" ry="{sz*0.17:.0f}" fill="{BLUSH}"/>')
    s.append(f'<ellipse cx="{x+sz/2:.0f}" cy="{y+sz*0.60:.0f}" rx="{sz/2:.0f}" ry="{sz/2:.0f}" fill="{BUN}"/>')
    s.append(f'<circle cx="{x+sz*0.34:.0f}" cy="{y+sz*0.52:.0f}" r="{sz*0.04:.0f}" fill="{BUND}"/>')
    s.append(f'<circle cx="{x+sz*0.66:.0f}" cy="{y+sz*0.52:.0f}" r="{sz*0.04:.0f}" fill="{BUND}"/>')
    mx = x+sz*0.5; my = y+sz*0.66
    s.append(f'<path d="M {mx-8:.0f} {my:.0f} Q {mx-4:.0f} {my+8:.0f} {mx:.0f} {my:.0f} Q {mx+4:.0f} {my+8:.0f} {mx+8:.0f} {my:.0f}" stroke="{BUND}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    s.append(f'<ellipse cx="{x+sz*0.21:.0f}" cy="{y+sz*0.65:.0f}" rx="{sz*0.07:.0f}" ry="{sz*0.05:.0f}" fill="{BLUSH}"/>')
    s.append(f'<ellipse cx="{x+sz*0.79:.0f}" cy="{y+sz*0.65:.0f}" rx="{sz*0.07:.0f}" ry="{sz*0.05:.0f}" fill="{BLUSH}"/>')

    # stars & hearts & cloud
    s.append(f'<polygon points="{star_points(218, 108, 20)}" fill="{PYELLOW}"/>')
    s.append(f'<polygon points="{star_points(862, 112, 16)}" fill="{PPINK}"/>')
    s.append(f'<polygon points="{star_points(78, 1002, 16)}" fill="{PBLUE}"/>')
    s.append(f'<polygon points="{star_points(962, 962, 15)}" fill="{PYELLOW}"/>')
    for hx, hy, hs, col in ((72, 220, 46, PPINK), (1002, 1000, 40, PPINK)):
        s.append(f'<circle cx="{hx-hs/2:.0f}" cy="{hy-hs*0.05:.0f}" r="{hs/2:.0f}" fill="{col}"/>')
        s.append(f'<circle cx="{hx+hs/2:.0f}" cy="{hy-hs*0.05:.0f}" r="{hs/2:.0f}" fill="{col}"/>')
        s.append(f'<polygon points="{hx-hs*0.92:.0f},{hy:.0f} {hx+hs*0.92:.0f},{hy:.0f} {hx:.0f},{hy+hs*0.85:.0f}" fill="{col}"/>')
    # cloud
    x, y, sz = 886, 208, 84
    s.append(f'<g fill="{CLOUD}"><ellipse cx="{x+sz*0.22:.0f}" cy="{y+sz*0.57:.0f}" rx="{sz*0.22:.0f}" ry="{sz*0.22:.0f}"/><ellipse cx="{x+sz*0.50:.0f}" cy="{y+sz*0.27:.0f}" rx="{sz*0.22:.0f}" ry="{sz*0.27:.0f}"/><ellipse cx="{x+sz*0.79:.0f}" cy="{y+sz*0.57:.0f}" rx="{sz*0.21:.0f}" ry="{sz*0.22:.0f}"/><rect x="{x+sz*0.12:.0f}" y="{y+sz*0.50:.0f}" width="{sz*0.76:.0f}" height="{sz*0.30:.0f}"/></g>')
    return "\n".join(s)

def difficulty_label(givens):
    if givens >= 36: return ('EASY', PMINT)
    if givens >= 30: return ('MEDIUM', PYELLOW)
    return ('HARD', PPINK)

def render(puzzle, solution, date_line, kind):
    givens = sum(1 for p in puzzle if p)
    label, pill = difficulty_label(givens)
    sub = date_line if kind == 'puzzle' else date_line + '  ·  Answer Key'

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">',
             '<rect width="1080" height="1080" fill="white"/>',
             decorations(),
             f'<text x="540" y="122" text-anchor="middle" font-family="{FONT}" font-size="62" font-weight="700" fill="{INK}">Today\'s Sudoku</text>']
    # date + pill (approximate centering: date text ~600px wide at 32px font)
    parts.append(f'<text x="380" y="178" text-anchor="middle" font-family="{FONT}" font-size="32" fill="{SUB}">{sub}</text>')
    parts.append(f'<rect x="700" y="138" width="150" height="46" rx="23" fill="{pill}"/>')
    parts.append(f'<text x="775" y="169" text-anchor="middle" font-family="{FONT}" font-size="26" font-weight="700" fill="{INK}">{label}</text>')

    # grid
    gs, gx, gy = 780, 150, 235
    cell = gs / 9
    for i in range(81):
        r, c = divmod(i, 9)
        x = gx + c*cell + cell/2
        yy = gy + r*cell + cell/2
        if puzzle[i]:
            v, col, wt = puzzle[i], INK, 700
        elif kind == 'solution':
            v, col, wt = solution[i], BLUE, 400
        else:
            continue
        parts.append(f'<text x="{x:.1f}" y="{yy:.1f}" text-anchor="middle" dominant-baseline="central" font-family="{FONT}" font-size="54" font-weight="{wt}" fill="{col}">{v}</text>')
    for k in range(10):
        w = 8 if k in (0, 9) else (4 if k % 3 == 0 else 2)
        col = INK if k % 3 == 0 else "#cdcdcd"
        x = gx + k*cell
        parts.append(f'<line x1="{x:.1f}" y1="{gy}" x2="{x:.1f}" y2="{gy+gs}" stroke="{col}" stroke-width="{w}"/>')
        y = gy + k*cell
        parts.append(f'<line x1="{gx}" y1="{y:.1f}" x2="{gx+gs}" y2="{y:.1f}" stroke="{col}" stroke-width="{w}"/>')

    foot = 'Answer on the next page' if kind == 'puzzle' else 'See you tomorrow morning!'
    parts.append(f'<text x="540" y="1058" text-anchor="middle" font-family="{FONT}" font-size="30" fill="{SUB}">{foot}</text>')
    parts.append('</svg>')
    return "\n".join(parts)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--date', default=None)
    ap.add_argument('--outdir', default=None)
    args = ap.parse_args()
    today = args.date or datetime.now().strftime('%Y-%m-%d')
    dt = datetime.strptime(today, '%Y-%m-%d')
    date_line = f'{WEEKDAY_EN[dt.weekday()]}, {MONTH_EN[dt.month-1]} {dt.day}, {dt.year}'

    jpath = os.path.expanduser(f'~/workspace/sudoku/daily/{today}.json')
    d = json.load(open(jpath))
    puzzle, solution = d['puzzle'], d['solution']

    outdir = os.path.expanduser(args.outdir or '~/workspace/sudoku/daily')
    os.makedirs(outdir, exist_ok=True)
    for kind in ('puzzle', 'solution'):
        p = os.path.join(outdir, f'{today}_{kind}.svg')
        open(p, 'w', encoding='utf-8').write(render(puzzle, solution, date_line, kind))
        print(('PUZZLE_SVG:' if kind == 'puzzle' else 'SOLUTION_SVG:') + p)

if __name__ == '__main__':
    main()
