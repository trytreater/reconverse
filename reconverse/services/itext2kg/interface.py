from xml.dom import NotFoundErr
from itext2kg.documents_distiller import DocumentsDistiller, CV
from itext2kg import iText2KG
from reconverse.server.reconverse import Reconverse
from .ie_queries import email_query
from.custom_schemas import Email
from typing import List


class iText2KGInterface:
    #stopgap
    accepted_document_types = {
        "email": (Email, email_query),
    }

    def __init__(self, server: Reconverse):
        self.server = server
        self._instantiate_document_distiller()
        self._instantiate_itext2kg()

    def _instantiate_document_distiller(self) -> None:
        self.server.logger.info("Instantiating iText2KG Module 1: Document Distiller...")
        self.document_distiller = DocumentsDistiller(self.server.llm)
        self.server.logger.info("\t Instantiated.")

    def _instantiate_itext2kg(self) -> None:
        self.server.logger.info(
            "Instantiating iText2KG Modules 2 through 4: Incremental Entity Extractor, Incremental Relation Extractor, Graph Integrator")
        self.itext2kg = iText2KG(llm_model=self.server.llm, embeddings_model=self.server.embeddings_model)
        self.server.logger.info("\t Instantiated.")

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

