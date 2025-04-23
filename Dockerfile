FROM mcr.microsoft.com/playwright/python:focal

# Install dotenv and requests
RUN pip install python-dotenv requests

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Run your script
CMD ["python", "upwork_scraper.py"]