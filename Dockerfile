# Use official Python runtime
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (gcc for building some python packages if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port used by Streamlit (7860 is standard for HF Spaces)
EXPOSE 7860

# Make the start script executable
RUN chmod +x start.sh

# Run the startup script
CMD ["./start.sh"]
