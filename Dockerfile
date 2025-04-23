FROM mcr.microsoft.com/playwright/python:v1.43.1-focal

# Install dotenv and requests
RUN pip install python-dotenv requests

# Copy your app
WORKDIR /app
COPY . .

# Run your script
CMD ["python", "upwork_scraper.py"]