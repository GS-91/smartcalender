# Use official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . /app

# Copy the API key file explicitly to the correct location
COPY app/api_key.txt /app/app/api_key.txt

# Kopiere die credentials.json ins richtige Verzeichnis
COPY app/credentials.json /app/app/api/credentials.json

# Start the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]





