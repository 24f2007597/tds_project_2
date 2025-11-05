import requests
import io
import pdfplumber
import os

def get_pdf_text(url, timeout=30):
    """
    Download a PDF from `url` (http/https) or read a local PDF (file:// or path)
    and return all extracted text as a single string.

    Args:
        url (str): URL to the PDF file or local path (can start with file://).
        timeout (int): requests timeout in seconds for HTTP fetches.

    Returns:
        str: Extracted text (empty string if nothing found).

    Raises:
        requests.exceptions.RequestException on download errors.
        Exception on PDF parsing/extraction errors or missing local file.
    """
    # Handle local file URLs and plain local paths
    pdf_bytes = None
    if not url:
        raise ValueError("Empty URL/path supplied to get_pdf_text")

    if url.startswith("file://"):
        path = url[len("file://"):]
        path = path.lstrip('/') if path.startswith('/') and os.name == 'nt' else path
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Local PDF not found: {path}")
        with open(path, "rb") as f:
            pdf_bytes = f.read()
    elif os.path.exists(url) and os.path.isfile(url):
        # plain local path
        with open(url, "rb") as f:
            pdf_bytes = f.read()
    else:
        # treat as remote URL
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        pdf_bytes = resp.content

    data = io.BytesIO(pdf_bytes)

    try:
        with pdfplumber.open(data) as pdf:
            pages_text = []
            for page in pdf.pages:
                try:
                    text = page.extract_text() or ""
                except Exception:
                    text = ""
                pages_text.append(text)
    except Exception as e:
        raise Exception(f"Failed to open or parse PDF: {e}")

    return "\n\n".join(p for p in pages_text if p).strip()

'''
if __name__ == "__main__":
    # local quick test (runs only when executed directly)
    test_file = 'MAD II Project Report.pdf'
    if not os.path.exists(test_file):
        print(f"--- ❌ Failure! '{test_file}' file not found. ---")
    else:
        print("--- Testing get_pdf_text locally ---")
        local_url = 'file://' + os.path.abspath(test_file)
        quiz_text = get_pdf_text(local_url)
        if quiz_text:
            print("\n--- ✅ Success! Decoded Quiz Text ---")
            print(quiz_text)  # limit output
        else:
            print("\n--- ❌ Failure! No text decoded ---")
'''