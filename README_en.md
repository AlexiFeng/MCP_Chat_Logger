# MCP Chat Logger

[![smithery badge](https://smithery.ai/badge/@AlexiFeng/MCP_Chat_Logger)](https://smithery.ai/server/@AlexiFeng/MCP_Chat_Logger)

<div align="center">
  <a href="README.md">中文</a> | <a href="README_ko.md">한국어</a>
</div>

---

MCP Chat Logger is a simple yet powerful tool for saving chat history as Markdown format files with real-time message publishing through RabbitMQ support. It supports both development and production environment configurations.

## 🚀 Quick Start

### 1. Project Setup

```bash
# Clone repository
git clone https://github.com/yourusername/MCP_Chat_Logger.git
cd MCP_Chat_Logger

# Install dependencies
uv add "mcp[cli]>=1.6.0"
uv add "pika>=1.3.0" 
uv add "python-dotenv>=1.0.0"
```

### 2. Environment Selection

This project supports **Development** and **Production** environment configurations:

#### 🛠️ Development Environment (Local Docker RabbitMQ)

Local Docker-based RabbitMQ environment for development and testing.

```bash
# Create environment variables file
cp dev-tools/.env.example .env

# Start RabbitMQ server with Docker
cd dev-tools
docker-compose up -d

# Test connection
uv run test_rabbitmq.py

# Run MCP server
cd ..
uv run chat_logger.py
```

#### ☁️ Production Environment (CloudAMQP Recommended)

For actual service deployment, we recommend using managed RabbitMQ services like **CloudAMQP**.

```bash
# Create .env file directly
cat > .env << EOF
RABBITMQ_HOST=your-cloudamqp-url.com
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=your-username
RABBITMQ_PASSWORD=your-password
RABBITMQ_VIRTUAL_HOST=your-vhost
RABBITMQ_EXCHANGE=llmLogger
RABBITMQ_ROUTING_KEY=llm_logger
RABBITMQ_QUEUE_NAME=llm_logger
EOF

# Run MCP server
uv run chat_logger.py
```

#### 📂 File-Only Mode (Without RabbitMQ)

If you want to use only file saving without RabbitMQ, simply don't set the environment variables and it will automatically run in file-only mode:

```bash
# Run without environment variables (automatically enters file-only mode)
uv run chat_logger.py
```

### 3. Automatic Mode Detection

MCP Chat Logger automatically determines the operating mode based on environment variable settings:

- **RabbitMQ Mode**: When `RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_USERNAME`, `RABBITMQ_PASSWORD` are all set
- **File-Only Mode**: When any of the above environment variables is missing

```bash
# Run (automatically determines mode based on environment variables)
uv run chat_logger.py
```

## 📋 Environment-Specific Configuration

### Development Environment Setup

#### Environment Variables File

Copy `dev-tools/.env.example` to create `.env` file:

```bash
# RabbitMQ Configuration (Development)
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VIRTUAL_HOST=/
RABBITMQ_EXCHANGE=llmLogger
RABBITMQ_ROUTING_KEY=llm_logger
RABBITMQ_QUEUE_NAME=llm_logger
```

#### Docker Commands

```bash
# Start RabbitMQ server
cd dev-tools
docker-compose up -d

# Stop RabbitMQ server
docker-compose down

# View logs
docker-compose logs rabbitmq

# Access Web management UI: http://localhost:15672 (guest/guest)
```

#### Development Tools Execution

```bash
# RabbitMQ connection test
cd dev-tools
uv run test_rabbitmq.py

# Or from project root
uv run dev-tools/test_rabbitmq.py
```

### Production Environment Setup

#### CloudAMQP Configuration (Recommended)

1. Create [CloudAMQP](https://www.cloudamqp.com/) account
2. Create RabbitMQ instance
3. Set connection information in `.env` file

```bash
# CloudAMQP connection example
RABBITMQ_HOST=your-instance.cloudamqp.com
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=your-username
RABBITMQ_PASSWORD=your-password
RABBITMQ_VIRTUAL_HOST=your-vhost
RABBITMQ_EXCHANGE=llmLogger
RABBITMQ_ROUTING_KEY=llm_logger
RABBITMQ_QUEUE_NAME=llm_logger

# Optional connection settings
RABBITMQ_CONNECTION_TIMEOUT=30
RABBITMQ_HEARTBEAT=600
RABBITMQ_BLOCKED_CONNECTION_TIMEOUT=300
```

## Features

- 🐰 **RabbitMQ Integration**: Real-time message publishing and subscription support
- 📝 **Markdown Storage**: Save chat history in clean Markdown format
- ⏰ **Timestamps**: Automatically add timestamps to each message
- 📁 **Custom Directory**: Support for user-defined save directories
- 🔍 **Session Management**: Support session IDs to identify different conversations
- 🛠️ **Environment Variables**: Configuration management through `.env` files
- ☁️ **Multi-Environment Support**: Support for development (Docker) and production (CloudAMQP) environments

### Exchange Design

- **Exchange Name**: `llmLogger`
- **Exchange Type**: `direct`
- **Routing Key**: `llm_logger`
- **Queue Name**: `llm_logger`
- **Binding**: Queue `llm_logger` bound to Exchange `llmLogger` with Routing Key `llm_logger`

### Available MCP Tool

**save_chat_history**: Save chat history as Markdown files and publish to RabbitMQ (when environment variables are set)

## Claude Desktop / Cursor Configuration

### RabbitMQ Mode (With Environment Variables)

```json
{
  "chat_logger": {
    "name": "chat_logger",
    "isActive": true,
    "command": "uv",
    "args": [
      "--directory",
      "/path/to/MCP_Chat_Logger",
      "run",
      "chat_logger.py"
    ],
    "env": {
      "RABBITMQ_HOST": "your-rabbitmq-host",
      "RABBITMQ_PORT": "5672",
      "RABBITMQ_USERNAME": "your-username",
      "RABBITMQ_PASSWORD": "your-password"
    }
  }
}
```

### File-Only Mode (Without Environment Variables)

```json
{
  "chat_logger_file_only": {
    "name": "chat_logger_file_only",
    "isActive": true,
    "command": "uv",
    "args": [
      "--directory",
      "/path/to/MCP_Chat_Logger",
      "run",
      "chat_logger.py"
    ]
  }
}
```

## Project Structure

```
MCP_Chat_Logger/
├── chat_logger.py         # Main MCP server
├── utils/                 # Utility modules
│   └── rabbitmq_publisher.py  # RabbitMQ message publishing module
├── dev-tools/            # Development environment tools
│   ├── docker-compose.yml    # RabbitMQ Docker configuration
│   ├── .env.example          # Development environment variables example
│   └── test_rabbitmq.py      # RabbitMQ connection test script
├── chat_logs/            # Default save directory
├── pyproject.toml        # Project settings and dependencies
├── .env                  # Environment variables config (user-created)
├── README.md             # Project description (Chinese)
├── README_ko.md          # Korean description
├── README_en.md          # English description
└── .gitignore            # Git ignore file
```

## Installation Options

### Automatic Installation via Smithery

Install MCP Chat Logger for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@AlexiFeng/MCP_Chat_Logger):

```bash
npx -y @smithery/cli install @AlexiFeng/MCP_Chat_Logger --client claude
```

## Next Steps

- Add Overview functionality
- Message format customization options
- Additional message broker support
- High availability configuration guide

## Contribution Guidelines

Issues and pull requests are welcome! If you want to contribute code, please follow these steps:

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 