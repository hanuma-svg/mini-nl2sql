import pytest
from errors import BuildError
from builder import build


def norm(sql):
    return " ".join(sql.split()).upper()


def test_count_with_filter():
    actual = build(
        {
            "metric": "count_orders",
            "table": "orders",
            "filter_column": "customer_id",
            "filter_value": 5,
        }
    )
    expected = "SELECT COUNT(*) FROM orders WHERE customer_id = 5"
    assert norm(actual) == norm(expected)


def test_sum_no_filter():
    actual = build(
        {
            "metric": "sum_amount",
            "table": "orders",
            "filter_column": None,
            "filter_value": None,
        }
    )
    expected = "SELECT SUM(amount) FROM orders"
    assert norm(actual) == norm(expected)


def test_avg_with_filter():
    actual = build(
        {
            "metric": "avg_amount",
            "table": "orders",
            "filter_column": "customer_id",
            "filter_value": 3,
        }
    )
    expected = "SELECT AVG(amount) FROM orders WHERE customer_id = 3"
    assert norm(actual) == norm(expected)


def test_invalid_metric_raises_build_error():
    with pytest.raises(BuildError):
        build(
            {
                "metric": "bogus",
                "table": "orders",
                "filter_column": None,
                "filter_value": None,
            }
        )


def test_invalid_table_raises_build_error():
    with pytest.raises(BuildError):
        build(
            {
                "metric": "count_orders",
                "table": "unknown",
                "filter_column": None,
                "filter_value": None,
            }
        )
