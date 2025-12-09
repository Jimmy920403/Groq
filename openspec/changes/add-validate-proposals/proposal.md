## Why
Change proposals sometimes lack machine-checked validation or CI enforcement. This results in proposals that fail validation late in the process or require manual fixes during review. Adding a validation command and CI enforcement will catch formatting and structural issues earlier, reduce review friction, and keep the `openspec` repository healthy.

## What Changes
- Add a lightweight `openspec validate-proposals` helper (or document `openspec validate <change-id> --strict`) as the recommended validation step for authors.
- Add a GitHub Actions workflow that runs `openspec validate` (strict) on new PRs that modify `openspec/changes/**` or `openspec/specs/**`.
- Update `openspec/project.md` documentation to require validation and link to the CI status.

**BREAKING:** No.

## Impact
- Affected specs: none existing specs will be modified by this proposal — this proposal adds a validation gate.
- Affected files: `openspec/changes/*` (authors), `openspec/project.md` (policy), `.github/workflows/openspec-validate.yml` (new CI workflow)
- Owner: repo maintainers / CHANGE_ADOPTER team

## Acceptance Criteria
- Authors can run a local `openspec validate <change-id> --strict` and get a non-error exit code for valid proposals.
- Pull requests that add or modify change proposals or specs are validated in CI and fail when validation errors exist.
