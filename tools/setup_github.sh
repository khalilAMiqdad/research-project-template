#!/usr/bin/env bash
# =============================================================================
# setup_github.sh — create and configure the GitHub repository for [PROJECT_NAME]
#
# Requirements: git, git-lfs, GitHub CLI (gh) >= 2.40, python3
#   gh auth login                       # once
#   gh auth refresh -s project,admin:org   # project board (+ org teams if OWNER is an organization)
#
# Usage:
#   1. Edit the CONFIGURATION block below (no passwords or tokens here!).
#   2. From the repository root:  bash tools/setup_github.sh
#   3. Optional dry run:          DRY_RUN=1 bash tools/setup_github.sh
#
# Safe to re-run: labels use --force, protection/settings are PUT/PATCH (idempotent).
# =============================================================================
set -euo pipefail

# ------------------------------- CONFIGURATION -------------------------------
OWNER="YOUR_GITHUB_USER_OR_ORG"          # e.g. the organization's GitHub login
OWNER_IS_ORG="true"                      # "true" for an organization, "false" for a personal account
REPO="research-project-template"         # e.g. <org>-<study>-<year>, lowercase-kebab
VISIBILITY="private"                     # private (recommended) | internal | public
DESCRIPTION="Reproducible, secure and auditable repository for collaborative survey and quantitative research: data pipeline from raw to analysis-ready, reviewed workflow, data-protection guardrails."
PROJECT_TITLE="Research Board"
MAKE_TEMPLATE="false"                    # "true" to mark the repo as a GitHub template repository

# GitHub handles (without @) replacing the CODEOWNERS placeholders.
# With an organization you can use teams instead, e.g. "my-org/data-team".
H_PROJECT_LEAD="PROJECT_LEAD_HANDLE"
H_DATA_MANAGER="DATA_MANAGER_HANDLE"
H_METHODOLOGY_LEAD="METHODOLOGY_LEAD_HANDLE"
H_ANALYSIS_LEAD="ANALYSIS_LEAD_HANDLE"
H_FIELDWORK_COORDINATOR="FIELDWORK_COORDINATOR_HANDLE"
H_REPORT_LEAD="REPORT_LEAD_HANDLE"

# Collaborators to invite: "github_handle:permission"  (permission: pull|triage|push|maintain|admin)
# Leave empty and use ORG_TEAMS below when OWNER is an organization.
COLLABORATORS=(
  # "DATA_MANAGER_HANDLE:maintain"
  # "METHODOLOGY_LEAD_HANDLE:maintain"
  # "ANALYSIS_LEAD_HANDLE:push"
  # "FIELDWORK_COORDINATOR_HANDLE:push"
  # "RESEARCH_ASSISTANT_HANDLE:push"
  # "REVIEWER_HANDLE:push"
)

# Organization teams: "team-slug:permission" (created if missing; add members in the web UI or with
#   gh api -X PUT orgs/$OWNER/teams/<slug>/memberships/<handle> -f role=member )
ORG_TEAMS=(
  "research-leads:admin"
  "data-team:maintain"
  "methodology:maintain"
  "analysis:push"
  "field-team:push"
  "research-assistants:push"
  "reviewers:push"
)
# -----------------------------------------------------------------------------

DRY_RUN="${DRY_RUN:-0}"
run()  { echo "+ $*"; [[ "$DRY_RUN" == "1" ]] || "$@"; }
try()  { echo "+ $*"; [[ "$DRY_RUN" == "1" ]] || "$@" || echo "  ! step failed (non-fatal) — see note above; continue."; }
step() { printf '\n\033[1;34m==> %s\033[0m\n' "$*"; }

cd "$(dirname "$0")/.."
[[ -f README.md && -d .github ]] || { echo "Could not find the repository root."; exit 1; }

step "0. Checking prerequisites"
for bin in git gh python3; do command -v "$bin" >/dev/null || { echo "Missing: $bin"; exit 1; }; done
git lfs version >/dev/null 2>&1 || { echo "Missing: git-lfs (https://git-lfs.com)"; exit 1; }
gh auth status >/dev/null || { echo "Run: gh auth login"; exit 1; }
[[ "$OWNER" != "YOUR_GITHUB_USER_OR_ORG" ]] || { echo "Edit the CONFIGURATION block first."; exit 1; }

