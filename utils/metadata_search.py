import json

METADATA_PATH = "metadata/metadata.json"

def search_metadata(query):

    with open(METADATA_PATH, "r") as file:

        metadata = json.load(file)

    query = query.lower()

    matched_results = []

    for item in metadata:

        searchable_text = (
            item.get("title", "") + " " +
            item.get("subject", "") + " " +
            item.get("semester", "") + " " +
            item.get("regulation", "") + " " +
            item.get("type", "")
        ).lower()

        matched_count = 0

        for word in query.split():

            if word in searchable_text:
                matched_count += 1

        if matched_count >= 2:
            matched_results.append(item)

    return matched_results