FROM python:3.12-slim

# Install dependencies
RUN apt-get update && apt-get install -y wget gnupg curl unzip fonts-liberation libnss3 libatk1.0-0 libatk-bridge2.0-0 libxss1 libasound2 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libgtk-3-0 libxshmfence1 libxext6 libxfixes3 libdrm2 libglu1-mesa

# Install pip dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install Playwright and Chromium
RUN pip install playwright && playwright install chromium

# Copy app files
COPY . .

# Start command
CMD ["python", "upwork_scraper.py"]