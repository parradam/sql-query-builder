class Relationship:
    def __init__(
        self, from_table: str, from_field: str, to_table: str, to_field: str
    ) -> None:
        self.from_table: str = from_table
        self.from_field: str = from_field
        self.to_table: str = to_table
        self.to_field: str = to_field


def build_query(relationships: list[Relationship]) -> str:
    joins = []
    last_table = None
    this_join = ""

    # Follow relationships
    for relationship in relationships:
        if relationship.from_table is not last_table:
            # If it's the first time with a relationship, creat a JOIN statement
            this_join: str = f"JOIN {relationship.to_table} ON {relationship.from_table}.{relationship.from_field} = {relationship.to_table}.{relationship.to_field}"
        else:
            # Add to existing JOIN with AND:
            this_join += f" AND {relationship.from_table}.{relationship.from_field} = {relationship.to_table}.{relationship.to_field}"

        # Error if relationship not found

        # Append to joins list
        joins.append(this_join)
        last_table: str = relationship.from_table

    # Convert joins list to string
    joins_string = "\n".join(joins)

    # Create initial SELECT ... FROM ...
    select_from: str = f"SELECT\n\t-- [fields]\nFROM {relationships[0].from_table}\n"

    # Combine statements
    query: str = select_from + joins_string

    # Return result
    return query
