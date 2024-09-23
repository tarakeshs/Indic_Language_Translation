import os
import re
import requests
from dotenv import load_dotenv
from textblob import TextBlob
from flask import jsonify

# Load environment variables from .env file
load_dotenv()

# Retrieve the Google API key from environment variables
google_api_key = os.getenv('GOOGLE_API_KEY')

if not google_api_key:
    raise ValueError("Google API key is missing!")

def preprocess_text(text: str) -> str:
    """Preprocess the text by applying common cleaning steps and autocorrection."""
    print("Pre processing the given text:", text)
    try:
        # 1. Lowercase the text (optional)
        text = text.lower()
        
        # 2. Remove extra spaces, newlines, and tabs
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 3. Remove unwanted special characters (except important punctuation)
        text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
        
        # 4. Autocorrect the text using TextBlob
        blob = TextBlob(text)
        corrected_text = str(blob.correct())  # Apply autocorrect
        print("Pre processed text:",corrected_text)
        return corrected_text
    except Exception as e:
        # Return original text if autocorrect fails
        return text  

def translate_with_google_preprocessed(text, target_language):
    """Translates the given preprocessed text to the target language using Google Translate API."""
    url = f"https://translation.googleapis.com/language/translate/v2"
    params = {
        'q': text,
        'target': target_language,
        'key': google_api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an error for bad responses
        data = response.json()
        return data['data']['translations'][0]['translatedText']
    except requests.exceptions.RequestException as e:
        raise Exception(f"Google Translate API Error: {str(e)}")


def translate_with_google(text, target_language):
    """Preprocess, autocorrect, and translate text."""
    try:
        # Step 1: Preprocess and autocorrect the text
        preprocessed_text = preprocess_text(text)

        # Step 2: Translate the preprocessed text
        translated_text = translate_with_google_preprocessed(preprocessed_text, target_language)

        # Return the original, preprocessed, and translated text in a dictionary
        return {
            "original_text": text,
            "preprocessed_text": preprocessed_text,
            "translated_text": translated_text
        }

    except Exception as e:
        raise Exception(f"Translation Error: {str(e)}")
