
from neo4j import Session
from . import config
from flask import Flask
from reconverse.server.routes import configure_routes
import logging
from xml.dom import NotFoundErr

from reconverse.models import Neo4jClient, rdb

from reconverse.services.itext2kg.interface import iText2KGInterface

class Reconverse:
    def __init__(self, env: str):
        self.env = env
        self.accepted_document_types = None
        self._instantiate_logger()
        self._instantiate_neo4j_client()
        self._instantiate_itext2kg_interface()
        self._create_and_deploy_api()

    def _instantiate_logger(self) -> None:
        logger = logging.getLogger(__name__)

        # Create stream handler
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        handler.setFormatter(formatter)


        if self.env == "development":
            logger.setLevel(logging.DEBUG)
            handler.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
            handler.setLevel(logging.INFO)

        logger.addHandler(handler)
        self.logger = logger

    def _instantiate_neo4j_client(self) -> None:
        self.logger.info("Instantiating Neo4jClient...")
        self.neo4j_client = Neo4jClient()
        self.logger.info("\t⤷ Done.")

    def _instantiate_itext2kg_interface(self) -> None:
        self.logger.info("Instantiating iText2KGInterface...")
        self.itext2g_interface = iText2KGInterface(self)
        self.accepted_document_types = [key for key in iText2KGInterface.accepted_document_types]
        self.logger.info("\t⤷ Done.")

    def _create_api(self) -> None:
        self.api = Flask(__name__)
        match self.env:
            case 'development':
                self.api.config.from_object(config.APIDevelopmentConfig)
            case 'testing':
                self.api.config.from_object(config.APITestingConfig)
            case _:
                raise Exception(f"Invalid environment: {self.env}")

        configure_routes(self, self.api)

    def _create_and_deploy_api(self) -> None:
        self._create_api()

        if self.env == "development" or self.env == "testing":
            host = '127.0.0.1'
            port = 5000
            debug = True
        else:
            host = '0.0.0.0' #TODO fix
            port = 8080
            debug = False


        self.logger.info(f"Running API on host {host}, port {port}...")
        self.api.run(host='127.0.0.1', port=5000, debug=debug)

    def _connect_to_cp_gdb(self, counterparty_id) -> Session:
        try:
            gdb_name, gdb_provider = rdb.get_gdb_name_from_cp_id(counterparty_id)
            self.logger.info(f"Successfully retrieved graph database name '{gdb_name}' hosted by '{gdb_provider}' that maps to counterparty ID {counterparty_id}")

        except NotFoundErr:  # TODO Replace with the specific exception you expect from get_knowledge_graph_id_from_cp_id
            self.logger.warning(f"No existing GDB found for counterparty ID {counterparty_id}. Creating a new GDB.")

            # Temporary hardcode
            gdb_name, gdb_provider = "neo4j", "neo4j"

        except Exception as e:  # Generic exception handling for unexpected errors
            self.logger.error(f"Unexpected error occurred while processing counterparty ID {counterparty_id}: {e}",
                         exc_info=True)
            raise e

        match gdb_provider:
            case "neo4j":
                return self.neo4j_client.create_session(gdb_name)
            case _:
                raise Exception(f"Unknown provider: {gdb_provider}")


    def _visualize_kg(self, gdb_provider, kg):
        match gdb_provider:
            case "neo4j":
                self.itext2g_interface.visualize_knowledge_graph(kg=kg)
            case _:
                raise Exception(f"Unknown provider: {gdb_provider}")


    def internalize(self, raw_text, document_type, counterparty_id, expects_response):

        # Execute iText2KG pipeline
        self.logger.info("Reconverse: building semantic blocks...")
        semantic_blocks = self.itext2g_interface.build_semantic_blocks(raw_text=raw_text, document_type=document_type)
        self.logger.info("Reconverse: building knowledge graph...")
        kg = self.itext2g_interface.build_knowledge_graph(semantic_blocks=semantic_blocks)

        with self._connect_to_cp_gdb(counterparty_id) as session:
            ## Visualize graph
            self.logger.info("Reconverse: visualizing graph...")
            self.neo4j_client.visualize_graph(kg=kg, session=session)

    def shutdown(self):
        self.neo4j_client.close()
