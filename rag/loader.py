import fitz
import pytesseract
from PIL import Image
import io
import os
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

DATA_PATH = "data"

def load_documents():

    documents = []

    for root, dirs, files in os.walk(DATA_PATH):

        for file in files:

            if file.endswith(".pdf"):

                file_path = os.path.join(root, file)

                pdf = fitz.open(file_path)

                full_text = ""

                print(f"\nProcessing: {file}")

                for page_num in range(len(pdf)):

                    page = pdf[page_num]

                    # Convert page to image
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

                    img_bytes = pix.tobytes("png")

                    image = Image.open(
                        io.BytesIO(img_bytes)
                    )

                    # OCR extraction
                    text = pytesseract.image_to_string(image)

                    full_text += text

                documents.append({
                    "text": full_text,
                    "source": file
                })

    return documents