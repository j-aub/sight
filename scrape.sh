#!/usr/bin/env sh
set -eux

# perform scrape
uv run scrape.py

# commit changes
git add output
git commit -m 'Update data'
git push
