from chromadb import PersistentClient

CHROMA_PATH = "chroma_db"


def retrieve_documents(query):

    client = PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_collection(
        name="campusgpt"
    )

    # =========================================
    # DIRECT TEXT QUERY
    # =========================================

    results = collection.query(
        query_texts=[query],
        n_results=10
    )

    # =========================================
    # FILTER LOW QUALITY RESULTS
    # =========================================

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

            # Smaller distance = better match

            if distance < 1.2:

                filtered_documents.append(doc)

                filtered_metadatas.append(meta)

                filtered_distances.append(distance)

    return {
        "documents": [filtered_documents],
        "metadatas": [filtered_metadatas],
        "distances": [filtered_distances]
    }