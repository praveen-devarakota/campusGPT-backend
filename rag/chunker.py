from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    final_chunks = []

    for doc in documents:

        chunks = splitter.split_text(doc["text"])

        for chunk in chunks:

            final_chunks.append({
                "chunk": chunk,
                "source": doc["source"]
            })

    return final_chunks