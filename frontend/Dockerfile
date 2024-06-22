# Use the official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY ./frontend/requirements.txt .
# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend folder to the container
COPY ./frontend /app

# Expose port 80 for the app
EXPOSE 8501

# Run the Streamlit app with Uvicorn
CMD ["streamlit", "run", "app.py"]