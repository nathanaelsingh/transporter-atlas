#!/usr/bin/env bash
# Create and deploy a new Transporter Atlas GitHub repository.
# Requires: git, Python 3, GitHub CLI (gh), and an authenticated GitHub account.
set -euo pipefail

cd "$(dirname "$0")"
REPO_NAME="${REPO_NAME:-transporter-atlas}"
VISIBILITY="${VISIBILITY:-public}"
if [[ "$VISIBILITY" != "public" && "$VISIBILITY" != "private" ]]; then
  echo "VISIBILITY must be public or private" >&2
  exit 2
fi
for command in git python3 gh; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "Missing required command: $command. See SETUP_GITHUB.md." >&2
    exit 2
  fi
done
if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub CLI is not logged in. Run: gh auth login" >&2
  exit 2
fi
ACCOUNT="$(gh api user --jq .login)"
FULL="$ACCOUNT/$REPO_NAME"
if gh repo view "$FULL" --json name >/dev/null 2>&1; then
  echo "Repository $FULL already exists. No files were overwritten." >&2
  exit 2
fi

echo "Validating local Transporter Atlas project..."
python3 -m unittest discover -s tests
python3 scripts/build_site.py

if [[ ! -d .git ]]; then
  git init -b main
fi
if [[ -z "$(git config user.name || true)" ]]; then
  git config user.name "$ACCOUNT"
fi
if [[ -z "$(git config user.email || true)" ]]; then
  USER_ID="$(gh api user --jq .id)"
  git config user.email "${USER_ID}+${ACCOUNT}@users.noreply.github.com"
fi

git add -A
if ! git diff --cached --quiet; then
  git commit -m "Initial Transporter Atlas website and literature updater"
fi

echo "Creating GitHub repository: $FULL ($VISIBILITY)"
gh repo create "$FULL" "--$VISIBILITY" --description "Living evidence-based atlas of orphan transporters, ion channels and deorphanization experiments" --source=. --remote=origin --push

# Grant GITHUB_TOKEN the write access needed for weekly publication snapshots.
if ! gh api -X PUT "repos/$FULL/actions/permissions/workflow" \
   -f default_workflow_permissions=write \
   -F can_approve_pull_request_reviews=false >/dev/null 2>&1; then
  echo "NOTICE: Could not configure Actions write access automatically."
  echo "Check Settings > Actions > General > Workflow permissions: Read and write."
fi

# Pages is public-facing; GitHub may restrict Pages on private repositories.
if ! gh api -X POST "repos/$FULL/pages" -f build_type=workflow >/dev/null 2>&1; then
  echo "NOTICE: Could not enable GitHub Pages automatically."
  echo "Open Settings > Pages and select GitHub Actions as the build source."
fi

if ! gh workflow run update-and-deploy.yml --repo "$FULL" --ref main >/dev/null 2>&1; then
  echo "NOTICE: Could not start the first workflow yet."
  echo "Go to Actions > Update literature and deploy atlas > Run workflow."
fi

echo
printf 'Repository: https://github.com/%s\n' "$FULL"
printf 'Expected site after successful Pages deployment: https://%s.github.io/%s/\n' "$ACCOUNT" "$REPO_NAME"
printf 'Workflow: https://github.com/%s/actions\n' "$FULL"
echo "Publishing and the first literature refresh must complete before the site URL is live."
