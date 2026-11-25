from errors import BuildError
from sqlglot import exp

ALLOWED_METRICS = {"count_orders", "sum_amount", "avg_amount"}
ALLOWED_TABLES = {"orders"}
ALLOWED_FILTER_COLUMNS = {"customer_id", None}


def build(intent: dict) -> str:
    metric = intent.get("metric")
    table = intent.get("table")
    filter_column = intent.get("filter_column")
    filter_value = intent.get("filter_value")

    if metric not in ALLOWED_METRICS:
        raise BuildError(
            f"Unknown metric '{metric}'. Available: count_orders, sum_amount, avg_amount"
        )

    if table not in ALLOWED_TABLES:
        raise BuildError(f"Unknown table '{table}'. Available: orders")

    if filter_column not in ALLOWED_FILTER_COLUMNS:
        raise BuildError(
            f"Unknown filter column '{filter_column}'. Available: customer_id"
        )

    if metric == "count_orders":
        metric_expr = exp.Count(this=exp.Star())
    elif metric == "sum_amount":
        metric_expr = exp.Sum(this=exp.column("amount"))
    elif metric == "avg_amount":
        metric_expr = exp.Avg(this=exp.column("amount"))

    select = exp.Select().select(metric_expr).from_(table)

    if filter_column is not None:
        select = select.where(
            exp.EQ(
                this=exp.column(filter_column),
                expression=exp.Literal.number(filter_value),
            )
        )

    return select.sql(dialect="sqlite")
