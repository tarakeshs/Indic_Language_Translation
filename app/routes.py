from flask import Blueprint, request, jsonify
from app.models import google_translate

main = Blueprint('main', __name__)

# Base route to check if the API is working
@main.route('/')
def home():
    return jsonify(message="Welcome to the Indic Language Translation API!")

# Translation route using Google Translate API by default
@main.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    target_language = data.get('target_language')

    if not text or not target_language:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        translated_text = google_translate.translate(text, target_language)
        return jsonify({"translated_text": translated_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
