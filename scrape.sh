#!/usr/bin/env sh
set -eux

# perform scrape
uv run scrape.py

# commit changes
# https://stackoverflow.com/questions/69839851/github-actions-copy-git-user-name-and-user-email-from-last-commit
# https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address#about-commit-email-addresses
NAME="${GITHUB_ACTOR:-octocat}"
EMAIL="${GITHUB_ACTOR_ID:-101839405}+${NAME}@users.noreply.github.com"
git config user.name "$NAME"
git config user.email "$EMAIL"
git add output
git commit -m 'Update data'
git push
