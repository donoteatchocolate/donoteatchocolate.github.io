#!/usr/bin/env python3
"""
Scan the Swipe/games directory for .html files and write Swipe/games/index.json.
Run this after adding/removing game HTML files.
"""
import os
import json

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
games_dir = os.path.join(repo_root, 'Swipe', 'games')
output_file = os.path.join(games_dir, 'index.json')

if not os.path.isdir(games_dir):
    print('Games directory not found:', games_dir)
    raise SystemExit(1)

entries = []
for fname in sorted(os.listdir(games_dir)):
    # skip index file
    if fname in ('index.json', 'index.html'):
        continue
    fpath = os.path.join(games_dir, fname)
    if os.path.isdir(fpath):
        continue
    is_html = False
    if fname.lower().endswith('.html'):
        is_html = True
    else:
        # try to detect HTML by reading the start of the file
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as fh:
                head = fh.read(512).lower()
                if '<!doctype html' in head or '<html' in head:
                    is_html = True
        except Exception:
            is_html = False
    if not is_html:
        continue
    path = os.path.join('Swipe', 'games', fname).replace('\\', '/')
    title = os.path.splitext(fname)[0].replace('_', ' ').replace('-', ' ').title()
    entries.append({
        'name': fname,
        'title': title,
        'src': path,
        'meta': ''
    })

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(entries, f, indent=2)

print(f'Wrote {len(entries)} entries to {output_file}')
