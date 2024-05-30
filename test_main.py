from main import Relationship, build_query


def test_join_with_two_tables() -> None:
    relationships: list[Relationship] = [
        Relationship("customers", "customer_id", "orders", "customer_id"),
        Relationship("orders", "order_id", "order_items", "order_id"),
    ]

    q: str = build_query(relationships)

    assert q == (
        "SELECT\n"
        "\t-- [fields]\n"
        "FROM customers\n"
        "JOIN orders ON customers.customer_id = orders.customer_id\n"
        "JOIN order_items ON orders.order_id = order_items.order_id"
    )


def test_join_with_four_tables() -> None:
    relationships: list[Relationship] = [
        Relationship("customers", "customer_id", "orders", "customer_id"),
        Relationship("orders", "order_id", "order_items", "order_id"),
        Relationship("order_items", "product_id", "products", "product_id"),
        Relationship("products", "category_id", "categories", "category_id"),
    ]

    q: str = build_query(relationships)

    assert q == (
        "SELECT\n"
        "\t-- [fields]\n"
        "FROM customers\n"
        "JOIN orders ON customers.customer_id = orders.customer_id\n"
        "JOIN order_items ON orders.order_id = order_items.order_id\n"
        "JOIN products ON order_items.product_id = products.product_id\n"
        "JOIN categories ON products.category_id = categories.category_id"
    )
