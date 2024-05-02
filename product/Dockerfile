#Python Version
FROM python:3.9-slim

#Creating a working directory
WORKDIR /app

#Adding the requirement.txt file
COPY requirements.txt .

#Installing all the requirements
RUN pip install --no-cache-dir -r requirements.txt

#Adding all the files into docker
COPY src/ .

#Running the file
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5001"]