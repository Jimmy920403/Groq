## 1. Implementation
- [ ] 1.1 Document recommended local validation commands in `openspec/project.md`.
- [ ] 1.2 Add CI workflow `.github/workflows/openspec-validate.yml` to run `openspec validate --strict` on PRs.
- [ ] 1.3 Add a small README snippet in `openspec/changes/add-validate-proposals/` if helpful for reviewers.
- [ ] 1.4 Run validation on this change and fix any issues.

## 2. Verification
- [ ] 2.1 Create a test PR that modifies `openspec/changes` and ensure CI blocks when validation fails.
- [ ] 2.2 Confirm valid proposals pass CI and status is reported on the PR.
