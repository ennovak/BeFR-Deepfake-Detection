FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files into the image
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port required by Hugging Face Spaces
EXPOSE 7860

# Run the Flask app with Gunicorn
# IMPORTANT: routing.py is inside the backend/ directory
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "backend.routing:app"]

