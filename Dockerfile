# Use the official Python 3.8 image as the base image
FROM python:3.8-slim-buster

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt requirements.txt

# Install any dependencies specified in requirements.txt
RUN pip3 install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Specify the
