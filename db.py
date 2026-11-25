import os
import sqlite3

DB_PATH = "data.db"


def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            amount REAL
        )
    """
    )

    customers = [
        (1, "Alice"),
        (2, "Bob"),
        (3, "Carol"),
        (4, "David"),
        (5, "Eve"),
        (6, "Frank"),
        (7, "Grace"),
        (8, "Heidi"),
        (9, "Ivan"),
        (10, "Judy"),
    ]
    cursor.executemany("INSERT INTO customers (id, name) VALUES (?, ?)", customers)

    # Customer 3 has 0 orders intentionally as an edge case
    orders = [
        (1, 1, 120.50),
        (2, 1, 45.00),
        (3, 1, 250.00),
        (4, 2, 89.99),
        (5, 2, 310.25),
        (6, 4, 75.00),
        (7, 5, 25.50),
        (8, 5, 140.00),
        (9, 5, 490.00),
        (10, 6, 60.00),
        (11, 6, 185.75),
        (12, 7, 35.00),
        (13, 7, 210.00),
        (14, 7, 115.50),
        (15, 8, 95.00),
        (16, 8, 420.00),
        (17, 9, 150.00),
        (18, 9, 275.50),
        (19, 10, 50.00),
        (20, 10, 380.00),
    ]
    cursor.executemany(
        "INSERT INTO orders (id, customer_id, amount) VALUES (?, ?, ?)", orders
    )

    conn.commit()
    conn.close()
