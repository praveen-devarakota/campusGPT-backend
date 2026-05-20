from chromadb import PersistentClient
from rag.embeddings import get_embedding_model

CHROMA_PATH = "chroma_db"


def retrieve_documents(query):

    client = PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_collection(
        name="campusgpt"
    )

    embedding_model = get_embedding_model()

    query_embedding = embedding_model.embed_query(
        query
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    filtered_documents = []
    filtered_metadatas = []
    filtered_distances = []

    if results["documents"]:

        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, meta, distance in zip(
            docs,
            metas,
            distances
        ):

            if distance < 1.5:

                filtered_documents.append(doc)

                filtered_metadatas.append(meta)

                filtered_distances.append(distance)

    return {
        "documents": [filtered_documents],
        "metadatas": [filtered_metadatas],
        "distances": [filtered_distances]
    }