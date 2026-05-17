from rag.loader import load_documents

docs = load_documents()

print("\n==============================")
print("TOTAL DOCUMENTS LOADED:", len(docs))
print("==============================\n")

for doc in docs:

    print("\n===================================")
    print("SOURCE FILE:", doc["source"])
    print("===================================\n")

    text = doc["text"]

    if len(text.strip()) == 0:

        print("❌ NO TEXT EXTRACTED")

    else:

        print(text[:5000])

    print("\n===================================\n")