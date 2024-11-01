from neo4j import GraphDatabase
import os

class Neo4jClient:
    """Class to manage interactions with the Neo4j database."""

    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = None

    def connect(self):
        """Establishes a connection to the Neo4j database."""
        if not self.driver:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password)
            )

    def close(self):
        """Closes the connection to the Neo4j database."""
        if self.driver:
            self.driver.close()
            self.driver = None
