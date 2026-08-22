# MCP Chat Logger

[![Smithery](https://smithery.ai/badge/@AlexiFeng/MCP_Chat_Logger)](https://smithery.ai/server/@AlexiFeng/MCP_Chat_Logger)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[Chinese documentation / 中文文档](README_zh.md)

MCP Chat Logger is a small [Model Context Protocol](https://modelcontextprotocol.io/) server that lets an AI client save a conversation as a readable Markdown file.

## What it does

- Exposes a `save_chat_history` MCP tool
- Writes messages, roles, and timestamps to Markdown
- Uses an optional conversation ID in the filename and document header
- Stores logs locally in the `chat_logs/` directory

## Requirements

- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/)
- An MCP-compatible client

## Quick start

Clone the repository and install the locked dependencies:

```bash
git clone https://github.com/AlexiFeng/MCP_Chat_Logger.git
cd MCP_Chat_Logger
uv sync
```

Start the server over stdio:

```bash
uv run chat_logger.py
```

## Client configuration

Use an absolute path to your clone. A typical MCP client configuration looks like this:

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

The outer configuration shape can differ between clients; the `command` and `args` values remain the same.

## Tool input

`save_chat_history` accepts:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `messages` | array | Yes | Chat messages containing `role` and `content` fields |
| `conversation_id` | string | No | Identifier added to the output filename and document header |

Example message list:

```json
[
  {"role": "user", "content": "Summarize this experiment."},
  {"role": "assistant", "content": "Here are the main findings..."}
]
```

Generated files are written to `chat_logs/chat_<timestamp>.md`, or `chat_logs/chat_<conversation_id>_<timestamp>.md` when an ID is supplied.

## Install with Smithery

For clients supported by Smithery:

```bash
npx -y @smithery/cli install @AlexiFeng/MCP_Chat_Logger --client claude
```

## Privacy

Conversation logs are written to the machine running this server. Review the content before sharing or committing generated files. The `chat_logs/` directory is excluded from Git by default.

## Development

```bash
uv sync
uv run python -m compileall chat_logger.py
```

Issues and pull requests are welcome.

## License

[MIT](LICENSE)
