import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
load_dotenv("secrets.env")

API_KEY = os.getenv("API_KEY")
secret = os.getenv("my_secret")
genai.configure(api_key=API_KEY)

def get_answer_from_llm(quiz_text, is_pdf_data=False, is_html_data=False):
    system_prompt = f"""
    You are an expert data analysis agent. Your job is to parse a quiz question
    and return a structured JSON object detailing the *exact* steps to solve it.
    
    Base JSON schema:
    {{
      "submission_url": "url to post the answer to",
      "payload": {{
        "email": "24f2007597@ds.study.iitm.ac.in",
        "secret": "{secret}",
        "answer": "the final answer",
        "tools": null,
        "question": null
      }}
    }}

    Special cases:
    1. For PDF parsing:
       - Set "tools": "pdf_parser"
       - Set "answer": "<pdf_url>"
       - Set "question": "specific parsing instructions"
       
    2. For web scraping:
       - Set "tools": "web_scraper"
       - Set "answer": "<target_url>"
       - Set "question": "specific scraping instructions"

    3. For data analysis:
       - Set "tools": "data_analysis"
       - Set "answer": null
       - Set "question": "specific data analysis instructions"

    Rules:
    - If {is_pdf_data} is true, treat input as PDF-extracted text with pages separated by blank lines
    - If {is_html_data} is true, treat input as raw HTML content
    - Return ONLY valid JSON - no additional text
    - Use null for missing/unknown values
    - Always include submission_url and basic payload fields
    - Include tools and question ONLY when special processing needed
    """

    prompt = f"Here is the quiz text:\n\n{quiz_text}"

    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash', # Fast and good at JSON
        system_instruction=system_prompt,
        generation_config={"response_mime_type": "application/json"} # Enforce JSON output!
    )
    
    print("--- 🧠 Calling Gemini API... ---")

    try:
        response = model.generate_content(prompt)
        response_text = response.text
        
        print("--- ✅ LLM Response (Raw Text) ---")
        print(response_text)
        
        # --- Parse the JSON response ---
        json_plan = json.loads(response_text)
        
        return json_plan

    except Exception as e:
        print(f"--- ❌ Error calling LLM or parsing JSON ---")
        print(f"Error: {e}")

'''
mock_quiz_text = """
Q901. Analyze the following sales data (in CSV format):
id,name,sales
1,Alice,150
2,Bob,200
3,Charlie,100

What is the total sum of the "sales" column?

Post your answer to https://example.com/submit-q901 with this JSON payload:

<pre>
{
  "email": "your-email",
  "secret": "your secret",
  "answer": 450 // the correct answer
}
</pre>
"""

if __name__ == "__main__":
    ans = get_answer_from_llm(mock_quiz_text)
    
    if ans:
        print("\n--- ✅ Success!")
        # Use json.dumps for pretty printing the dictionary
        print(json.dumps(ans, indent=2))
        
        # You can now access parts of the plan:
        print(f"\nSubmit URL: {ans.get('submission_url')}")
        print(f"Answer: {ans.get('payload', {}).get('answer')}")
    else:
        print("\n--- ❌ Failure! No answer was generated. ---")
'''