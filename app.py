import pytesseract
import subprocess
import numpy as np
import streamlit as st
from PIL import Image
import re

# Hardcode the Tesseract path for deployment
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update this if your path is different

# Check if Tesseract is installed
try:
    output = subprocess.check_output(["tesseract", "--version"])
    print("Tesseract version:", output.decode())
except Exception as e:
    print("Tesseract not found:", str(e))
    st.error("Tesseract is not installed or not found in the specified path.")

def perform_ocr(image):
    """Convert image to grayscale and perform OCR to extract text."""
    gray_image = image.convert('L')  # Convert to grayscale using PIL
    text = pytesseract.image_to_string(gray_image, lang='hin+eng')
    return text

def search_first_keyword_in_text(text, keyword):
    """Search for the first occurrence of the keyword in the text."""
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    match = pattern.search(text)
    if match:
        return f"Keyword '{keyword}' found at position {match.start()}."
    else:
        return f"Keyword '{keyword}' not found in the text."

def main():
    st.title("OCR and Keyword Search Application")

    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        # Display the uploaded image
        st.image(image, caption='Uploaded Image', use_column_width=True)

        keyword = st.text_input("Enter Keyword to Search:")

        if st.button("Search"):
            # Perform OCR and keyword search
            extracted_text = perform_ocr(image)
            search_result = search_first_keyword_in_text(extracted_text, keyword)

            # Display results
            st.subheader("Extracted Text:")
            st.write(extracted_text)
            st.markdown(search_result, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
