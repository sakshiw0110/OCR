import pytesseract
import cv2
import numpy as np
import streamlit as st
import re

# Set the path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def perform_ocr(image):
    """Convert image to grayscale and perform OCR to extract text."""
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_image, lang='hin+eng')
    return text

def search_first_keyword_in_text(text, keyword):
    """Search for the first sentence containing the keyword in the extracted text."""
    if keyword:
        text = text.replace('\n', ' ')
        sentences = re.split(r'(?<=[.!?]) +', text)
        for sentence in sentences:
            if re.search(keyword, sentence, re.IGNORECASE):
                highlighted_sentence = re.sub(f'({re.escape(keyword)})', r'<b>\1</b>', sentence, flags=re.IGNORECASE)
                return highlighted_sentence.strip()
        return "No matching sentence found."
    else:
        return "Please enter a keyword to search."

def main():
    """Main function to run the Streamlit application."""
    st.title("OCR and Keyword Search Application")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    keyword = st.text_input("Enter keyword to search")

    if uploaded_file is not None and keyword:
        # Read the image file
        image = np.array(cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR))
        
        # Perform OCR and keyword search
        extracted_text = perform_ocr(image)
        search_result = search_first_keyword_in_text(extracted_text, keyword)

        # Display results
        st.subheader("Extracted Text:")
        st.text_area("", extracted_text, height=200)
        st.subheader("Search Result (First Matching Sentence):")
        st.markdown(search_result, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
