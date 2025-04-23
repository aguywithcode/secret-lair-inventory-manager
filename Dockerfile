FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for JavaScript functionality
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g eslint \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt .
COPY tests/requirements-test.txt ./tests/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt \
    && pip3 install --no-cache-dir -r tests/requirements-test.txt

# Copy application code
COPY . .

# Run data initialization on container start
CMD ["sh", "-c", "python3 init_data.py && python3 run_web.py --host=0.0.0.0"]

# Expose the port the app runs on
EXPOSE 5000