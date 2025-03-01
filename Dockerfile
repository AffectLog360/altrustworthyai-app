# Use an official lightweight Python image.
FROM python:3.9-slim

# Set the working directory.
WORKDIR /app

# Copy and install dependencies.
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire code.
COPY . .

# Expose port 5002.
EXPOSE 5002

# Set the dynamic lookup flag.
ENV FORCE_DYNAMIC_LIBEBM=true

# Start the application.
CMD ["python", "app.py"]
