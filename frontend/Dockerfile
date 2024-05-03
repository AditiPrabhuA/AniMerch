# Use the official Python image as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 5000
CMD ["python","app.py", "--host", "0.0.0.0"]