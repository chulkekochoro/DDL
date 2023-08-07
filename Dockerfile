# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /flask

# Copy the requirements file into the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Expose the port that your Flask app will run on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]