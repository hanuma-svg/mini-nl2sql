import pytest
from errors import ParseError
from parser import parse


def test_count_orders_with_filter():
    assert parse("How many orders did customer 5 place?") == {
        "metric": "count_orders",
        "table": "orders",
        "filter_column": "customer_id",
        "filter_value": 5,
    }


def test_sum_amount_no_filter():
    assert parse("What is the total amount of all orders?") == {
        "metric": "sum_amount",
        "table": "orders",
        "filter_column": None,
        "filter_value": None,
    }


def test_sum_amount_with_revenue_keyword():
    assert parse("total revenue for customer 7") == {
        "metric": "sum_amount",
        "table": "orders",
        "filter_column": "customer_id",
        "filter_value": 7,
    }


def test_avg_amount_with_filter():
    assert parse("What is the average amount for customer 3?") == {
        "metric": "avg_amount",
        "table": "orders",
        "filter_column": "customer_id",
        "filter_value": 3,
    }


def test_unknown_question_raises_parse_error():
    with pytest.raises(ParseError):
        parse("Who are the customers?")


def test_case_insensitive():
    assert parse("HOW MANY ORDERS DID CUSTOMER 2 PLACE?") == {
        "metric": "count_orders",
        "table": "orders",
        "filter_column": "customer_id",
        "filter_value": 2,
    }
