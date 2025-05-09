# Generated by https://smithery.ai. See: https://smithery.ai/docs/config#dockerfile
FROM python:3.10-alpine

# Install build dependencies and runtime dependencies
RUN apk add --no-cache build-base libffi-dev openssl-dev

# Set working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Upgrade pip and install uv and mcp with CLI extras
RUN pip install --upgrade pip \
    && pip install uv "mcp[cli]>=1.6.0"

# Expose port if needed (not necessary for stdio transport)

# Run the MCP server using uv
CMD ["uv", "run", "chat_logger.py"]
