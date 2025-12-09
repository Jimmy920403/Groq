## ADDED Requirements

### Requirement: Change proposals MUST be machine-validated
All change proposals in `openspec/changes/<change-id>/` SHALL be valid according to the `openspec` validator.

#### Scenario: Local validation succeeds
- **WHEN** an author runs `openspec validate <change-id> --strict` on a proposal directory that follows the OpenSpec format
- **THEN** the command SHALL exit with code `0` and produce no validation errors

#### Scenario: CI blocks invalid proposals
- **WHEN** a pull request modifies files under `openspec/changes/` or `openspec/specs/`
- **THEN** the CI workflow SHALL run `openspec validate --strict` and fail the build if validation errors are present
