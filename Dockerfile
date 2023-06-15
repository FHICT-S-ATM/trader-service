# Stage 1: Build the application
FROM python:3.9-slim AS builder

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN apt-get update -y && apt-get install -y
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

# Stage 2: Create the final image
FROM python:3.9-slim AS final

WORKDIR /app

# Copy the built application from the builder stage
COPY --from=builder /app /app

# Set the Python path
# ENV PYTHONPATH="$PYTHONPATH:/app"
ENV PYTHONPATH="/usr/local/lib/python3.9/site-packages:./.venv/lib/python3.9/site-packages"

# Install numpy
# RUN pip install --no-cache-dir numpy

# Expose the Flask app's port
EXPOSE 5000

# Set environment variables, if necessary
# ENV FLASK_ENV=production

# Run the Flask application
CMD ["python", "-m", "app.py"]
