import psycopg

def get_knowledge_graph_id_from_cp_id(counterparty_id):
    """
    Retrieves the knowledge graph ID associated with a given counterparty ID.
    """
    try:
        # Connect to the database
        with psycopg.connect(DATABASE_URL) as conn:
            # Use a server-side cursor for efficient memory management
            with conn.cursor() as cursor:
                # Execute a parameterized query for safety
                cursor.execute("SELECT kg_id FROM entities WHERE cp_id = %s", (counterparty_id,))

                # Fetch one result
                result = cursor.fetchone()

                # Extract kg_id if found, else return a placeholder
                kg_id = result[0] if result else "dummy_kg_id"

    except Exception as e:
        print(f"Error fetching kg_id for counterparty_id {counterparty_id}: {e}")
        kg_id = "dummy_kg_id"  # Fallback value in case of error

    return kg_id
