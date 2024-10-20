from contextlib import contextmanager
import os
from neo4j import GraphDatabase, Transaction


class KnowledgeGraphManager:
    def __init__(self):
        self.uri = os.environ["NEO4J_URI"]
        self.user = os.environ["NEO4J_USER"]
        self.password = os.environ["NEO4J_PASSWORD"]
        self.database = os.environ["NEO4J_DATABASE"]
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    @contextmanager
    def transactional_graph(self):
        with self.driver.session(database=self.database) as session:
            with session.begin_transaction() as tx:
                yield KnowledgeGraph(tx)


class KnowledgeGraph:
    def __init__(self, tx: Transaction):
        self.tx = tx

    def create_node(self, label: str, properties: dict | None = None):
        # CREATE (n:label { key1: value1, key2: value2, ... })

        _check_valid_label(label)

        query = f"CREATE (n:{label} $props) RETURN n"
        result = self.tx.run(
            query,  # type: ignore
            label=label,
            props=properties,
        ).single()
        if result is None:
            return None
        return result[0]

    def get_node(self, label: str, properties: dict | None):
        # MATCH (n:label { key1: value1, key2: value2, ... }) RETURN n

        _check_valid_label(label)

        props_query_parts = []
        props_query_values = {}
        for i, (key, value) in enumerate((properties or {}).items()):
            _check_valid_property_key(key)
            prop_value_id = f"prop_{i}"
            props_query_parts.append(f"{key}: ${prop_value_id}")
            props_query_values[prop_value_id] = value
        props_query = ", ".join(props_query_parts)

        query = f"MATCH (n:{label} {{ {props_query} }}) RETURN n"
        result = self.tx.run(
            query,  # type: ignore
            label=label,
            **props_query_values,
        ).single()
        if result is None:
            return None
        return result[0]

    def rollback(self):
        self.tx.rollback()


def _check_valid_label(label: str):
    if not label.isidentifier():
        raise ValueError(f"Invalid label: {label}")


def _check_valid_property_key(key: str):
    if not key.isidentifier():
        raise ValueError(f"Invalid property key: {key}")
