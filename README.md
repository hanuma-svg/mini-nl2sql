# mini-nl2sql

Converts English questions into SQL using rule-based parsing and a sqlglot AST builder with a 100-run determinism test — no LLM in the calculation path.

**Live demo:** [https://mini-nl2sql.streamlit.app/](https://mini-nl2sql.streamlit.app/)

## Why I built it

I built this because LLM-based NL-to-SQL tools fail silently: they produce queries that look plausible but return incorrect numbers for business decisions. This is a 1% scale model demonstrating the deterministic approach used by query engines like Trinetro Labs' TRE, separating strict intent parsing from AST-driven SQL generation with an audit trail.

## How to run it

```bash
python db.py
streamlit run app.py
python main.py "How many orders did customer 5 place?"
pytest -v
```

## What it does

- Parser maps 3 question patterns to structured intents — no fuzzy match, no LLM
- Builder emits SQL via sqlglot AST — no f-strings, no concatenation
- Every answer ships with an audit trail: intent, SQL, tables, columns, execution time
- Determinism test: 100 runs of the same intent → 1 unique SQL string

## What it does NOT do

- Only 3 question patterns — no free-form English
- No multi-table joins
- No LLM parser — that is the point
- Only SQLite; only the orders and customers tables
- No authentication, multi-user, or deployment config

## What I'd build next

- Grain compatibility checker — catch double-counting when metric grain does not match dimension grain
- BFS join resolver over foreign keys
- Governed metric memory — versioned metric definitions
- Optional LLM parser that still feeds the same deterministic builder
