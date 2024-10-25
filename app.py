from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the chatbot model from the data folder
CHATBOT_MODEL_PATH = os.path.join('model', 'chatbot_model.pkl')
chatbot_model = joblib.load(CHATBOT_MODEL_PATH)

@app.route('/')
def index():
    # Render the main page using the templates folder
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.form.get('question', '')
    if not user_question:
        return jsonify({"error": "No question provided."}), 400
    
    # Predict the answer
    predicted_answer = chatbot_model.predict([user_question])[0]
    return jsonify({"answer": predicted_answer})

# 1. Chatbot Endpoint
@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    data = request.get_json()
    user_message = data.get('message', '')

    # Process user_message through chatbot model
    bot_response = chatbot_model_response(user_message)
    return jsonify({'response': bot_response})

def chatbot_model_response(user_message):
    # Assuming your model has a predict method
    response = chatbot_model.predict([user_message])
    return response[0]

# 2. Tax Filing Bot Endpoint (currently placeholder)
@app.route('/generate-ais', methods=['POST'])
def generate_ais():
    data = request.files.get('bank_statement')
    if data is None:
        return jsonify({'error': 'No bank statement uploaded'}), 400

    # Placeholder response for tax model processing
    # Uncomment and implement once the tax model is ready
    # ais_report = tax_model_response(data)
    return jsonify({'AIS_report': 'AIS report generation is currently disabled.'})

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)