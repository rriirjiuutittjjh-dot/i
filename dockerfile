# Use the official lightweight Debian 13 (Trixie) stable release image
FROM debian:13-slim

# Set the working directory inside the container
WORKDIR /app

# Install Python and pip safely via apt
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# Copy the rest of the application files (app.py, templates, etc.)
COPY . .

# Expose port 5000 for Flask
EXPOSE 5000

# Command to run your Flask application
CMD ["python3", "app.py"]
