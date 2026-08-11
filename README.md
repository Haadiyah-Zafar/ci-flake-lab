# ci-flake-lab

Synthetic flaky-test lab for demonstrating **FlakeFixer**. This repo intentionally produces diverse CI failures that mirror real-world flake patterns.

## Flake types

| Matrix job | Env var | Simulated failure |
|---|---|---|
| `RACE` | `FLAKE_RACE=1` | Race condition / threading |
| `NETWORK` | `FLAKE_NETWORK=1` | Network timeout |
| `INFRA` | `FLAKE_INFRA=1` | Infrastructure blip (disk space) |
| `DEPENDENCY` | `FLAKE_DEPENDENCY=1` | Missing dependency import |

## Trigger runs

- **Push** to any branch runs the workflow automatically.
- **Manual:** Actions → **Flake Farm** → **Run workflow**.

Each matrix job runs one flake type. Re-run failed jobs to build a history of failures for FlakeFixer to analyze.

## Local testing

```bash
pip install pytest
set FLAKE_NETWORK=1
pytest test_app.py -v
```

## Related

Pair this repo with [flake-fixer](../flake-fixer) — the agent that ingests these failures and opens GitHub issues.
