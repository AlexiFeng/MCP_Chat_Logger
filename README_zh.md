# MCP Chat Logger

[English](README.md)

MCP Chat Logger 是一个小型 [Model Context Protocol](https://modelcontextprotocol.io/) 服务器，让 AI 客户端可以将对话保存为易于阅读的 Markdown 文件。

## 功能

- 提供 `save_chat_history` MCP 工具
- 将消息、角色和时间戳写入 Markdown
- 支持可选的会话 ID
- 日志仅保存在本地 `chat_logs/` 目录

## 环境要求

- Python 3.10 或更高版本
- [uv](https://docs.astral.sh/uv/)
- 支持 MCP 的客户端

## 快速开始

```bash
git clone https://github.com/AlexiFeng/MCP_Chat_Logger.git
cd MCP_Chat_Logger
uv sync
uv run chat_logger.py
```

## 客户端配置

将下面的路径替换为仓库的绝对路径：

```json
{
  "mcpServers": {
    "chat_logger": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/MCP_Chat_Logger",
        "run",
        "chat_logger.py"
      ]
    }
  }
}
```

`save_chat_history` 接收消息数组和可选的 `conversation_id`。生成的文件保存为 `chat_logs/chat_<timestamp>.md`；提供会话 ID 时，文件名为 `chat_logs/chat_<conversation_id>_<timestamp>.md`。

## 隐私

对话记录保存在运行此服务器的设备上。分享或提交文件前请检查其内容。`chat_logs/` 默认已加入 Git 忽略列表。

## 开发检查

```bash
uv sync
uv run python -m compileall chat_logger.py
```

## 许可证

[MIT](LICENSE)
