# Project Context

## Purpose
This repository holds the OpenSpec-driven definition and change management for the project: a small, spec-first CLI and tooling set that helps the team author, review, validate, and archive behavioral specs and change proposals. The goal is to keep requirements, proposals, and implementation aligned and machine-validated using the `openspec` workflow.

## Tech Stack
- Primary runtime: `Node.js` (>=18) with `TypeScript` for CLI tooling
- CLI tooling: `openspec` (project-specific tooling), `npm` scripts
- Validation & tests: `jest` for unit tests, lightweight integration tests for CLI commands
- CI: `GitHub Actions` for validation, linting, and test runs
- Developer experience: `prettier`, `eslint` (TypeScript rules), and `husky` + `lint-staged` for pre-commit checks

## Project Conventions

### Code Style
- Use `Prettier` for formatting and `ESLint` for linting. Follow the TypeScript recommended rules with `strict` enabled.
- File names: `kebab-case` for CLI modules and `PascalCase` for exported classes.
- Exports: prefer named exports; default exports only for small utility entrypoints.

### Architecture Patterns
- Keep the codebase modular and small: separate `cli/`, `lib/`, and `scripts/` folders when code grows.
- Each capability lives in `openspec/specs/<capability>/spec.md` and any change proposals live in `openspec/changes/<change-id>/`.
- Prefer single-file implementations for new features until complexity justifies extra structure.

### Testing Strategy
- Unit tests for pure logic using `jest`.
- Integration tests for CLI commands using spawn of `node` in the test sandbox (small and fast).
- Spec validation is part of CI: run `openspec validate --strict` on relevant changes and on main branch.

### Git Workflow
- `main` is the release branch and should always be green.
- Feature branches: `change/<change-id>` for OpenSpec proposals and implementations; `feature/<short-desc>` for non-spec work.
- Commit messages follow Conventional Commits (e.g., `feat: add openspec validate command`).
- Pull requests: link to the `openspec/changes/<change-id>/proposal.md` when applicable and include a checklist from `tasks.md`.

## Domain Context
- This repository is spec-first. The canonical representation of capabilities is in `openspec/specs/` and proposed changes are in `openspec/changes/` until approved and merged.
- Validation rules are strict: requirements MUST use `SHALL`/`MUST` and scenarios MUST use the `#### Scenario:` header format.

## Important Constraints
- All change proposals that affect behavior must include spec deltas and pass `openspec validate <change-id> --strict` before implementation begins.
- Do not merge breaking changes without explicit approval and migration notes in the proposal.
- Keep change proposals small and focused (prefer smaller, incremental proposals).

## External Dependencies
- GitHub (for hosting and CI)
- Node.js (developer runtime)
- Any external APIs called by specs should be documented in the affected capability's spec file and referenced in the proposal's `Impact` section.
