from . import config
from flask import Flask
from reconverse.server.routes import configure_routes
import logging
from xml.dom import NotFoundErr

from reconverse.models import Neo4jClient, rdb
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os
from reconverse.services.itext2kg.interface import iText2KGInterface

class Reconverse:

    accepted_media = ["email"]

    def __init__(self, env: str):
        self.env = env

        self._instantiate_logger()
        self._instantiate_neo4j_client()
        self._set_llm()
        self._set_embeddings_model()
        self._instantiate_itext2kg_interface()
        self._create_and_deploy_api()

    def _instantiate_logger(self) -> None:
        logger = logging.getLogger(__name__)

        if self.env == "development":
            logger.setLevel(logging.DEBUG)
        self.logger = logger

    def _instantiate_neo4j_client(self) -> None:
        self.neo4j_client = Neo4jClient()

    def _set_llm(self) -> None:
        model_name = os.getenv("LLM", "OPENAI")
        self.llm = None

        match model_name:
            case "OPENAI":
                self.llm = ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-4o",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
                )

    def _set_embeddings_model(self) -> None:
        model_name = os.getenv("EMBEDDING_MODEL", "OPENAI")
        self.embeddings_model = None

        match model_name:
            case "OPENAI":
                self.embeddings_model = OpenAIEmbeddings(
            api_key = os.getenv("OPENAI_API_KEY") ,
            model="text-embedding-3-large",
                )

    def _instantiate_itext2kg_interface(self) -> None:
        self.itext2g_interface = iText2KGInterface(self)


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
            debug = True
        else:
            debug = False

        self.api.run(host='127.0.0.1', port=5000, debug=debug)

    def _get_knowledge_graph_id(self, counterparty_id):
        try:
            kg_id = rdb.get_knowledge_graph_id_from_cp_id(counterparty_id)
            self.logger.info(f"Successfully retrieved KG ID {kg_id} that maps to counterparty ID {counterparty_id}")

        except NotFoundErr:  # TODO Replace with the specific exception you expect from get_knowledge_graph_id_from_cp_id
            self.logger.warning(f"No existing KG found for counterparty ID {counterparty_id}. Creating a new KG.")

            # Logic for creating a new knowledge graph (KG)
            # new_kg_id = create_knowledge_graph_for_cp_id(counterparty_id)
            # self.logger.info(f"Created new KG with ID {new_kg_id} for counterparty ID {counterparty_id}")
            self.logger.warning("create_knowledge_graph_for_cp_id() has not been defined")
            return "dummy-value"

        except Exception as e:  # Generic exception handling for unexpected errors
            self.logger.error(f"Unexpected error occurred while processing counterparty ID {counterparty_id}: {e}",
                         exc_info=True)
            # Optionally, re-raise the exception if it should propagate up
            raise e

    #
    def internalize(self, raw_text, document_type, counterparty_id, expects_response):

        kg_id = self._get_knowledge_graph_id(counterparty_id)

        semantic_blocks = self.itext2g_interface.build_semantic_blocks(raw_text=raw_text, document_type=document_type)

        kg = self.itext2g_interface.build_knowledge_graph(semantic_blocks=semantic_blocks)

        ## Add Graph Integrator logic here


