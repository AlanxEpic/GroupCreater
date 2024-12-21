# Use Python 3.10 slim as base image
FROM python:3.10-slim

# Install system dependencies for Chrome and Chromium WebDriver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libxss1 \
    libappindicator3-1 \
    fonts-liberation \
    xdg-utils \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app

# Set working directory
WORKDIR /app

# Expose port
EXPOSE 8080

# Command to run the app
CMD ["python", "app.py"]
