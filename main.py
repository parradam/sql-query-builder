from typing import Any
from typing_extensions import Self
from dataclasses import dataclass, field
import dataclasses_json

@dataclass
class JoinCondition:
    firstTable: str
    firstField: str
    secondTable: str
    secondField: str
    operator: str

@dataclass
class Join:
    type: str
    table: str
    conditions: list[JoinCondition]

@dataclass
class WhereCondition:
    table: str
    field: str
    value: str

@dataclass
class Relationship:
    from_field: str
    to_table: str
    to_field: str
    objective: str

@dataclass
class Table:
    name: str
    fields: list[str] = field(default_factory=list)
    relationships: list[Relationship] = field(default_factory=list)
    whereConditions: list[WhereCondition] = field(default_factory=list)

@dataclass
class Schema(dataclasses_json.DataClassJsonMixin):
    tables: list[Table]

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
        return f"{join_condition.firstTable}.{join_condition.firstField} = {join_condition.secondTable}.{join_condition.secondField}"

    @staticmethod
    def _build_where_conditions(where_condition: WhereCondition) -> str:
        return f"{where_condition.table}.{where_condition.field} = {where_condition.value}"

# Convert to dataclass
def convert_to_dataclass(input: dict[str, Any]) -> Schema:
    schema = Schema.from_dict(input)
    return schema

# Validate (coming soon)

# Decide how to build query and call QueryBuilder
def create_query(dc: Schema) -> str:
    qb = QueryBuilder()

    qb.from_table(dc.tables[0].name)

    for table in dc.tables:
        if table.fields:
            qb.select(*table.fields)
        
        if table.whereConditions:
            qb.where(table.whereConditions)

        if table.relationships:
            join_conditions: list[JoinCondition] = []
        
            for relationship in table.relationships:
                join_conditions.append(JoinCondition(table.name, relationship.from_field, relationship.to_table, relationship.to_field, "="))
            qb.join(Join("INNER", table.relationships[0].to_table, join_conditions))

    return qb.build()