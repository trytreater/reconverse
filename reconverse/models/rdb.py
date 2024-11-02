import psycopg

def get_gdb_name_from_cp_id(counterparty_id) -> tuple[str, str]:
    """
    Retrieves the name of the graph database associated with a given counterparty ID.
    """

    # Futureproof
    gdb_provider = "neo4j"

    try:
        # Connect to the database
        DATABASE_URL = ""
        with psycopg.connect(DATABASE_URL) as conn:
            # Use a server-side cursor for efficient memory management
            with conn.cursor() as cursor:
                # Execute a parameterized query for safety
                cursor.execute("SELECT kg_id FROM entities WHERE cp_id = %s", (counterparty_id,))

                # Fetch one result
                result = cursor.fetchone()

                # Extract kg_id if found, else return a placeholder
                gdb_name = result[0] if result else "dummy_kg_id"

    except Exception:
        # print(f"Error fetching kg_id for counterparty_id {counterparty_id}: {e}")
        gdb_name = "neo4j"  # Default name in Neo4j Community Version
        gdb_provider = "neo4j"

    return gdb_name, gdb_provider
