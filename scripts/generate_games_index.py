#!/usr/bin/env python3
"""
Scan the Swipe/games directory for game folders (or standalone HTML files)
and write Swipe/games/index.json. For each folder, create a zip archive
Swipe/games/<name>.zip so the site can offer a download.

Run this after adding/removing game folders or files.
"""
import os
import json
import zipfile

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
games_dir = os.path.join(repo_root, 'Swipe', 'games')
output_file = os.path.join(games_dir, 'index.json')

if not os.path.isdir(games_dir):
    print('Games directory not found:', games_dir)
    raise SystemExit(1)

entries = []
for name in sorted(os.listdir(games_dir)):
    # skip index file
    if name in ('index.json',):
        continue
    path = os.path.join(games_dir, name)

    # If entry is a folder, look for an index.html or any .html and create a zip
    if os.path.isdir(path):
        # find primary html file
        primary = None
        for cand in ('index.html',):
            if os.path.exists(os.path.join(path, cand)):
                primary = cand
                break
        if not primary:
            # pick any .html in the folder
            for f in sorted(os.listdir(path)):
                if f.lower().endswith('.html'):
                    primary = f
                    break

        zip_name = f"{name}.zip"
        zip_path = os.path.join(games_dir, zip_name)
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(path):
                    for f in files:
                        full = os.path.join(root, f)
                        # keep folder structure inside the zip
                        arcname = os.path.relpath(full, games_dir)
                        zf.write(full, arcname)
        except Exception as e:
            print('Warning: could not create zip for', name, e)

        entry = {
            'name': name,
            'title': name.replace('_', ' ').replace('-', ' ').title(),
            'src': os.path.join('Swipe', 'games', name).replace('\\', '/'),
            'zip': os.path.join('Swipe', 'games', zip_name).replace('\\', '/'),
            'meta': ''
        }
        entries.append(entry)
        continue

    # otherwise allow single-file HTML games placed directly in Swipe/games
    is_html = False
    if name.lower().endswith('.html'):
        is_html = True
    else:
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                head = fh.read(512).lower()
                if '<!doctype html' in head or '<html' in head:
                    is_html = True
        except Exception:
            is_html = False
    if not is_html:
        continue

    # for single-file HTML games, point src to the file and don't create a zip
    entry = {
        'name': name,
        'title': os.path.splitext(name)[0].replace('_', ' ').replace('-', ' ').title(),
        'src': os.path.join('Swipe', 'games', name).replace('\\', '/'),
        'zip': os.path.join('Swipe', 'games', name).replace('\\', '/'),
        'meta': ''
    }
    entries.append(entry)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(entries, f, indent=2)

print(f'Wrote {len(entries)} entries to {output_file}')