step "1. Filling repository placeholders (owner/repo links, CODEOWNERS)"
python3 - "$OWNER" "$REPO" "$H_PROJECT_LEAD" "$H_DATA_MANAGER" "$H_METHODOLOGY_LEAD" \
          "$H_ANALYSIS_LEAD" "$H_FIELDWORK_COORDINATOR" "$H_REPORT_LEAD" "$DRY_RUN" <<'PY'
import pathlib, sys
owner, repo, pl, dm, ml, al, fc, rl, dry = sys.argv[1:]
text_ext = {".md", ".yml", ".yaml", ".cff", ".py", ".sh", ".toml", ""}
changed = 0
for p in pathlib.Path(".").rglob("*"):
    if not p.is_file() or ".git" in p.parts or p.suffix not in text_ext:
        continue
    t = p.read_text(encoding="utf-8", errors="ignore")
    n = t.replace("[ORG_OR_USER]", owner).replace("[REPO_NAME]", repo)
    if p.as_posix() == ".github/CODEOWNERS":
        for k, v in {"@PROJECT_LEAD": pl, "@DATA_MANAGER": dm, "@METHODOLOGY_LEAD": ml,
                     "@ANALYSIS_LEAD": al, "@FIELDWORK_COORDINATOR": fc, "@REPORT_LEAD": rl}.items():
            n = n.replace(k + " ", "@" + v + " ").replace(k + "\n", "@" + v + "\n")
    if n != t:
        changed += 1
        if dry != "1":
            p.write_text(n, encoding="utf-8")
print(f"  {changed} file(s) updated")
PY

step "2. Initialising Git + LFS and creating the first commit"
[[ -d .git ]] || run git init -b main
run git lfs install --local
run git add -A
if ! git rev-parse HEAD >/dev/null 2>&1; then
  run git commit -m "chore: initialise research repository structure (v0.1.0)"
fi

step "3. Creating the GitHub repository ($OWNER/$REPO, $VISIBILITY)"
if gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  echo "  repository exists — pushing"
  git remote get-url origin >/dev/null 2>&1 || run git remote add origin "https://github.com/$OWNER/$REPO.git"
  run git push -u origin main
else
  run gh repo create "$OWNER/$REPO" "--$VISIBILITY" --description "$DESCRIPTION" --source . --remote origin --push
fi

step "4. Repository settings (squash-merge only, auto-delete branches, no wiki)"
run gh repo edit "$OWNER/$REPO" \
  --enable-squash-merge --enable-merge-commit=false --enable-rebase-merge=false \
  --delete-branch-on-merge --enable-wiki=false --enable-issues --enable-projects \
  --add-topic research --add-topic reproducible-research --add-topic survey-methodology
[[ "$MAKE_TEMPLATE" == "true" ]] && run gh repo edit "$OWNER/$REPO" --template

step "5. Labels"
LABELS=(
  "data|1d76db|Anything touching data or data scripts"
  "data-cleaning|5319e7|Cleaning rules / stage 02"
  "methodology|0e8a16|Protocol, sampling, questionnaire, weighting design"
  "analysis|fbca04|Analysis scripts and outputs"
  "statistics|c5def5|Statistical method questions"
  "documentation|0075ca|Documentation only"
  "report|d4c5f9|Report writing"
  "fieldwork|bfd4f2|Field operations"
  "technical|e4e669|Git, CI, environment"
  "urgent|b60205|Must be handled within 48h"
  "review-required|ff9f1c|Waiting for a reviewer"
  "review:methodology|0e8a16|Needs methodology review"
  "review:statistics|fbca04|Needs statistical review"
  "review:data|1d76db|Needs data-manager review"
  "sensitive|000000|Involves sensitive-data handling - never put the data in the issue"
  "blocked|e11d21|Cannot progress - explain why"
  "decision-needed|f9d0c4|Requires a decision by the leads"
  "release|0052cc|Release preparation"
  "no-changelog|eeeeee|PR intentionally without CHANGELOG entry"
  "good-first-task|7057ff|Suitable for new team members"
)
for l in "${LABELS[@]}"; do
  IFS='|' read -r name color desc <<<"$l"
  run gh label create "$name" --repo "$OWNER/$REPO" --color "$color" --description "$desc" --force
done
# Remove GitHub default labels that overlap
for d in bug enhancement "help wanted" invalid question wontfix duplicate "good first issue"; do
  try gh label delete "$d" --repo "$OWNER/$REPO" --yes
done

