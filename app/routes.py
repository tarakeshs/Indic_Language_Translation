from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify(message="Welcome to the Indic Language Translation API!")
