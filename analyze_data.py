import pandas as pd
import io
import requests
import os
from get_ans_from_llm import get_llm_generated_code

def get_file_as_string(data_url: str, timeout: int = 30) -> str:
    """
    Handles file://, local paths, and http:// URLs,
    downloads the file, and returns its content as a string.
    """
    print(f"--- 🛠️ Tool: get_file_as_string ---")
    print(f"URL: {data_url}")
    
    file_bytes = None
    
    if data_url.startswith("file://"):
        path = data_url[len("file://"):]
        path = path.lstrip('/') if path.startswith('/') and os.name == 'nt' else path
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Local file not found: {path}")
        with open(path, "rb") as f:
            file_bytes = f.read()
            
    elif os.path.exists(data_url) and os.path.isfile(data_url):
        with open(data_url, "rb") as f:
            file_bytes = f.read()
            
    else:
        try:
            resp = requests.get(data_url, timeout=timeout)
            resp.raise_for_status() 
            file_bytes = resp.content
        except Exception as e:
            print(f"Error downloading {data_url}: {e}")
            return f"Error: {e}" 

    try:
        return file_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # Fallback for other encodings
        print("Warning: UTF-8 decode failed, falling back to latin-1.")
        return file_bytes.decode('latin-1') 
    except Exception as e:
        return f"Error decoding file: {e}"
    
def analyze_data(csv_data, analysis_prompt):
    """
    Loads CSV data into pandas and executes LLM-generated code
    to answer a question.
    """
    print(f"--- 🛠️ Tool: analyze_data ---")
    print(f"Prompt: {analysis_prompt}")
    
    try:
        # Load the CSV string into a pandas DataFrame
        df = pd.read_csv(io.StringIO(csv_data))
        
        # Get the code from the LLM
        # (This calls your get_llm_generated_code helper function)
        generated_code = get_llm_generated_code(df.head(), analysis_prompt)

        if not generated_code:
            return "Error: Could not generate analysis code."
            
        print(f"Code to run: {generated_code}")
        
        # Execute the generated pandas code
        local_scope = {'df': df}
        answer = eval(generated_code, {"pd": pd}, local_scope)
        
        print(f"Raw answer: {answer}")
        return str(answer) # Convert answer to string
        
    except Exception as e:
        print(f"Error during data analysis: {e}")
        return f"Error: {e}"