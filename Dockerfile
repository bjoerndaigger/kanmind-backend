# Base image: Python 3.12 on Alpine Linux
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . $WORKDIR

# Default port the application listens on
ENV APPLICATION_PORT=8000 

# Install dependencies and make entrypoint executable
RUN apk add --no-cache postgresql-dev gcc musl-dev \
    && pip install -r requirements.txt \
    && chmod +x /app/entrypoint.sh   

# Document the port (informational only)
EXPOSE ${APPLICATION_PORT}

# Create and switch to non-root user for security
RUN adduser -D appuser
USER appuser

# Run entrypoint script on container start
ENTRYPOINT ["/app/entrypoint.sh"]