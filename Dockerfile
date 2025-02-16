# Use Python as base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all necessary files
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Run the application
CMD ["uv", "run", "app.py"]
