# Base image: Python 3.12 on Alpine Linux
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Copy project files into /app
COPY . .

# Default port the application listens on
ENV APPLICATION_PORT=8000 

# Create and switch to non-root user for security
RUN adduser -D appuser

# Install dependencies and make entrypoint executable
RUN apk add --no-cache postgresql-dev gcc musl-dev \
    && pip install -r requirements.txt \
    && chmod +x /app/entrypoint.sh \
    && chown -R appuser:appuser /app 

# Document the port (informational only)
EXPOSE ${APPLICATION_PORT}

USER appuser

# Run entrypoint script on container start
ENTRYPOINT ["/app/entrypoint.sh"]