import re
from errors import ParseError


def parse(question: str) -> dict:
    q = question.lower()

    # "total revenue" must match before "total amount" if distinct, but both map to sum_amount
    if "how many orders" in q:
        metric = "count_orders"
    elif "total amount" in q:
        metric = "sum_amount"
    elif "total revenue" in q:
        metric = "sum_amount"
    elif "average amount" in q:
        metric = "avg_amount"
    else:
        raise ParseError(
            "I could not understand the question. Try one of these:\n"
            '  - "How many orders did customer 5 place?"\n'
            '  - "What is the total amount of all orders?"\n'
            '  - "What is the average amount for customer 3?"'
        )

    table = "orders"

    match = re.search(r"customer\s+(\d+)", q)
    if match:
        filter_column = "customer_id"
        filter_value = int(match.group(1))
    else:
        filter_column = None
        filter_value = None

    return {
        "metric": metric,
        "table": table,
        "filter_column": filter_column,
        "filter_value": filter_value,
    }
