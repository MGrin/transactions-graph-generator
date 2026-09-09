<!-- agents-md ceiling: 77 lines -->
# AGENTS.md — transactions-graph-generator

Generates a large synthetic transactions graph — clients, companies, ATMs and the
transactions between them — with money-laundering patterns (flow, circular, time) planted
inside it and **labelled**. [`README.md`](README.md) is the user-facing document: every
flag, every generated column, and what each transformation script produces.

## Commands, run 2026-09-09

```sh
mkdir -p data output logs                    # REQUIRED FIRST — nothing creates these
pipenv install                               # NOT run here: pipenv is not on this machine
pipenv run python generateGraph.py 100
```

What was actually exercised, and how, because `pipenv` was absent:

```sh
uv run --with 'mimesis>=5.0,<22' --with numpy --with typing_extensions \
  python generateGraph.py 20                 # rc=0 — wrote 12 CSVs under data/<timestamp>/
```

That is a faithful substitute — the `Pipfile` pins exactly those three packages — but
`Pipfile.lock` is the real dependency contract and `uv` does not read it. Use `pipenv` when
you have it.

**There is no test suite and no CI** (`.github/` does not exist). The generator running to
completion and producing non-empty CSVs is the entire signal.

## Two things that bite on the first run

- **`data`, `output` and `logs` must exist before you start.** The README's first line says
  so; nothing creates them and the failure is not obvious.
- **An empty CSV is normal at small N.** The 20-client run wrote
  `nodes.transactions.company-sourcing.csv` and `patterns.flow.csv` at zero bytes: the
  probabilities simply did not fire. Do not read an empty pattern file as a broken build —
  raise N or the `--probs` before concluding anything.

## The `pattern` column is the point

Every transaction row carries the ground-truth label of the pattern that produced it —
`flow`, `circular`, `time`, or `None` for background noise (verified in the generated CSVs:
`…|None` for the sourcing files, `…|time` in `patterns.time.csv`). **That label must survive
every transformation script**, or the shuffled output stops being usable for training and
evaluation, which is what the data is for.

Output is **pipe-delimited**, not comma-delimited, despite the `.csv` extension.

## Layout

| path | what it is |
|---|---|
| `generateGraph.py` | the entry point and the configuration reference — the flags are documented in the file itself |
| `generator/` | one module per step: `generateNodes`, `generateEdges`, `generateTransactions`, `generatePatterns` |
| `models/` | `Client`, `Company`, `ATM`, `Node`, `Transaction`, `Patterns` |
| `scripts/output2*.sh` | shuffle+concat to CSV, or build the import for neo4j / postgres / orientdb, optionally starting a docker image with the data loaded |
| `Pipfile` | the dependency contract, with the reason for each pin written beside it |

## Conventions that differ from the defaults

- **`--steps` is ordered and the order is a real dependency**: nodes → edges →
  transactions → patterns. Transactions cannot be generated before edges exist.
- **`--batch-size` controls memory, disk-write frequency AND log frequency** at once. It is
  one knob for three things; a change to it changes how much progress you see.
- **The `mimesis` floor of 5.0.0 is not arbitrary** — that release renamed `Business` →
  `Finance` and `Numbers` → `Numeric`. `typing_extensions` is pinned only because `mimesis`
  imports it without declaring it; the comment says to drop it when upstream fixes that.
- **The generator has never been run above ~100,000 nodes.** The README says "theoretically
  supports" any size, and that is exactly the claim it makes — do not quote it as a measured
  one.

**Nothing about who may merge, how agents are spawned, or how the maintainer's
machine handles secrets belongs in this file, and none of it is stated here.**
Those are properties of a working environment, not of this project; if you are
contributing, your own conventions apply and nothing in this repo depends on
the maintainer's.
