📄 Document Verifier System

(Freelancing Project | Real-World Identity Verification Solution)

The Document Verifier System is an end-to-end OCR-based identity information extraction platform designed to automatically process uploaded document images and extract key personal details in a structured format.

Built with a FastAPI backend and a Streamlit frontend, this system demonstrates how modern AI-powered document processing can be transformed into a deployable, user-friendly verification solution.

🧩 Real-World Problem Addressed

Manual document verification is:

Time-consuming

Error-prone

Difficult to scale

Organizations dealing with onboarding, verification, or record digitization require automated, accurate, and fast document processing.
This system solves that problem by converting raw document images into structured identity data using OCR and intelligent parsing.

🚀 Key Features
📤 Document Upload

Supports PNG, JPG, JPEG formats

Secure upload handling via REST API

🔍 OCR-Based Text Extraction

Extracts raw text from document images

Handles real-world scanned and photographed documents

🧾 Automated Structured Field Extraction

The system intelligently parses OCR output to extract:

🧑 Name

📅 Date of Birth

🏠 Address

🌐 RESTful API

Built using FastAPI

Clean and scalable endpoints

Ready for integration with other systems

🖥️ Interactive Streamlit Interface

Two-panel layout for better UX:

Left Panel: Document upload & image preview

Right Panel: Extracted and parsed identity details

Real-time interaction with backend API

🔐 Deployment-Ready Backend

CORS-enabled for frontend integration

Modular and production-friendly structure

🛠️ Tech Stack
Backend

Python

FastAPI

OCR Engine

Tesseract / EasyOCR

REST API architecture

CORS middleware for frontend communication

Frontend

Streamlit

Requests (API communication)

Clean, minimal UI for non-technical users

🧠 System Workflow

User uploads a document image via Streamlit UI

Image is sent to FastAPI backend

OCR engine extracts raw text

Parsed logic extracts structured fields

🔮 Future Enhancements

Confidence scores for extracted fields

Support for multilingual documents

Face–text consistency checks

Database integration for verification history

Admin dashboard

📜 License

This project is developed as a freelancing solution.
Commercial reuse or redistribution requires permission from the author.

⭐ Reviewer Note

This repository is designed to showcase production-oriented thinking, not just OCR experimentation.
It reflects the ability to design, implement, integrate, and document a real-world verification system.

Results are returned and displayed in real time
