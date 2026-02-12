import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import Part

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Create GenAI client
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Gemini Artifact App", layout="centered")
st.title("Gemini Artifact App")

# Image upload
st.markdown("### Upload an Image")
uploaded_file = st.file_uploader(
    "Drag and drop file here", type=["png", "jpg", "jpeg"]
)

# Prompt input
st.markdown("### Enter prompt for Gemini")
input_prompt = st.text_input(
    "Prompt", placeholder="Describe the artifact in the image"
)

if uploaded_file and input_prompt:
    st.image(uploaded_file, caption="Uploaded Image", width=600)
    image_bytes = uploaded_file.read()

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                Part.from_bytes(data=image_bytes, mime_type=uploaded_file.type),
                input_prompt
            ],
        )

        st.subheader("Gemini Response")
        st.write(response.text)

    except Exception as e:
        st.error(f"Error calling Gemini API: {e}")
