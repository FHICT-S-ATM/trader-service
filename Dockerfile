# Stage 1: Build the application
FROM python:3.9-slim AS builder

# Set the working directory
WORKDIR /app

# Copy the source code and requirements
COPY app.py eurusdyfinance.py eurusdyfinance-plot.py requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Create the final image
FROM python:3.9-slim AS final

# Set the working directory
WORKDIR /app

# Copy the source code from the builder stage
COPY --from=builder /app /app

# Copy the dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Expose the Flask app's port
EXPOSE 5000

# Set environment variables, if necessary
# ENV FLASK_ENV=production

# Run the Flask application
CMD ["python", "app.py"]

