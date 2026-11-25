from builder import build
from parser import parse


def test_build_is_deterministic():
    intent = {
        "metric": "count_orders",
        "table": "orders",
        "filter_column": "customer_id",
        "filter_value": 5,
    }
    results = {build(intent) for _ in range(100)}
    assert len(results) == 1


def test_parse_is_deterministic():
    question = "How many orders did customer 5 place?"
    results = {str(parse(question)) for _ in range(100)}
    assert len(results) == 1


def test_full_pipeline_is_deterministic():
    question = "What is the total amount of all orders?"
    sqls = {build(parse(question)) for _ in range(100)}
    assert len(sqls) == 1
