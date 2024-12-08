import fitz  # PyMuPDF
from pdfminer.high_level import extract_text
import pytesseract
from PIL import Image
from io import BytesIO
from sys import argv
from pdf2image import convert_from_path


class CvExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = ""

    def extract(self):
        if self.file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            self.extract_image()
        elif self.file_path.lower().endswith('.pdf'):
            self.extract_pdf()
        else:
            print("Format de fichier non pris en charge.")

    def extract_text_from_image_pdf(self):
        pages = convert_from_path(self.file_path)
        for page in pages:
            self.text += pytesseract.image_to_string(page)

    def extract_image(self):
            self.text = pytesseract.image_to_string(self.file_path)
    
    def extract_pdf(self):
        try:
            #print(len(self.text))
            self.text = extract_text(self.file_path)
            if len(self.text) < 700 or self.text.startswith("(cid:"):
                #print("PDF image-based détecté.")
                self.extract_text_from_image_pdf()
        except Exception as e:
            print(f"Erreur lors du parsing du PDF : {e}")
    
    def parse_pdf_image_based(self):
        pages = convert_from_path(self.file_path)
        extracted_text = ""
        for page in pages:
            extracted_text += pytesseract.image_to_string(page)
        return extracted_text

if __name__ == "__main__":
    file_path = argv[1]
    cv_parser = CvExtractor(file_path)
    cv_parser.extract()
    print(cv_parser.text)
