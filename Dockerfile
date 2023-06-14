# Stage 1: Build the application
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

# Stage 2: Create the final image
FROM python:3.11-slim AS final

WORKDIR /app

# Copy the built application from the builder stage
COPY --from=builder /app /app

# Expose the Flask app's port
EXPOSE 5000

# Set environment variables, if necessary
# ENV FLASK_ENV=production

# Run the Flask application
CMD ["python", "app.py"]