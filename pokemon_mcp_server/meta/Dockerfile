# Use an official Python runtime
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy project files except meta folder
COPY .. .

# Install dependencies
RUN pip install --no-cache-dir -r meta/requirements.txt

# Expose port your app listens to
EXPOSE 5000

# Run the application
CMD ["fastmcp", "run", "server.py", "--transport", "sse", "--host", "0.0.0.0", "--port", "5000"]
