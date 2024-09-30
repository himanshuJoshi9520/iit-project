import streamlit as st
from PIL import Image
import pytesseract
import re

# Remove the tesseract_cmd setting, as it won't work on cloud platforms
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image, lang):
    text = pytesseract.image_to_string(image, lang=lang)
    return text

def highlight_keywords(text, keyword):
    highlighted_text = re.sub(rf'(\b{keyword}\b)', r'<mark>\1</mark>', text, flags=re.IGNORECASE)
    return highlighted_text

st.set_page_config(page_title="Pixel OCR Extractor", layout="wide")

st.markdown(
    """
    <style>
    /* Main app background */
    .stApp {
        background-color: #1a1a2e;  /* Dark background */
        color: white;  /* Text color */
    }

    /* Title and header customization */
    h1, h2, h3 {
        text-align: center;
        color: #ffffff;  /* White text */
        font-family: 'Verdana', sans-serif;
    }

    /* Center content in the page */
    .block-container {
        padding: 2rem;
    }

    /* Style for the buttons */
    .stButton>button {
        background-color: #4CAF50; /* Green button */
        color: white;
        border: none;
        padding: 10px 24px;
        font-size: 16px;
        margin: 10px;
        border-radius: 12px;
        cursor: pointer;
    }

    /* Style for file uploader */
    .file_uploader {
        display: block;
        margin-left: auto;
        margin-right: auto;
        padding: 20px;
        border: 2px solid #4CAF50;
        border-radius: 10px;
        background-color: #2f2f3f;
        text-align: center;
        color: #ffffff;
    }

    /* Highlight keywords in yellow */
    mark {
        background-color: yellow;
        font-weight: bold;
        padding: 3px;
    }

    /* Sidebar customization */
    .css-1d391kg {
        background-color: #1a1a2e;
    }

    /* Footer */
    footer {
        text-align: center;
        padding: 10px;
        font-size: 14px;
        background-color: #333;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("Pixel OCR & Text Extractor")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Upload an Image")
    uploaded_image = st.file_uploader("", type=["png", "jpg", "jpeg"])

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

with col2:
    # Language selection from the sidebar
    st.sidebar.header("Settings")
    language = st.sidebar.selectbox("Select OCR Language:", ["English", "Hindi", "Both"])
    lang_code = "eng"

    if language == "Hindi":
        lang_code = "hin"
    elif language == "Both":
        lang_code = "eng+hin"

    if uploaded_image:
        with st.spinner("Extracting text..."):
            extracted_text = extract_text_from_image(image, lang_code)
        st.subheader("📄 Extracted Text")
        st.write(extracted_text)

        search_query = st.text_input("🔍 Enter a keyword to search:")

        if search_query:
            matches = re.findall(rf'\b{search_query}\b', extracted_text, re.IGNORECASE)
            if matches:
                st.success(f"Keyword '{search_query}' found {len(matches)} times!")

                highlighted_text = highlight_keywords(extracted_text, search_query)
                st.markdown(f"### Text with highlighted keyword:")
                st.markdown(f"<div style='padding:10px;background-color:#f0f0f0;'>{highlighted_text}</div>",
                            unsafe_allow_html=True)
            else:
                st.warning(f"No matches found for '{search_query}'.")
    else:
        st.info("Please upload an image to start the OCR process.")

# Footer section
st.markdown("---")
st.markdown("<footer>Developed with Streamlit ❤️ | Pixel Extractor</footer>", unsafe_allow_html=True)
