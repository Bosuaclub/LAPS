"""
RAG Knowledge Base Module

Uses LangChain and ChromaDB to build a knowledge base from advertising documents.
Extracts campaign strategies and parameter spaces for optimization.
"""

import os
from typing import List, Dict, Any, Optional
from pathlib import Path

from loguru import logger
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate

from faosim.core.schemas import ParameterSpace, KnowledgeBaseDocument


class RAGKnowledgeBase:
    """
    RAG-based Knowledge Base for Facebook Ads strategies.

    Loads documents about ad optimization techniques and provides
    intelligent retrieval for parameter generation.
    """

    def __init__(
        self,
        persist_directory: str = "./data/chroma_db",
        embedding_model: str = "text-embedding-ada-002",
        collection_name: str = "fb_ads_knowledge",
    ):
        """
        Initialize RAG Knowledge Base.

        Args:
            persist_directory: Directory to persist ChromaDB
            embedding_model: OpenAI embedding model name
            collection_name: ChromaDB collection name
        """
        self.persist_directory = persist_directory
        self.embedding_model = embedding_model
        self.collection_name = collection_name

        logger.info(f"Initializing RAG Knowledge Base at {persist_directory}")

        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(model=embedding_model)

        # Initialize or load ChromaDB
        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None

        # Create persist directory if not exists
        Path(persist_directory).mkdir(parents=True, exist_ok=True)

    def load_documents(self, document_paths: List[str]) -> List[KnowledgeBaseDocument]:
        """
        Load documents from various formats (PDF, DOCX, TXT).

        Args:
            document_paths: List of file paths to load

        Returns:
            List of parsed documents
        """
        logger.info(f"Loading {len(document_paths)} documents...")
        documents = []

        for doc_path in document_paths:
            try:
                file_extension = Path(doc_path).suffix.lower()

                if file_extension == ".pdf":
                    loader = PyPDFLoader(doc_path)
                elif file_extension in [".docx", ".doc"]:
                    loader = UnstructuredWordDocumentLoader(doc_path)
                elif file_extension == ".txt":
                    loader = TextLoader(doc_path)
                else:
                    logger.warning(f"Unsupported file format: {doc_path}")
                    continue

                docs = loader.load()
                logger.info(f"Loaded {len(docs)} pages from {doc_path}")
                documents.extend(docs)

            except Exception as e:
                logger.error(f"Error loading {doc_path}: {e}")

        return documents

    def build_knowledge_base(
        self,
        document_paths: List[str],
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:
        """
        Build the knowledge base from documents.

        Args:
            document_paths: Paths to knowledge documents
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        logger.info("Building knowledge base...")

        # Load documents
        documents = self.load_documents(document_paths)

        if not documents:
            logger.warning("No documents loaded. Knowledge base will be empty.")
            return

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        splits = text_splitter.split_documents(documents)
        logger.info(f"Split documents into {len(splits)} chunks")

        # Create or update vector store
        if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
            logger.info("Loading existing vector store...")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name=self.collection_name,
            )
        else:
            logger.info("Creating new vector store...")
            self.vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings,
                persist_directory=self.persist_directory,
                collection_name=self.collection_name,
            )

        # Create retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5},
        )

        logger.info("Knowledge base built successfully")

    def setup_qa_chain(self) -> None:
        """Set up the QA chain for querying the knowledge base."""
        if self.vectorstore is None:
            raise ValueError("Knowledge base not built. Call build_knowledge_base first.")

        # Create custom prompt template
        template = """Use the following pieces of context about Facebook Ads optimization to answer the question.
If you don't know the answer, just say you don't know. Don't make up an answer.

Context: {context}

Question: {question}

Answer in a structured format that can be parsed as JSON when requested."""

        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"],
        )

        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=OpenAI(temperature=0),
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": prompt},
        )

        logger.info("QA chain initialized")

    def query(self, question: str) -> str:
        """
        Query the knowledge base.

        Args:
            question: Question to ask

        Returns:
            Answer from the knowledge base
        """
        if self.qa_chain is None:
            self.setup_qa_chain()

        logger.debug(f"Querying: {question}")
        result = self.qa_chain.run(question)
        return result

    def extract_parameter_space(self) -> ParameterSpace:
        """
        Extract the parameter space for campaign optimization from knowledge base.

        Returns:
            ParameterSpace object with extracted strategies
        """
        logger.info("Extracting parameter space from knowledge base...")

        # Query for different aspects
        targeting_query = """
        List all audience targeting strategies mentioned in the documents.
        Include age ranges, gender targeting, interest categories, and geographic targeting options.
        Format as JSON.
        """

        creative_query = """
        List all ad creative formats and best practices mentioned.
        Include image formats, video formats, carousel, collection ads, etc.
        Format as JSON.
        """

        bidding_query = """
        List all bidding strategies and optimization goals mentioned.
        Include bid types, optimization goals, and budget recommendations.
        Format as JSON.
        """

        placement_query = """
        List all available ad placements and combinations mentioned.
        Include Facebook feed, Instagram, Stories, Messenger, Audience Network.
        Format as JSON.
        """

        try:
            # Extract strategies (in real implementation, would parse JSON responses)
            targeting_strategies = self._parse_targeting_strategies(
                self.query(targeting_query)
            )
            creative_formats = self._parse_creative_formats(self.query(creative_query))
            bidding_strategies = self._parse_bidding_strategies(self.query(bidding_query))
            placement_combinations = self._parse_placements(self.query(placement_query))

            parameter_space = ParameterSpace(
                targeting_strategies=targeting_strategies,
                creative_formats=creative_formats,
                bidding_strategies=bidding_strategies,
                placement_combinations=placement_combinations,
                budget_ranges={"min": 10.0, "max": 1000.0, "recommended": 100.0},
            )

            logger.info("Parameter space extracted successfully")
            return parameter_space

        except Exception as e:
            logger.error(f"Error extracting parameter space: {e}")
            # Return default parameter space
            return self._get_default_parameter_space()

    def _parse_targeting_strategies(self, response: str) -> List[Dict[str, Any]]:
        """Parse targeting strategies from LLM response."""
        # Simplified parser - in production, use proper JSON parsing
        return [
            {
                "name": "Broad Targeting",
                "age_min": 18,
                "age_max": 65,
                "genders": ["all"],
                "locations": ["US", "CA", "GB"],
            },
            {
                "name": "Young Adults",
                "age_min": 18,
                "age_max": 34,
                "genders": ["all"],
                "locations": ["US"],
            },
            {
                "name": "Middle Age",
                "age_min": 35,
                "age_max": 54,
                "genders": ["all"],
                "locations": ["US"],
            },
        ]

    def _parse_creative_formats(self, response: str) -> List[str]:
        """Parse creative formats from LLM response."""
        return ["single_image", "carousel", "video", "collection"]

    def _parse_bidding_strategies(self, response: str) -> List[str]:
        """Parse bidding strategies from LLM response."""
        return [
            "LOWEST_COST_WITHOUT_CAP",
            "LOWEST_COST_WITH_BID_CAP",
            "COST_CAP",
            "LOWEST_COST_WITH_MIN_ROAS",
        ]

    def _parse_placements(self, response: str) -> List[List[str]]:
        """Parse placement combinations from LLM response."""
        return [
            ["facebook_feed"],
            ["instagram_feed"],
            ["facebook_feed", "instagram_feed"],
            ["facebook_feed", "instagram_feed", "facebook_stories"],
            ["facebook_feed", "instagram_feed", "facebook_stories", "instagram_stories"],
        ]

    def _get_default_parameter_space(self) -> ParameterSpace:
        """Get default parameter space if knowledge base is empty."""
        logger.warning("Using default parameter space")
        return ParameterSpace(
            targeting_strategies=[
                {"name": "Default", "age_min": 18, "age_max": 65, "genders": ["all"]}
            ],
            creative_formats=["single_image", "carousel", "video"],
            bidding_strategies=["LOWEST_COST_WITHOUT_CAP", "COST_CAP"],
            placement_combinations=[
                ["facebook_feed", "instagram_feed"],
                ["facebook_feed", "instagram_feed", "facebook_stories", "instagram_stories"],
            ],
            budget_ranges={"min": 10.0, "max": 500.0, "recommended": 50.0},
        )

    def get_recommendations(self, context: str) -> str:
        """
        Get recommendations based on context.

        Args:
            context: Context for recommendations

        Returns:
            Recommendations from knowledge base
        """
        question = f"Based on the following context, what are the best practices? {context}"
        return self.query(question)
