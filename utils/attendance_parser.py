import fitz
from PIL import Image
import io
import re
import os

# Tesseract path
import platform
import pytesseract

if platform.system() == "Windows":

    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ATTENDANCE_PDF = os.path.join(
    BASE_DIR,
    "data",
    "attendance",
    "attendance.pdf"
)

attendance_data = {}


def load_attendance():

    global attendance_data

    attendance_data = {}

    print("\nLoading Attendance PDF...\n")

    pdf = fitz.open(ATTENDANCE_PDF)

    full_text = ""

    # OCR extraction
    for page in pdf:

        pix = page.get_pixmap(
            matrix=fitz.Matrix(3, 3)
        )

        img_bytes = pix.tobytes("png")

        image = Image.open(
            io.BytesIO(img_bytes)
        )

        text = pytesseract.image_to_string(image)

        full_text += text + "\n"


    # Extract roll numbers
    roll_numbers = re.findall(
        r'238W1A\w+',
        full_text
    )


    # Extract percentages
    percentage_matches = re.findall(
        r'\b\d+\.\d+\b|\b\d{2}\b',
        full_text
    )


    # Last percentages in PDF
    final_percentages = percentage_matches[-4:]



    # Map correctly
    for i in range(
        min(len(roll_numbers), len(final_percentages))
    ):

        clean_roll = roll_numbers[i].strip().upper()
        attendance_data[clean_roll] = {
            "attendance": final_percentages[i]
        }

    print("\nAttendance Loaded Successfully\n")