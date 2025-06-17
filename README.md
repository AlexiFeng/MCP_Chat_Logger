# MCP Chat Logger

[![smithery badge](https://smithery.ai/badge/@AlexiFeng/MCP_Chat_Logger)](https://smithery.ai/server/@AlexiFeng/MCP_Chat_Logger)

<div align="center">
  <a href="README_ko.md">한국어</a> | <a href="README_en.md">English</a>
</div>

---

MCP Chat Logger是一个简单而强大的聊天记录保存工具，可以将聊天历史保存为Markdown格式文件，并支持通过RabbitMQ进行实时消息发布。支持开发环境和生产环境双重配置。

## 🚀 快速开始

### 1. 项目设置

```bash
# 克隆仓库
git clone https://github.com/yourusername/MCP_Chat_Logger.git
cd MCP_Chat_Logger

# 安装依赖
uv add "mcp[cli]>=1.6.0"
uv add "pika>=1.3.0" 
uv add "python-dotenv>=1.0.0"
```

### 2. 环境选择

本项目支持**开发环境**和**生产环境**两种配置：

#### 🛠️ 开发环境（本地Docker RabbitMQ）

用于开发和测试的本地Docker RabbitMQ环境。

```bash
# 创建环境变量文件
cp dev-tools/.env.example .env

# 使用Docker启动RabbitMQ服务器
cd dev-tools
docker-compose up -d

# 连接测试
uv run test_rabbitmq.py

# 运行MCP服务器
cd ..
uv run chat_logger.py
```

#### ☁️ 生产环境（推荐CloudAMQP）

对于实际服务部署，推荐使用**CloudAMQP**等托管RabbitMQ服务。

```bash
# 直接创建.env文件
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

# 运行MCP服务器
uv run chat_logger.py
```

#### 📂 仅文件模式（无RabbitMQ）

如果只想使用文件保存功能而不使用RabbitMQ，不设置环境变量即可自动启用仅文件模式：

```bash
# 无环境变量运行（自动进入仅文件模式）
uv run chat_logger.py
```

### 3. 自动模式检测

MCP Chat Logger根据环境变量设置情况自动决定运行模式：

- **RabbitMQ模式**：当`RABBITMQ_HOST`、`RABBITMQ_PORT`、`RABBITMQ_USERNAME`、`RABBITMQ_PASSWORD`全部设置时
- **仅文件模式**：当上述环境变量中任一未设置时

```bash
# 运行（根据环境变量自动决定模式）
uv run chat_logger.py
```

## 📋 环境详细配置

### 开发环境配置

#### 环境变量文件

复制`dev-tools/.env.example`创建`.env`文件：

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

#### Docker命令

```bash
# 启动RabbitMQ服务器
cd dev-tools
docker-compose up -d

# 停止RabbitMQ服务器
docker-compose down

# 查看日志
docker-compose logs rabbitmq

# 访问Web管理界面：http://localhost:15672 (guest/guest)
```

#### 开发工具运行

```bash
# RabbitMQ连接测试
cd dev-tools
uv run test_rabbitmq.py

# 或从项目根目录
uv run dev-tools/test_rabbitmq.py
```

### 生产环境配置

#### CloudAMQP设置（推荐）

1. 创建[CloudAMQP](https://www.cloudamqp.com/)账户
2. 创建RabbitMQ实例
3. 在`.env`文件中设置连接信息

```bash
# CloudAMQP连接示例
RABBITMQ_HOST=your-instance.cloudamqp.com
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=your-username
RABBITMQ_PASSWORD=your-password
RABBITMQ_VIRTUAL_HOST=your-vhost
RABBITMQ_EXCHANGE=llmLogger
RABBITMQ_ROUTING_KEY=llm_logger
RABBITMQ_QUEUE_NAME=llm_logger

# 可选连接设置
RABBITMQ_CONNECTION_TIMEOUT=30
RABBITMQ_HEARTBEAT=600
RABBITMQ_BLOCKED_CONNECTION_TIMEOUT=300
```

## 功能特点

- 🐰 **RabbitMQ集成**：实时消息发布和订阅支持
- 📝 **Markdown存储**：将聊天记录保存为整洁的Markdown格式
- ⏰ **时间戳**：自动为每条消息添加时间戳
- 📁 **自定义目录**：支持用户自定义保存目录
- 🔍 **会话管理**：支持会话ID标识不同的对话
- 🛠️ **环境变量**：通过`.env`文件进行配置管理
- ☁️ **多环境支持**：支持开发环境（Docker）和生产环境（CloudAMQP）

### Exchange设计

- **Exchange名称**：`llmLogger`
- **Exchange类型**：`direct`
- **路由键**：`llm_logger`
- **队列名称**：`llm_logger`
- **绑定**：队列`llm_logger`通过路由键`llm_logger`绑定到Exchange `llmLogger`

### 可用的MCP工具

**save_chat_history**：将聊天记录保存为Markdown文件并发布到RabbitMQ（环境变量设置时）

## Claude Desktop / Cursor配置

### RabbitMQ模式（设置环境变量）

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

### 仅文件模式（无环境变量）

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

## 项目结构

```
MCP_Chat_Logger/
├── chat_logger.py         # 主MCP服务器
├── utils/                 # 工具模块
│   └── rabbitmq_publisher.py  # RabbitMQ消息发布模块
├── dev-tools/            # 开发环境工具
│   ├── docker-compose.yml    # RabbitMQ Docker配置
│   ├── .env.example          # 开发用环境变量示例
│   └── test_rabbitmq.py      # RabbitMQ连接测试脚本
├── chat_logs/            # 默认保存目录
├── pyproject.toml        # 项目设置和依赖
├── .env                  # 环境变量配置（用户创建）
├── README.md             # 项目说明（中文）
├── README_ko.md          # 韩语说明
├── README_en.md          # 英文说明
└── .gitignore            # Git忽略文件
```

## 安装选项

### 通过Smithery自动安装

通过[Smithery](https://smithery.ai/server/@AlexiFeng/MCP_Chat_Logger)为Claude Desktop自动安装MCP Chat Logger：

```bash
npx -y @smithery/cli install @AlexiFeng/MCP_Chat_Logger --client claude
```

## 下一阶段

- 添加Overview功能
- 消息格式自定义选项
- 额外的消息代理支持
- 高可用性配置指南

## 贡献指南

欢迎提交问题和拉取请求！如果您想贡献代码，请遵循以下步骤：

1. Fork这个仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个Pull Request

## 许可证

该项目采用MIT许可证 - 详情请查看 LICENSE 文件。
