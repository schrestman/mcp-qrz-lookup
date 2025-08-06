# Use a slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies first so Docker can cache the install step
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source
COPY . .

# Expose the FastAPI default port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
