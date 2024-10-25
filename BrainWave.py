import json5
import pandas as pd
from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import joblib

"""
# Step 1: Load JSON data
with open('data.json') as f:
    data = json5.load(f)

# Step 2: Prepare the dataset
questions = []
answers = []

for category in data.values():
    for qna in category.values():
        for item in qna:
            questions.append(item['question'])
            answers.append(item['answer'])

# Create a DataFrame
df = pd.DataFrame({'question': questions, 'answer': answers})

# Step 3: Train the model
X_train, X_test, y_train, y_test = train_test_split(df['question'], df['answer'], test_size=0.2, random_state=42)
model = make_pipeline(CountVectorizer(), LogisticRegression(max_iter=1000))
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, 'chatbot_model.pkl')
"""
# Step 4: Create Flask app
app = Flask(__name__)

# Load the trained model
model = joblib.load('chatbot_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.form.get('question', '')
    if not user_question:
        return jsonify({"error": "No question provided."}), 400
    
    # Predict the answer
    predicted_answer = model.predict([user_question])[0]
    return jsonify({"answer": predicted_answer})

if __name__ == '__main__':
    app.run(debug=True)
