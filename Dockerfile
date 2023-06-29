# Use an official Python runtime as a parent image
FROM python:3.10.11-slim-buster

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Make port 50001 available to the world outside this container
EXPOSE 5001

# Run the application using Gunicorn
CMD ["gunicorn", "-b", ":5001", "app:create_app()"]
