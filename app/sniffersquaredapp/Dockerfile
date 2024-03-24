
# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the project dependencies
# in 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code to the container
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port that the Django app will run on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]