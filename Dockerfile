# Use lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency file and install required Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the Flask app port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
