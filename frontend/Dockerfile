# Use a minimal base image with Python 3.13, matching the backend
FROM python:3.13-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file first so the dependency layer is cached between builds
COPY requirements.txt .

# Install Python dependencies without keeping the download cache, to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Document the port the Streamlit app listens on
EXPOSE 8501

# Run the Streamlit app on port 8501, reachable from outside the container
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.enableXsrfProtection=false", \
     "--browser.gatherUsageStats=false"]
