from chromadb import PersistentClient

from rag.loader import load_documents
from rag.chunker import chunk_documents
from rag.embeddings import get_embedding_model
from rag.metadata_extractor import extract_metadata

import uuid

CHROMA_PATH = "chroma_db"


def create_vectorstore():

    client = PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name="campusgpt"
    )

    embedding_model = get_embedding_model()

    documents = load_documents()

    chunks = chunk_documents(documents)

    for chunk_data in chunks:

        chunk = chunk_data["chunk"]

        source = chunk_data["source"]

        # =========================================
        # CREATE EMBEDDING
        # =========================================

        embedding = embedding_model.embed_query(
            chunk
        )

        # =========================================
        # EXTRACT METADATA
        # =========================================

        metadata = extract_metadata(source)

        # =========================================
        # STORE IN CHROMADB
        # =========================================

        collection.add(
            ids=[str(uuid.uuid4())],

            embeddings=[embedding],

            documents=[chunk],

            metadatas=[metadata]
        )

    print("Vector Database Created Successfully")