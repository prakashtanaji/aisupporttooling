# AI Support Tooling

This repository contains small Python examples and tests for reusable support utilities.

## Current package

The current reusable package is `codexAgents`.

Key files:
- `codexAgents/src/originalFunc.py`
- `codexAgents/src/__init__.py`
- `codexAgents/units/test_originalFunc.py`

## What the code does

`codexAgents/src/originalFunc.py` exposes `calculate_final_cost`, which calculates a discounted price with these rules:
- `discount` defaults to `0`
- `discount=None` is treated as `0`
- negative prices are rejected
- negative discounts are rejected
- discounts greater than `100` are rejected

## How to run

Run the example script from the repository root:

```powershell
python .\codexAgents\src\originalFunc.py
```

Expected output:

```text
Cost for discount 80.0
```

## How to run tests

Run the unit test module from the repository root:

```powershell
python -m unittest codexAgents.units.test_originalFunc
```

## Pre-commit hook

This repository includes a Git pre-commit hook at `.githooks/pre-commit`.
It runs the unit test command below and aborts the commit if the tests fail:

```powershell
python -m unittest codexAgents.units.test_originalFunc
```

Enable repo-managed hooks in your local clone with:

```powershell
git config core.hooksPath .githooks
```

## How to import the function

You can import the reusable function with:

```python
from codexAgents.src import calculate_final_cost
```
