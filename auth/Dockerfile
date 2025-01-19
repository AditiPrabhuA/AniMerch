# Use the official Python image as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY src/ .

# Set the command to run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]