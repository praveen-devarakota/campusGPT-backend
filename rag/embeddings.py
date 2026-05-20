from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = None


def get_embedding_model():

    global embedding_model

    if embedding_model is None:

        print("Loading lightweight embedding model...")

        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"
        )

    return embedding_model