"""
Streamlit Application for Gemini Historical Artifact Description
Main application file that creates the web interface and orchestrates
the workflow between user input and Gemini model responses
"""

import streamlit as st
from config import initialize_gemini, get_gemini_model
from utils import input_image_setup, get_gemini_response, display_uploaded_image
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Gemini Historical Artifact Description App",
    page_icon="🏺",
    layout="centered"
)

# Custom CSS for better styling
st.markdown('''
    <style>
        .main {
            padding-top: 2rem;
        }
        .stButton > button {
            width: 100%;
            padding: 0.5rem;
            border-radius: 0.5rem;
        }
    </style>
''', unsafe_allow_html=True)

# Initialize session state for error handling
if "error_message" not in st.session_state:
    st.session_state.error_message = None

if "response_text" not in st.session_state:
    st.session_state.response_text = None

# Page Header
st.title("🏺 Gemini Historical Artifact Description App")
st.markdown("---")
st.markdown("Upload an image of a historical artifact and get an AI-generated description!")

try:
    # Initialize Gemini API
    initialize_gemini()
    model = get_gemini_model()
    
except ValueError as e:
    st.error(f"Configuration Error: {str(e)}")
    st.info("Please set the GEMINI_API_KEY environment variable in your .env file")
    st.stop()

# Main Application Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Input Prompt")
    # Input text from user
    input_prompt = st.text_input(
        "Describe what you want to know about the artifact:",
        placeholder="e.g., Analyze this historical artifact...",
        label_visibility="collapsed"
    )

with col2:
    st.subheader("🖼️ Upload Image")
    # File uploader for image
    uploaded_file = st.file_uploader(
        "Choose an image of an artifact...",
        type=["jpg", "jpeg", "png", "gif", "webp"],
        label_visibility="collapsed"
    )

st.markdown("---")

# Display uploaded image if available
if uploaded_file is not None:
    try:
        st.subheader("Preview")
        image = display_uploaded_image(uploaded_file)
        st.image(image, use_column_width=True)
    except Exception as e:
        st.error(f"Error displaying image: {str(e)}")

st.markdown("---")

# Generate button and response
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    generate_button = st.button("🚀 Generate Description", use_container_width=True)

# Handle generation
if generate_button:
    # Validate inputs
    if not input_prompt.strip():
        st.error("⚠️ Please enter a prompt to describe what you want to know about the artifact.")
    elif uploaded_file is None:
        st.error("⚠️ Please upload an image of the artifact.")
    else:
        try:
            with st.spinner("🔄 Generating description... This may take a moment."): 
                # Process image
                image_data = input_image_setup(uploaded_file)
                
                # Get response from Gemini
                response = get_gemini_response(input_prompt, image_data, model)
                
                # Store response in session state
                st.session_state.response_text = response
                st.session_state.error_message = None
                
        except FileNotFoundError:
            st.error("❌ No file uploaded. Please upload an image.")
        except Exception as e:
            error_msg = f"Error generating description: {str(e)}"
            st.error(f"❌ {error_msg}")
            st.session_state.error_message = error_msg

# Display response if available
if st.session_state.response_text:
    st.markdown("---")
    st.subheader("📄 Generated Description")
    
    # Display the response in a container
    with st.container(border=True):
        st.markdown(st.session_state.response_text)
    
    # Copy and export options
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📥 Download as Text",
            data=st.session_state.response_text,
            file_name="artifact_description.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        if st.button("🔄 Generate New Description", use_container_width=True):
            st.session_state.response_text = None
            st.rerun()

# Footer
st.markdown("---")
st.markdown('''
    <div style='text-align: center'>
        <p style='color: gray; font-size: 0.8rem;'>
            Powered by Google Gemini 1.5 Flash | Historical Artifact Analysis Tool
        </p>
    </div>
''', unsafe_allow_html=True)