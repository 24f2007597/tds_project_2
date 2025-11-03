from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
import get_quiz_content
import get_ans_from_llm
load_dotenv("secrets.env")

app = Flask(__name__)

@app.route('/quiz-task', methods=['POST'])
def quiz_task():
    data = request.get_json()
    secret = data.get('secret')
    email = data.get('email')
    url = data.get('url')
    print(email, url)
    if secret != os.getenv("my_secret"):
        return jsonify({'error': 'Forbidden'}), 403
    
    try:
        return jsonify({'message': 'Task started successfully!'}), 200
    finally:
        quiz_content = get_quiz_content.get_quiz_content(url)
        answers = get_ans_from_llm.get_answer_from_llm(quiz_content)

if __name__ == '__main__':
    app.run(debug=True)
