# Use the official Debian 13 (Trixie) stable release image
FROM debian:13-slim

# Set working directory inside the container
WORKDIR /app

# Update package lists and install basic tools or dependencies safely
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy your project files into the container
COPY . .

# Set the default command to run when the container starts
CMD ["python3", "app.py"]
