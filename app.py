import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_from_directory

from rag.retriever import retrieve_documents
from rag.llm import generate_response

from utils.attendance_parser import (
    load_attendance,
    attendance_data
)

from utils.attendance_query import (
    extract_roll_number,
    get_attendance
)

app = Flask(__name__)

CORS(app)


@app.route("/")
def home():

    return "CampusGPT Backend Running"


@app.route("/chat", methods=["POST"])
def chat():

    data = request.json

    query = data.get("question")

    # =========================================
    # ATTENDANCE FEATURE
    # =========================================

    attendance_keywords = [
        "attendance",
        "attendence",
        "attendace",
        "present",
        "percentage"
    ]

    if any(
        keyword in query.lower()
        for keyword in attendance_keywords
    ):

        roll_no = extract_roll_number(query)

        if roll_no:

            # =========================================
            # LOAD ATTENDANCE ONLY WHEN NEEDED
            # =========================================

            if not attendance_data:

                print("\nLoading attendance data...\n")

                load_attendance()

            student = get_attendance(roll_no)

            if student:

                return jsonify({
                    "answer": f"""
Attendance Details

Roll No: {roll_no}
Attendance: {student['attendance']}%
                    """,
                    "sources": [],
                    "links": []
                })

            else:

                return jsonify({
                    "answer": "Student attendance not found.",
                    "sources": [],
                    "links": []
                })

        else:

            return jsonify({
                "answer": "Please provide valid roll number.",
                "sources": [],
                "links": []
            })

    # =========================================
    # RAG RETRIEVAL
    # =========================================

    retrieved_docs = retrieve_documents(query)

    # =========================================
    # PRINT METADATA
    # =========================================

    print("\n========== METADATA ==========\n")

    if retrieved_docs["metadatas"]:

        metas = retrieved_docs["metadatas"][0]

        for i, meta in enumerate(metas):

            print(f"\n--- METADATA {i+1} ---\n")

            print(meta)

    print("\n==============================\n")

    # =========================================
    # GENERATE RESPONSE
    # =========================================

    answer, sources = generate_response(
        query,
        retrieved_docs
    )

    # =========================================
    # REMOVE DUPLICATE SOURCES
    # =========================================

    sources = list(set(sources))

    # =========================================
    # EXTRACT UNIQUE SOURCE LINKS
    # =========================================

    links = []

    seen_files = set()

    if retrieved_docs["metadatas"]:

        metas = retrieved_docs["metadatas"][0]

        for meta in metas:

            filename = meta.get("source", "")

            if (
                "source_link" in meta and
                filename not in seen_files
            ):

                seen_files.add(filename)

                links.append({
                    "filename": filename,
                    "subject": meta.get("subject_name", ""),
                    "college": meta.get("college", ""),
                    "link": meta.get("source_link", "")
                })

    # =========================================
    # RETURN RESPONSE
    # =========================================

    return jsonify({
        "answer": answer,
        "sources": sources,
        "links": links
    })


@app.route("/files/<filename>")
def get_file(filename):

    return send_from_directory(
        "data/question_papers",
        filename
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )