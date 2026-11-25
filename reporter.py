def report(question: str, intent: dict, sql: str, result: dict) -> None:
    if intent.get("filter_column") is not None and intent.get("filter_value") is not None:
        filter_str = f"{intent['filter_column']} = {intent['filter_value']}"
    else:
        filter_str = "none"

    metric = intent.get("metric")
    filter_col = intent.get("filter_column")

    cols = []
    if filter_col:
        cols.append(filter_col)
    if metric in ("sum_amount", "avg_amount"):
        cols.append("amount")
    elif metric == "count_orders" and not cols:
        cols.append("all (*)")

    columns_used_str = ", ".join(cols) if cols else "none"

    print("══════════════════════════════════════════════════════")
    print(" QUESTION")
    print(f' "{question}"')
    print()
    print(" PARSED INTENT (rule-based, deterministic)")
    print(f" metric       : {intent.get('metric')}")
    print(f" table        : {intent.get('table')}")
    print(f" filter       : {filter_str}")
    print()
    print(" GENERATED SQL (via sqlglot AST)")
    print(f" {sql}")
    print()
    print(" RESULT")
    print(f" columns      : {result.get('columns')}")
    print(f" rows         : {result.get('rows')}")
    print()
    print(" AUDIT TRAIL")
    print(" method       : rule-based (no LLM in calculation path)")
    print(f" tables used  : {intent.get('table')}")
    print(f" columns used : {columns_used_str}")
    print(f" execution    : {result.get('time_ms')} ms")
    print(f" rows returned: {len(result.get('rows', []))}")
    print("══════════════════════════════════════════════════════")
