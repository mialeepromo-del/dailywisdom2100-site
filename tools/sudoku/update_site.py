#!/usr/bin/env python3
"""Update the Daily Wisdom Deals repo with today's Sudoku.

Reads puzzle/solution from <workdir>/<date>.json (written by daily_sudoku.py)
and <workdir>/<date>_{puzzle,solution}.{png,svg}, then:
  - copies SVGs -> images/sudoku_<date>_{puzzle,solution}.svg
  - copies PNGs  -> images/daily/<date>_{puzzle,solution}.png (Instagram promo)
  - writes sudoku-daily.json (the single puzzle sudoku.html loads)
  - updates the Sudoku deal entry in script.js (image paths + dates)

Usage: python3 update_site.py --date YYYY-MM-DD --workdir DIR [--repo DIR]
"""
import argparse, json, os, re, shutil
from datetime import datetime, timedelta

WEEKDAY_EN = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
MONTH_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
            'August', 'September', 'October', 'November', 'December']

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--date', required=True)
    ap.add_argument('--workdir', required=True)
    ap.add_argument('--repo', default='.')
    args = ap.parse_args()
    today = args.date
    workdir = args.workdir
    repo = args.repo

    dt = datetime.strptime(today, '%Y-%m-%d')
    tmr = dt + timedelta(days=1)
    date_line = f'{WEEKDAY_EN[dt.weekday()]}, {MONTH_EN[dt.month-1]} {dt.day}, {dt.year}'
    expires_line = f'{MONTH_EN[tmr.month-1]} {tmr.day}, {tmr.year}'
    tomorrow = tmr.strftime('%Y-%m-%d')

    daily = json.load(open(os.path.join(workdir, f'{today}.json'), encoding='utf-8'))
    puzzle, solution = daily['puzzle'], daily['solution']
    givens = sum(1 for x in puzzle if x)
    difficulty = 'EASY' if givens >= 36 else ('MEDIUM' if givens >= 30 else 'HARD')

    # 1. copy SVGs + PNGs into the repo
    os.makedirs(os.path.join(repo, 'images', 'daily'), exist_ok=True)
    for kind in ('puzzle', 'solution'):
        shutil.copy(os.path.join(workdir, f'{today}_{kind}.svg'),
                    os.path.join(repo, 'images', f'sudoku_{today}_{kind}.svg'))
        shutil.copy(os.path.join(workdir, f'{today}_{kind}.png'),
                    os.path.join(repo, 'images', 'daily', f'{today}_{kind}.png'))

    # 2. sudoku-daily.json for the site game
    site_json = {
        'date': today,
        'displayDate': date_line,
        'difficulty': difficulty,
        'puzzle': puzzle,
        'solution': solution,
    }
    with open(os.path.join(repo, 'sudoku-daily.json'), 'w', encoding='utf-8') as f:
        json.dump(site_json, f)

    # 3. update the Sudoku deal entry in script.js
    js_path = os.path.join(repo, 'script.js')
    js = open(js_path, encoding='utf-8').read()
    m = re.search(r"    \{\n  title: \"Today's Sudoku.*?\n\}, \n", js, re.S)
    if not m:
        print('FATAL: Sudoku deal entry not found in script.js')
        return 1
    entry = m.group(0)
    entry = re.sub(r'images/sudoku_\d{4}-\d{2}-\d{2}_puzzle\.svg',
                   f'images/sudoku_{today}_puzzle.svg', entry)
    entry = re.sub(r'images/sudoku_\d{4}-\d{2}-\d{2}_solution\.svg',
                   f'images/sudoku_{today}_solution.svg', entry)
    entry = re.sub(r'expires: "[^"]*"', f'expires: "{expires_line}"', entry)
    entry = re.sub(r'expiryDate: "\d{4}-\d{2}-\d{2}"', f'expiryDate: "{tomorrow}"', entry)
    entry = re.sub(r'posted: "[^"]*"',
                   f'posted: "{MONTH_EN[dt.month-1][:3]} {dt.day}, {dt.year}"', entry)
    entry = re.sub(r'postingDate: "\d{4}-\d{2}-\d{2}"', f'postingDate: "{today}"', entry)
    js = js[:m.start()] + entry + js[m.end():]
    open(js_path, 'w', encoding='utf-8').write(js)

    print(f'DONE date={today} givens={givens}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
