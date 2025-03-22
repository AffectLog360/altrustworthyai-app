# Use an official Python 3.9 slim image (or any version you prefer)
FROM python:3.9-slim

# Create an app directory and set it as working dir
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire code into the container
COPY . .

# Expose the application port
EXPOSE 5002

# Command to run the application
CMD ["python", "app.py"]
