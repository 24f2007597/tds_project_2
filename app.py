from flask import Flask, jsonify, request
import os
import threading
from dotenv import load_dotenv
import get_quiz_content
import get_ans_from_llm
import submit_answer
load_dotenv("secrets.env")

app = Flask(__name__)

def run_quiz_chain(url):
    current_url = url
    try: 
        while current_url:
            quiz_content = get_quiz_content.get_quiz_content(current_url)
            llm_ans = get_ans_from_llm.get_answer_from_llm(quiz_content)

            if llm_ans:
                submit_url = llm_ans.get('submission_url', None)
                answer_value = llm_ans.get('payload', {}).get('answer', None)

                try:
                    response = submit_answer.submit_answer(submit_url, answer_value)
                    print(f"Submitted answer. Server response: {response}")
                    current_url = response.get('url', None)
                except Exception as e:
                    print(f"Error submitting answer: {e}")
                    break

        print("Quiz chain completed.")      
    except Exception as e:
        print(f"Error in quiz chain: {e}")

@app.route('/quiz-task', methods=['POST'])
def quiz_task():
    data = request.get_json()
    secret = data.get('secret')
    email = data.get('email')
    url = data.get('url')
    print(email, url)
    if secret != os.getenv("my_secret"):
        return jsonify({'error': 'Forbidden'}), 403
    
    worker = threading.Thread(target=run_quiz_chain, args=(url,))
    worker.start()

    return jsonify({'message': 'Task started successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