step "6. Milestones (project phases)"
for m in "M1 Protocol" "M2 Fieldwork" "M3 Data" "M4 Analysis" "M5 Report"; do
  if ! gh api "repos/$OWNER/$REPO/milestones?state=all" --jq '.[].title' 2>/dev/null | grep -qx "$m"; then
    run gh api "repos/$OWNER/$REPO/milestones" -f title="$m" --silent
  fi
done

step "7. Branch protection on main"
echo "  Note: on a personal FREE account, protection of PRIVATE repositories is not available"
echo "  (GitHub Pro/Team/Enterprise needed). Organization on GitHub Team or a public repo works."
try gh api -X PUT "repos/$OWNER/$REPO/branches/main/protection" \
  -H "Accept: application/vnd.github+json" --input - <<'JSON'
{
  "required_status_checks": { "strict": true, "contexts": ["structure-and-security", "docs-check"] },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "require_code_owner_reviews": true,
    "dismiss_stale_reviews": true,
    "require_last_push_approval": true
  },
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_conversation_resolution": true
}
JSON

step "8. Security features (availability depends on plan and visibility)"
try gh api -X PUT "repos/$OWNER/$REPO/vulnerability-alerts" --silent
try gh api -X PATCH "repos/$OWNER/$REPO" --silent \
  -f "security_and_analysis[secret_scanning][status]=enabled" \
  -f "security_and_analysis[secret_scanning_push_protection][status]=enabled"
[[ "$VISIBILITY" == "public" ]] && try gh api -X PUT "repos/$OWNER/$REPO/private-vulnerability-reporting" --silent

step "9. Team access"
if [[ "$OWNER_IS_ORG" == "true" ]]; then
  for t in "${ORG_TEAMS[@]}"; do
    IFS=':' read -r slug perm <<<"$t"
    gh api "orgs/$OWNER/teams/$slug" >/dev/null 2>&1 || try gh api "orgs/$OWNER/teams" -f name="$slug" -f privacy=closed --silent
    try gh api -X PUT "orgs/$OWNER/teams/$slug/repos/$OWNER/$REPO" -f permission="$perm" --silent
  done
fi
for c in "${COLLABORATORS[@]}"; do
  IFS=':' read -r user perm <<<"$c"
  try gh api -X PUT "repos/$OWNER/$REPO/collaborators/$user" -f permission="$perm" --silent
done

step "10. GitHub Project board"
echo "  Needs the 'project' scope: gh auth refresh -s project"
if [[ "$DRY_RUN" != "1" ]]; then
  PNUM=$(gh project list --owner "$OWNER" --format json --jq ".projects[] | select(.title==\"$PROJECT_TITLE\") | .number" 2>/dev/null | head -n1 || true)
  if [[ -z "$PNUM" ]]; then
    PNUM=$(gh project create --owner "$OWNER" --title "$PROJECT_TITLE" --format json --jq '.number' || true)
    if [[ -n "$PNUM" ]]; then
      try gh project field-create "$PNUM" --owner "$OWNER" --name "Research Stage" --data-type SINGLE_SELECT \
        --single-select-options "Backlog,To Do,In Progress,Internal Review,Methodology Review,Statistical Review,Approved,Completed,Archived"
      try gh project field-create "$PNUM" --owner "$OWNER" --name "Work Package" --data-type SINGLE_SELECT \
        --single-select-options "Protocol,Fieldwork,Data,Analysis,Reporting,Management"
      try gh project field-create "$PNUM" --owner "$OWNER" --name "Priority" --data-type SINGLE_SELECT \
        --single-select-options "P1-High,P2-Medium,P3-Low"
      try gh project field-create "$PNUM" --owner "$OWNER" --name "Due date" --data-type DATE
      try gh project field-create "$PNUM" --owner "$OWNER" --name "Effort (days)" --data-type NUMBER
    fi
  fi
  [[ -n "${PNUM:-}" ]] && try gh project link "$PNUM" --owner "$OWNER" --repo "$OWNER/$REPO"
  echo "  Project #${PNUM:-?}. In the web UI: New view → Board → Group by 'Research Stage';"
  echo "  Workflows: enable 'Item added → Backlog', 'PR merged → Completed', 'Auto-archive'."
fi

step "Done"
cat <<EOF
Repository: https://github.com/$OWNER/$REPO
Manual steps remaining (see README "Setup" / the implementation guide):
  • Require 2FA for the organization (Org settings → Authentication security).
  • Check Settings → Branches shows the protection rule (or add a Ruleset if your plan requires it).
  • Tag the first release after filling CHANGELOG date:  git tag -a v0.1.0 -m "v0.1.0" && git push origin v0.1.0
EOF
