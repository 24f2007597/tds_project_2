import requests
import json
import os
from dotenv import load_dotenv
load_dotenv("secrets.env")

my_secret = os.getenv("my_secret")

def submit_answer(submit_url, answer):
    """
    Submit an answer to the specified URL endpoint.
    
    Args:
        submit_url (str): The URL endpoint to submit to
        answer (str): The answer to submit
        
    Returns:
        dict: The response from the server
    """
    headers = {
        'Content-Type': 'application/json'
    }
    
    payload = {
        'email': '24f2007597@ds.study.iitm.ac.in',
        'secret': my_secret,
        'answer': answer
    }
    
    try:
        response = requests.post(
            submit_url,
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to submit answer: {str(e)}")
    
test_submit_url = "https://webhook.site/a46b21ac-4380-46a1-b71f-2ea227b0739e"
submit_answer(test_submit_url, "450")