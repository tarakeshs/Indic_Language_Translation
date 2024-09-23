from flask import Blueprint, request, jsonify
from app.models.google_translate import translate_with_google

main = Blueprint('main', __name__)

@main.route('/translate', methods=['POST'])
def translate_route():
    data = request.json
    text = data.get('text')  # Get the original text
    target_language = data.get('target_language')  # Get the target language
    model_flag = data.get('model')  # Use this flag to switch between models

    if not text or not target_language or not model_flag:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        if model_flag == 'google':
            # Call the logic from google_translate.py
            translation_result = translate_with_google(text, target_language)
        else:
            return jsonify({"error": "Invalid model flag"}), 400

        # Return the response based on the chosen model's result
        return jsonify(translation_result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
