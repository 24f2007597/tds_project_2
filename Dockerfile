FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 1. Install prerequisites for adding repositories
# We only install the bare minimum needed for the next step.
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 2. Add Google's GPG key, add the Chrome repo, and install
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    # Now, install Chrome. apt-get will automatically find and install
    # all the correct dependencies (like libnss3, etc.) for your OS.
    && apt-get install -y google-chrome-stable --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the requirements file first to cache dependencies
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Tell Railway what port your app will run on.
# Railway will provide the $PORT variable.
# Use 8080 as a default if $PORT isn't set.
ENV PORT 8080

# Command to run your Flask/FastAPI app.
# This example is for FastAPI with uvicorn.
# For Flask: CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app:app", "--bind", "0.0.0.0:$PORT"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]