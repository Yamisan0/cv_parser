# CV Parser

## Description
CV Parser is a FastAPI-based application designed to extract and analyze information from CVs (resumes). The project supports both structured and unstructured formats and uses Optical Character Recognition (OCR) to handle cases where the CV is not machine-readable. Additionally, it provides functionality for skill extraction and user management.

---

## Features

- **PDF and Image Parsing**: Extracts text from both PDF and image-based CVs using tools like `pdfminer` and `pytesseract`.
- **OCR Support**: Leverages Tesseract OCR to process image-based PDFs and other image formats.
- **Skill Extraction**: Identifies technical skills listed in CVs using fuzzy matching.
- **User Authentication**: Includes a user authentication system with JWT for secure access.
- **CRUD Operations**: Enables users to upload and manage CVs.

---

## Tech Stack

- **Backend Framework**: FastAPI
- **Frontend Framework**: NextJS
- **Database**: PostgreSQL (managed using SQLAlchemy)
- **OCR Tools**: Tesseract, pdfminer, pdf2image
- **Dependency Management**: Pip, Docker

---

## Installation

### Using Docker Compose

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your_username/cv-parser.git
   cd cv-parser
   ```

2. **Set up environment variables**:
   Create a `.env` file with the following content:
   ```env
   DB_URL=postgresql://<username>:<password>@postgres:5432/<database>
   SECRET_KEY=<your_secret_key>
   UPLOAD_DIRECTORY=/uploads
   ```

3. **Start the services**:
   Run the following command to build and start the services:
   ```bash
   docker-compose up --build
   ```

4. **Access the services**:
   - **Frontend**: [http://localhost:3000](http://localhost:3000)
   - **Backend API**: [http://localhost:8000](http://localhost:8000)
   - **pgAdmin**: [http://localhost:5050](http://localhost:5050)

### Without Docker

1. **Install dependencies**:
   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

2. **Set up Tesseract OCR**:
   ```bash
   sh tesseract.sh
   ```

3. **Run the application**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

---

## Usage

1. **Endpoints**:
   - `/auth`: User authentication routes
   - `/cv`: CV upload and processing routes

2. **Upload a CV**:
   Send a POST request to `/cv` with the file attached.

3. **Extract Skills**:
   The system will analyze the uploaded CV and return a list of detected skills.

---

## Dependencies

- `fastapi`
- `uvicorn`
- `pydantic`
- `sqlalchemy`
- `pytesseract`
- `pdf2image`
- `pdfminer.six`
- `fuzzywuzzy`
- `python-Levenshtein`
- `python-dotenv`

---

## Acknowledgments

- **OCR Tools**: Tesseract OCR and pdfminer for their robust text extraction capabilities.
- **Skill Matching**: FuzzyWuzzy for efficient fuzzy matching.

