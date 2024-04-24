# Dockerfile for the main application
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR .

# Copy the main application files
COPY . .

# Install dependencies
# COPY requirements.txt .
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 5001

# Command to run the application
CMD ["python", "master_assistant.py"]
