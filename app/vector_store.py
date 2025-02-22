from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from typing import List
from langchain.schema import Document

class VectorStoreManager:
    """Manages FAISS vector store operations"""
    
    def __init__(self, persist_directory: str):
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None

    def initialize_store(self, documents: List[Document]):
        """Initialize vector store with documents"""
        self.vector_store = FAISS.from_documents(
            documents,
            self.embeddings
        )
        self.vector_store.save_local(self.persist_directory)

    def load_store(self):
        """Load existing vector store"""
        self.vector_store = FAISS.load_local(
            self.persist_directory,
            self.embeddings
        )

    def similarity_search(self, query: str, k: int = 4):
        """Perform similarity search"""
        return self.vector_store.similarity_search(query, k=k) 