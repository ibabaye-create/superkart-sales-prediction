FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first so the dependency layer is cached between builds
COPY requirements.txt .

# Install dependencies without using cache to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and the model file
COPY . .

# Document the port the application listens on
EXPOSE 7860

# Start the application using Gunicorn
# -w 4                 : 4 worker processes to handle requests in parallel
# -b 0.0.0.0:7860      : listen on port 7860 on all network interfaces
# --timeout 120        : allow time for the model to load when a worker starts
# app:superkart_api    : the Flask instance named superkart_api inside app.py
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "--timeout", "120", "app:superkart_api"]
