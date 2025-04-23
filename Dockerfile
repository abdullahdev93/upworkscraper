FROM mcr.microsoft.com/playwright/python:focal

# Install Python libraries
RUN pip install python-dotenv requests playwright

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Run your script
CMD ["python", "upwork_scraper.py"]