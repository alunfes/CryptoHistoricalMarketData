# ⚠️  DEPRECATED: This Dockerfile is kept for backward compatibility only.
# ⚠️  Please use the Dockerfile in the root directory instead.
# ⚠️  The docker-compose.yml now uses the root-level Dockerfile by default.
#
# This file will be removed in a future version.
# See ../Dockerfile and ../DOCKER_GUIDE.md for the updated Docker setup.

# Use an official Python runtime as a parent image
FROM python:latest

# The environment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
#COPY requirements.txt /app/
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt

#CMD ["python", "./main.py"]