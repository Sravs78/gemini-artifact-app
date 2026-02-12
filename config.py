"""
Configuration module for Gemini API setup
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def initialize_gemini():
    """
    Initialize Gemini 1.5 Flash API with the provided API key
    
    Returns:
        str: Confirmation message
        
    Raises:
        ValueError: If API key is not set
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not set. Please add it to your .env file.")
    
    genai.configure(api_key=GEMINI_API_KEY)
    return "Gemini API initialized successfully"

def get_gemini_model():
    """
    Get the Gemini 1.5 Flash model
    
    Returns:
        GenerativeModel: The Gemini 1.5 Flash model instance
    """
    return genai.GenerativeModel('gemini-1.5-flash')