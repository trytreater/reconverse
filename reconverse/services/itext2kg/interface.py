from xml.dom import NotFoundErr
from itext2kg.documents_distiller import DocumentsDistiller
from itext2kg import iText2KG
from .ie_queries import email_query
from.custom_schemas import Email
from typing import List
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import os


class iText2KGInterface:
    accepted_document_types = {
        "email": (Email, email_query),
    }

    def __init__(self, server):
        self.server = server
        self._set_llm()
        self._set_embeddings_model()
        self._instantiate_document_distiller()
        self._instantiate_itext2kg()

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

    def _instantiate_document_distiller(self) -> None:
        self.server.logger.info("\t Instantiating iText2KG Module 1: Document Distiller...")
        self.document_distiller = DocumentsDistiller(self.llm)
        self.server.logger.info("\t\t⤷ Done.")

    def _instantiate_itext2kg(self) -> None:
        self.server.logger.info(
            "\t Instantiating iText2KG Modules 2, 3: Incr. Entity Extractor, Incr. Relation Extractor")
        self.itext2kg = iText2KG(llm_model=self.llm, embeddings_model=self.embeddings_model)
        self.server.logger.info("\t\t⤷ Done.")

    def build_semantic_blocks(self, raw_text: str, document_type: str) -> List[str]:
        if document_type not in self.accepted_document_types:
            raise NotFoundErr
        else:
            schema = self.accepted_document_types[document_type][0]
            query  = self.accepted_document_types[document_type][1]
            distilled_document = self.document_distiller.distill(
                documents=[raw_text],
                IE_query=query,
                output_data_structure=schema)

            semantic_blocks = [f"{key} - {value}".replace("{", "[").replace("}", "]")
                               for key, value in distilled_document.items() if value !=[] and value != ""  and value is not None]

        return semantic_blocks

    def build_knowledge_graph(self, semantic_blocks, ent_threshold=0.6, rel_threshold=0.6): #todo add typing
        return self.itext2kg.build_graph(sections=[semantic_blocks],
                                         ent_threshold=ent_threshold,
                                         rel_threshold=rel_threshold)
