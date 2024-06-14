from main import JoinCondition, Join, WhereCondition, QueryBuilder, convert_to_dataclass, Schema, create_query


def test_join_with_two_tables() -> None:
    where_condition_1 = WhereCondition("customers", "customer_id", "1")
    new_where: list[WhereCondition] = [where_condition_1]

    join_condition_1 = JoinCondition("customers", "customer_id", "orders", "customer_id", "=")
    join_condition_2 = JoinCondition(
        "customers", "customer_id2", "orders", "customer_id2", "="
    )
    new_join = Join("INNER", "orders", [join_condition_1, join_condition_2])

    qb = QueryBuilder()
    qb.select("field1").from_table("customers").join(new_join).where(new_where)
    q: str = qb.build()

    assert q == (
        "SELECT field1\n"
        "FROM customers\n"
        "INNER JOIN orders ON customers.customer_id = orders.customer_id AND customers.customer_id2 = orders.customer_id2\n"
        "WHERE customers.customer_id = 1"
    )


def test_join_with_four_tables() -> None:
    where_condition_1 = WhereCondition("customers", "customer_id", "1")
    new_where: list[WhereCondition] = [where_condition_1]

    join_condition_1 = JoinCondition("customers", "customer_id", "orders", "customer_id", "=")
    join_condition_2 = JoinCondition("orders", "order_id", "products", "order_id", "=")
    join_condition_3 = JoinCondition(
        "customers", "customer_id", "transactions", "customer_id", "="
    )
    new_join = Join("INNER", "orders", [join_condition_1])
    new_join2 = Join("INNER", "products", [join_condition_2])
    new_join3 = Join("INNER", "transactions", [join_condition_3])

    qb = QueryBuilder()
    qb.select("field1").from_table("customers").join(new_join).join(new_join2).join(
        new_join3
    ).where(new_where)
    q: str = qb.build()

    assert q == (
        "SELECT field1\n"
        "FROM customers\n"
        "INNER JOIN orders ON customers.customer_id = orders.customer_id\n"
        "INNER JOIN products ON orders.order_id = products.order_id\n"
        "INNER JOIN transactions ON customers.customer_id = transactions.customer_id\n"
        "WHERE customers.customer_id = 1"
    )

def test_create_query_with_two_tables() -> None:
    obj = {
        "tables": [
            {
                "name": "customers",
                "fields": [],
                "relationships": [
                    {
                        "from_field": "customer_id",
                        "to_table": "orders",
                        "to_field": "customer_id",
                        "objective": "all customers even if no orders"
                    },
                    {
                        "from_field": "customer_id2",
                        "to_table": "orders",
                        "to_field": "customer_id2",
                        "objective": "all customers even if no orders"
                    }
                ],
                "whereConditions": [
                    {
                        "table": "customers",
                        "field": "customer_id",
                        "value": "1"
                    }
                ]
            },
            {
                "name": "orders",
                "fields": ["order_stuff"]
            }
        ],
    }

    dc: Schema = convert_to_dataclass(obj)
    q: str = create_query(dc)

    assert q == (
        "SELECT order_stuff\n"
        "FROM customers\n"
        "INNER JOIN orders ON customers.customer_id = orders.customer_id AND customers.customer_id2 = orders.customer_id2\n"
        "WHERE customers.customer_id = 1"
    )