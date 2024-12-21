# Use official Python base image
FROM python:3.10-slim

# Install system dependencies for Chrome and Chromium WebDriver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libxss1 \
    libappindicator3-1 \
    libindicator3-1 \
    fonts-liberation \
    xdg-utils \
    && apt-get clean

# Install required Python libraries
RUN pip install selenium

# Set working directory
WORKDIR /usr/src/app

# Copy your Python script into the container
COPY . .

# Command to run the script
CMD ["python", "your_script.py"]
