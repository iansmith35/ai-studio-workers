# Use RunPod's official base image with CUDA support
FROM runpod/base:0.4.0-cuda11.8.0

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy handler
COPY handler.py .

# Start the RunPod serverless handler
CMD ["python", "-u", "handler.py"]