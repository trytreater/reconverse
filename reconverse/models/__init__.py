from neo4j import GraphDatabase, Driver, Session
import os
from itext2kg.models import KnowledgeGraph, Entity, EntityProperties, Relationship, RelationshipProperties
import numpy as np
from typing import List, Optional


class Neo4jClient:
    """Class to manage interactions with the Neo4j database."""

    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")

        self.driver = self.connect()

    @staticmethod
    def load_kg_into_memory(session) -> Optional[KnowledgeGraph]:

        def convert_embedding_from_str_to_np_arr(embedding_str: str) -> np.ndarray:
            # Split the string by comma and convert each piece to a float
            array = np.array(embedding_str.split(','), dtype=np.float32)
            return array

        kg = KnowledgeGraph()

        # nodes_result = session.run("MATCH (n) RETURN n")
        # for record in nodes_result:
        #     labels = record["labels(n)"]
        #     name = record["n.name"]
        #     entity = Entity(label=labels[0] if labels else "", name=name)
        #     kg.entities.append(entity)

        node_id_map = {}

        nodes_query_result = session.run("MATCH (n) RETURN n")
        for record in nodes_query_result:
            neo4j_node_obj = record["n"]
            embeddings = convert_embedding_from_str_to_np_arr(neo4j_node_obj._properties.get("embeddings"))
            # print(node.id, node.element_id, node.labels, node._properties.get("name"), node._properties.get("embeddings")[:10])
            entity = Entity(
                label=list(neo4j_node_obj.labels)[0] if neo4j_node_obj.labels else "",
                name=neo4j_node_obj._properties.get("name"), # iText2KG Entity model is not perfectly symmetrical with Neo4j node...
                properties=EntityProperties(
                    embeddings=embeddings
                )
            )

            node_id_map[neo4j_node_obj.id] = entity

            kg.entities.append(entity)

        relationships_query_results = session.run("""
            MATCH (start)-[r]->(end)
            RETURN id(start) AS start_id, id(end) as end_id, r as r
            """)
        for record in relationships_query_results:
            start = node_id_map[record["start_id"]]
            end = node_id_map[record["end_id"]]
            neo4j_relationship_obj = record["r"]


            embeddings = convert_embedding_from_str_to_np_arr(neo4j_relationship_obj._properties.get("embeddings"))

            relationship = Relationship(
                startEntity=start,
                endEntity=end,
                name=neo4j_relationship_obj.type,
                properties=RelationshipProperties(
                    embeddings=embeddings
                )
            )
            kg.relationships.append(relationship)


        if kg.entities or kg.relationships:
            return kg
        else:
            return None

    def connect(self) -> Driver:
        return GraphDatabase.driver(self.uri, auth=(self.username, self.password))

    def create_session(self, database_name) -> Session:
        """Establishes a connection to the Neo4j database."""
        return self.driver.session(database=database_name)

    @staticmethod
    def transform_embeddings_to_str_list(embeddings: np.array):
        """
        Transforms a NumPy array of embeddings into a comma-separated string.

        Args:
        embeddings (np.array): An array of embeddings.

        Returns:
        str: A comma-separated string of embeddings.
        """
        if embeddings is None:
            return ""
        return ",".join(list(embeddings.astype("str")))

    @staticmethod
    def transform_str_list_to_embeddings(embeddings: Optional[str]):
        """
        Transforms a comma-separated string of embeddings back into a NumPy array.

        Args:
        embeddings (Optional[str]): A comma-separated string of embeddings. If None, returns an empty array.

        Returns:
        np.array: A NumPy array of embeddings, with dtype as float64. Returns an empty array if input is None.
        """
        if embeddings is None:
            return np.array([], dtype=np.float64)
        return np.array(embeddings.split(","), dtype=np.float64)

    @staticmethod
    def create_nodes(kg: KnowledgeGraph) -> List[str]:
        """
        Constructs Cypher queries for creating nodes in the graph database from a KnowledgeGraph object.

        Args:
        knowledge_graph (KnowledgeGraph): The KnowledgeGraph object containing entities.

        Returns:
        List[str]: A list of Cypher queries for node creation.
        """
        queries = []
        for node in kg.entities:
            properties = []
            for prop, value in node.properties.model_dump().items():
                if prop == "embeddings":
                    value = Neo4jClient.transform_embeddings_to_str_list(value)
                properties.append(f'SET n.{prop.replace(" ", "_")} = "{value}"')

            query = f'CREATE (n:{node.label} {{name: "{node.name}"}}) ' + ' '.join(properties)
            queries.append(query)
        return queries

    @staticmethod
    def create_relationships(kg: KnowledgeGraph) -> list:
        """
        Constructs Cypher queries for creating relationships in the graph database from a KnowledgeGraph object.

        Args:
        kg (KnowledgeGraph): The KnowledgeGraph object containing relationships.

        Returns:
        List[str]: A list of Cypher queries for relationship creation.
        """
        rels = []
        for rel in kg.relationships:
            property_statements = ' '.join(
                [f'SET r.{key.replace(" ", "_")} = "{value}"'
                 if key != "embeddings"
                 else f'SET r.{key.replace(" ", "_")} = "{Neo4jClient.transform_embeddings_to_str_list(value)}"'
                 for key, value in rel.properties.model_dump().items()]
            )

            query = (
                f'MATCH (n:{rel.startEntity.label} {{name: "{rel.startEntity.name}"}}), '
                f'(m:{rel.endEntity.label} {{name: "{rel.endEntity.name}"}}) '
                f'MERGE (n)-[r:{rel.name}]->(m) {property_statements}'
            )
            rels.append(query)

        return rels

    def visualize_graph(self, kg: KnowledgeGraph, session) -> None:
        """
        Runs the necessary queries to visualize a graph structure from a KnowledgeGraph input.

        Args:
        kg (KnowledgeGraph): The KnowledgeGraph object containing the graph structure.
        """

        session.run("MATCH (n) DETACH DELETE n")

        nodes, relationships = (
            self.create_nodes(kg=kg),
            self.create_relationships(kg=kg),
        )

        for node in nodes:
            session.run(node)

        for relation in relationships:
            session.run(relation)

    def close(self):
        """Closes the connection to the Neo4j database."""
        if self.driver:
            self.driver.close()
            self.driver = None