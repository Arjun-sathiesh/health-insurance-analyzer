# health-insurance-analyzer
Description
This Streamlit app allows users to securely log in, submit health insurance claims, and upload supporting PDF documents. It uses AI to analyze claims for validity, coverage eligibility, and fraud detection, providing decisions (Accepted/Rejected) with reasons for rejection if applicable.

Features
Login System: User authentication with credentials (admin/user).
Claim Submission: Input details like Policy Number, Patient Name, Hospital Name, Treatment, and Bill Amount.
File Upload: Upload PDF files for claim support.
AI Analysis: AI-powered claim analysis for decision-making (Accepted/Rejected).
Fraud Detection: Shows fraud detection probability (Low/High).
Technologies
Streamlit: Web app framework
pypdf: PDF text extraction
Google Generative AI: AI model for claim analysis
Python: Backend logic
Setup
Clone/download the repository.
Install dependencies:
nginx
Copy
pip install streamlit pypdf google-generativeai
Replace the API key with a valid one.
Run the app:
arduino
Copy
streamlit run app.py
Usage
Log in with admin/password123 or user/userpass.
Submit claims and upload PDFs.
View claim analysis and fraud detection results.
