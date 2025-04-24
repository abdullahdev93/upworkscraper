FROM mcr.microsoft.com/playwright/python:v1.48.0-focal

# Install dependencies
RUN pip install python-dotenv requests playwright

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Print file list to verify visibility
RUN ls -la /app

# Force Python to run in unbuffered, verbose mode
CMD ["python", "-u", "upwork_scraper.py"]
