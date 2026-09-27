# Security Policy

This policy covers **(a)** secrets (passwords, tokens, keys) and **(b)** personal or
confidential research data that reach this repository or its history by mistake,
and **(c)** vulnerabilities in the project's code or configuration.

What may be stored where is defined in [DATA_SECURITY.md](DATA_SECURITY.md).

## 1. Reporting

| Channel | Use |
| --- | --- |
| **[SECURITY_CONTACT_EMAIL]** | Primary channel for any incident |
| [PROJECT_LEAD] / [DATA_MANAGER] | Direct message if e-mail is not possible |
| GitHub → *Security* → *Report a vulnerability* | Private vulnerability reporting (if enabled) |

**Never open a public Issue or PR describing the leaked content.** Do not paste the
secret or the personal data into chat, e-mail or issues — describe only *where* it is
(file path, commit SHA, PR number).

## 2. Incident response procedure

Time targets start from the moment anyone notices the problem.

### Step 1 — Contain (within 1 hour)

1. **Stop.** Do not merge, do not push further commits to the affected branch.
2. Notify the security contact and the Data Manager (see above).
3. If the leak is in an open PR: the Project Lead **closes the PR** (do not merge) and,
   if the repository is public, temporarily makes it private (Settings → General → Danger Zone).
4. **Secrets:** revoke/rotate the credential **immediately** at its provider
   (password, API key, token, SSH key). Assume it is compromised the moment it was pushed —
   removing it from Git does **not** make it safe again.

### Step 2 — Assess (within 24 hours)

The Data Manager and Project Lead record in a *restricted* incident log (in secure storage,
not in this repository):

- what was exposed (categories of data, number of records, secret type);
- where (branch, commit SHA, files) and since when;
- who had access (repository visibility, collaborators, forks, clones, CI logs);
- whether the data identify or could re-identify participants.

### Step 3 — Remove from history (within 72 hours)

Deleting the file in a new commit is **not** enough: it stays in history.

```bash
# Performed ONLY by the Project Lead or Data Manager, after coordination with the team.
pip install git-filter-repo
git clone --mirror https://github.com/[ORG_OR_USER]/[REPO_NAME].git
cd [REPO_NAME].git
git filter-repo --invert-paths --path path/to/leaked_file.csv      # remove a file everywhere
# or replace strings:   git filter-repo --replace-text ../replacements.txt
git push --force --mirror
```

Then:

1. Contact **GitHub Support** to purge cached views of the removed commits and PR refs.
2. Every collaborator **deletes their local clone and re-clones** (old clones still hold the data).
3. Check and delete forks; check CI logs/artifacts and delete affected workflow runs.
4. For LFS files: delete the objects via the repository's LFS settings / GitHub Support.

### Step 4 — Notify (per legal/ethical obligations)

If personal data were exposed, the Project Lead decides — with the institution's data
protection officer [DPO_CONTACT] and ethics committee [ETHICS_COMMITTEE] — whether
notification of the ethics committee, the funder, a regulator or participants is required,
within the deadlines of the applicable law ([APPLICABLE_DATA_PROTECTION_LAW]).

### Step 5 — Learn (within 2 weeks)

Write a short, blameless post-incident note (restricted storage), and implement the
prevention measures (e.g. extra pattern in `tools/check_sensitive.py`, `.gitignore` rule,
training). Record the decision in `00_project_management/decisions/`.

## 3. Preventive controls in this repository

| Control | Where |
| --- | --- |
| `.gitignore` blocks data files, secrets, keys, `.env` | [.gitignore](.gitignore) |
| Pre-commit hooks (secret scan, large files, sensitive names) | [.pre-commit-config.yaml](.pre-commit-config.yaml) |
| CI: sensitive-file + PII-pattern scan, secret scan (Gitleaks), size limit | [.github/workflows/validation.yml](.github/workflows/validation.yml) |
| Protected `main`, required reviews, CODEOWNERS | [tools/setup_github.sh](tools/setup_github.sh), [.github/CODEOWNERS](.github/CODEOWNERS) |
| GitHub secret scanning + push protection | Settings → Code security (enable where the plan allows) |
| Least-privilege roles | [ROLES_AND_PERMISSIONS.md](00_project_management/team/ROLES_AND_PERMISSIONS.md) |
| Two-factor authentication required for all members | Organization settings |

## 4. Credentials

- Credentials are **never** written in code, notebooks, config files or documentation.
- Scripts read them from environment variables loaded from a local `.env` file (git-ignored);
  the template is [config/.env.example](config/.env.example) (names only, no values).
- Shared credentials (e.g. survey-platform API) are stored in [PASSWORD_MANAGER] and
  owned by the Data Manager. CI secrets use GitHub *Actions secrets*, never plain text.

## 5. Supported versions

Only the latest release and `main` receive corrections.
