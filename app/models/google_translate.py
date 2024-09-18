import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the Google API key from environment variables
google_api_key = os.getenv('GOOGLE_API_KEY')

if not google_api_key:
    raise ValueError("Google API key is missing!")

def translate(text, target_language):
    """Translates the given text to the target language using Google Translate REST API."""
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
