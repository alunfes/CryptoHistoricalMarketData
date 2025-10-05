# Use an official Python runtime with specific version for reproducibility
FROM python:3.11-slim

# Set maintainer label
LABEL maintainer="CryptoHistoricalMarketData"
LABEL description="Docker image for fetching cryptocurrency historical market data"

# The environment variable ensures that the python output is set straight
# to the terminal without buffering it first
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy requirements file first for better layer caching
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app/ /app/app/
COPY ignore/ /app/ignore/

# Create data directory
RUN mkdir -p /app/app/Data

# Set proper permissions
RUN chmod -R 755 /app

# Default command to run the application
CMD ["python3", "app/main.py"]
