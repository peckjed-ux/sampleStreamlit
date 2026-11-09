# Streamlit & Gemini Playground Project

This project contains a fully commented Streamlit application demonstrating:
- Barcode/QR scanning from uploaded images (`pyzbar`)
- Gemini API integration with custom system instructions (`google-genai`)
- Streamlit layout, session state, interactive widgets, metrics, and data charts

## Setup Instructions for PyCharm

1. **Unzip** `streamlit_gemini_app.zip` into your desired project directory.
2. **Open in PyCharm**: Open PyCharm and select **File -> Open...**, then pick the project folder.
3. **Configure Environment Variables**:
   - Open `.env` in the project root.
   - Replace `your_actual_gemini_api_key_here` with your Gemini API key.
4. **Install Dependencies**:
   - Open the Terminal in PyCharm (`Alt + F12` or `Option + F12` on Mac).
   - Create a virtual environment if needed: `python -m venv venv`
   - Activate it and install requirements:
     ```bash
     pip install -r requirements.txt
     ```
   - *Note for Barcode scanning*: `pyzbar` requires system C libraries (`zbar`).
     - macOS: `brew install zbar`
     - Linux: `sudo apt-get install libzbar0`
5. **Run the Streamlit App**:
   - In PyCharm's built-in terminal, run:
     ```bash
     streamlit run app.py
     ```
