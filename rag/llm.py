from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_response(query, retrieved_docs):

    context = ""

    sources = set()

    docs = retrieved_docs["documents"][0]
    metas = retrieved_docs["metadatas"][0]

    for doc, meta in zip(docs, metas):

        source = meta.get("source", "Unknown")

        context += f"""
SOURCE FILE: {source}

CONTENT:
{doc}

====================
"""

        sources.add(source)

    if len(context.strip()) < 50:

        return (
            "No relevant college documents found.",
            []
        )

    prompt = f"""
You are CampusGPT.

ONLY answer using the retrieved college documents.

DO NOT use external knowledge.
DO NOT hallucinate filenames.

USER QUERY:
{query}

RETRIEVED DOCUMENTS:
{context}

INSTRUCTIONS:
- Mention ONLY actual source PDF filenames
- Identify relevant papers
- Summarize briefly
- Keep concise

ANSWER:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    return answer, list(sources)