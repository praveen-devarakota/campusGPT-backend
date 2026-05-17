import re
import os


def extract_metadata(source):

    filename = os.path.basename(source)

    metadata = {

        "source": filename,

        "subject_code": "",

        "department": "",

        "semester": "",

        "subject_name": "",

        "college": "VRSEC",

        "source_link":
        f"https://vrsec.edu.in/questionpapers/{filename}"
    }

    # =========================================
    # SUBJECT CODE
    # =========================================

    code_match = re.search(
        r'(\d{2}[A-Z]{2}\d{4}[A-Z]?)',
        filename
    )

    if code_match:

        metadata["subject_code"] = code_match.group()

    # =========================================
    # DEPARTMENT
    # =========================================

    if "IT" in filename:

        metadata["department"] = "IT"

    # =========================================
    # SEMESTER
    # =========================================

    if filename.startswith("20"):

        metadata["semester"] = "7"

    # =========================================
    # SUBJECT NAMES
    # =========================================

    subject_map = {

        "20IT7301": "Deep Learning",

        "20IT7402A":
        "Software Testing and Automation",

        "20IT7402C":
        "Data Analytics",

        "20IT7403A":
        "Cloud Computing"
    }

    metadata["subject_name"] = subject_map.get(
        metadata["subject_code"],
        "Unknown"
    )

    return metadata