# bailian-cli `reference/` maintenance

The Markdown files under `reference/` are **generated** from the open-source CLI repo ([modelstudioai/cli](https://github.com/modelstudioai/cli)) via `pnpm --filter bailian-cli run generate:reference` (see `tools/generate-reference.ts` there). Do not edit them by hand.

## Pin file

`./.reference-cli-ref` is a single line: the **git ref** (branch or tag) on `modelstudioai/cli` that the committed `reference/*.md` must match. The **Check bailian-cli reference** GitHub Action uses it.

## Workflows (repo root `.github/workflows/`)

| Workflow | Purpose |
|----------|---------|
| **Sync bailian-cli reference** (`workflow_dispatch`) | Check out cli at the given ref, regenerate, rsync into `skills/bailian-cli/reference/`, update `.reference-cli-ref`, open a PR. |
| **Check bailian-cli reference** | On PR/push (when these paths change), regenerate from the pinned cli ref and `diff` against the repo; fails if out of sync. |

## After changing CLI commands

1. Land changes in [modelstudioai/cli](https://github.com/modelstudioai/cli) (update `catalog.ts`, etc.).
2. In **this** repo: Actions → **Sync bailian-cli reference** → Run workflow (set `cli_ref` to `main` or a release tag; use `cli_repository` for forks).
3. Merge the resulting PR.

For forks of cli, set `cli_repository` to `your-org/cli` when running the sync workflow.
