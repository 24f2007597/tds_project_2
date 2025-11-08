from flask import Flask, jsonify, request
import os
import threading
from dotenv import load_dotenv
import get_quiz_content
import get_ans_from_llm
import submit_answer
import get_pdf_text
import scrape_website
from urllib.parse import urlparse
import analyze_data
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
                tools = llm_ans.get('payload', {}).get('tools', None)
                question_text = llm_ans.get('payload', {}).get('question', None)

                if tools == 'pdf_parser':
                    try:
                        pdf_text = get_pdf_text.get_pdf_text(answer_value)
                        print(f"Extracted PDF text")
                        answer_value = get_ans_from_llm.get_answer_from_llm(pdf_text, is_pdf_data=True, question_text=question_text).get('payload', {}).get('answer', None)
                    except Exception as e:
                        print(f"Error extracting PDF text: {e}")
                        break

                if tools == 'web_scraper':
                    try:
                        html_content = scrape_website.scrape_website(answer_value)
                        print(f"Extracted HTML content")
                        answer_value = get_ans_from_llm.get_answer_from_llm(html_content, is_html_data=True, question_text=question_text).get('payload', {}).get('answer', None)
                    except Exception as e:
                        print(f"Error extracting HTML content: {e}")
                        break
                
                if tools == 'data_analysis':
                    try:
                        data = answer_value
                        result = urlparse(answer_value)
                        if all([result.scheme, result.netloc, result.path]):
                            data = analyze_data.get_file_as_string(answer_value)
                        answer_value = analyze_data.analyze_data(data, question_text)

                    except Exception as e:
                        print(f"Error retrieving data for analysis: {e}")
                        break

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
