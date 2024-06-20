import factory
from main import JoinCondition, Join, WhereCondition, Relationship, Table, Schema

class JoinConditionFactory(factory.Factory):
    class Meta:
        model = JoinCondition
    
    firstTable = "firstTable"
    firstField = "firstField"
    secondTable = "secondTable"
    secondField = "secondField"
    operator = "="

class JoinFactory(factory.Factory):
    class Meta:
        model = Join

    type = "INNER"
    table = "firstTable"
    conditions = factory.List([
        factory.SubFactory(JoinConditionFactory)
    ])

class WhereConditionFactory(factory.Factory):
    class Meta:
        model = WhereCondition

    table = "firstTable"
    field = "firstTable"
    value = "1"

class RelationshipFactory(factory.Factory):
    class Meta:
        model = Relationship

    from_field = "firstField"
    to_table = "secondTable"
    to_field = "secondField"
    objective = ""

class TableFactory(factory.Factory):
    class Meta:
        model = Table
    
    name = "firstTable"
    fields = factory.List(["field1"])
    relationships = factory.List([
        factory.SubFactory(RelationshipFactory)
    ])
    whereConditions = factory.List([
        factory.SubFactory(WhereConditionFactory)
    ])

class SchemaFactory(factory.Factory):
    class Meta:
        model = Schema
    
    tables = factory.List([
        factory.SubFactory(TableFactory)
    ])

print(SchemaFactory())