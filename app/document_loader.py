from typing import List
from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader,
    TextLoader
)

class DocumentLoader:
    """Handles loading of different document types"""
    
    SUPPORTED_EXTENSIONS = {
        '.pdf': PyPDFLoader,
        '.docx': Docx2txtLoader,
        '.xlsx': UnstructuredExcelLoader,
        '.txt': TextLoader
    }

    @classmethod
    def load_documents(cls, directory: str) -> List:
        """Load all supported documents from a directory"""
        documents = []
        directory_path = Path(directory)
        
        for file_path in directory_path.glob('**/*'):
            if file_path.suffix.lower() in cls.SUPPORTED_EXTENSIONS:
                loader = cls.SUPPORTED_EXTENSIONS[file_path.suffix.lower()](str(file_path))
                documents.extend(loader.load())
                
        return documents 