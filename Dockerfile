ARG VERSION="dev"

FROM python:3.10-slim AS build

# Set build arguments
ARG VERSION

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Set working directory
WORKDIR /app

# Copy only the dependency files first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

# Build the package
RUN pip install --no-cache-dir -e .

# Create a runtime stage with minimal dependencies
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy installed packages and application from build stage
COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=build /app /app

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Expose any necessary ports
# (No ports needed as this uses stdio for communication)

# Set environment variable for version
ENV APP_VERSION=${VERSION}

# Command to run the server
ENTRYPOINT ["/app/entrypoint.sh"]

# The server will expect client_id and client_secret to be provided via environment variables:
# PORT_CLIENT_ID and PORT_CLIENT_SECRET
