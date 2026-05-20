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
        n_results=10
    )

    filtered_documents = []
    filtered_metadatas = []
    filtered_distances = []

    if results["documents"]:

        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        query_lower = query.lower()

        for doc, meta, distance in zip(
            docs,
            metas,
            distances
        ):

            doc_lower = doc.lower()

            subject_name = meta.get(
                "subject_name",
                ""
            ).lower()

            # =========================================
            # STRICT FILTERING
            # =========================================

            keyword_match = any(
                word in doc_lower
                or word in subject_name
                for word in query_lower.split()
            )

            if (
                distance < 35 and
                keyword_match
            ):

                filtered_documents.append(doc)

                filtered_metadatas.append(meta)

                filtered_distances.append(distance)

        # =========================================
        # DEBUG RESULTS
        # =========================================

        print("\n========== RETRIEVAL RESULTS ==========\n")

        for meta, distance in zip(
            filtered_metadatas,
            filtered_distances
        ):

            print(meta)

            print("Distance:", distance)

            print("--------------------------------")

    return {
        "documents": [filtered_documents],
        "metadatas": [filtered_metadatas],
        "distances": [filtered_distances]
    }