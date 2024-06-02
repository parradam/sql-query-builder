from typing import Any
from typing_extensions import Self
from dataclasses import dataclass


@dataclass
class JoinCondition:
    firstField: str
    secondField: str
    operator: str


@dataclass
class Join:
    type: str
    table: str
    conditions: list[JoinCondition]


@dataclass
class WhereCondition:
    field: str
    value: str
    operator: str


class QueryBuilder:
    def __init__(self) -> None:
        self.query: dict[str, Any] = {
            "select": [],
            "from": "",
            "joins": [],
            "where": [],
        }

    def select(self, *fields: str) -> Self:
        self.query["select"].extend(fields)
        return self

    def from_table(self, table: str) -> Self:
        self.query["from"] = table
        return self

    def join(self, join: Join) -> Self:
        initial: str = f"{join.type} JOIN {join.table} ON"
        join_conditions: str = " AND ".join(
            map(QueryBuilder._build_join_conditions, join.conditions)
        )
        join_clause = initial + " " + join_conditions
        self.query["joins"].append(join_clause)
        return self

    def where(self, conditions: list[WhereCondition]) -> Self:
        where_conditions: str = " AND ".join(
            map(QueryBuilder._build_where_conditions, conditions)
        )
        self.query["where"].append(where_conditions)
        return self

    def build(self) -> str:
        select: str = "SELECT " + ", ".join(self.query["select"])
        from_table: str = "\nFROM " + self.query["from"]
        joins: str = "\n" + "\n".join(self.query["joins"])
        where: str = "\nWHERE " + " AND ".join(self.query["where"])

        return select + from_table + joins + where

    @staticmethod
    def _build_join_conditions(join_condition: JoinCondition) -> str:
        return f"{join_condition.firstField} {join_condition.operator} {join_condition.secondField}"

    @staticmethod
    def _build_where_conditions(where_condition: WhereCondition) -> str:
        return f"{where_condition.field} {where_condition.operator} {where_condition.value}"


def validate_structure() -> None:
    pass


def format_input() -> None:
    pass


def handler() -> None:
    # Create dataclasses uses format_input

    # Validate the structure using validate_structure

    # Build the query

    # Return the result
    pass
