from typing import List, Dict, Any, Optional
import os
import re
from datetime import datetime
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from utils.rabbitmq_publisher import publish_chat_message, get_publisher

# Load environment variables
load_dotenv()

# Determine AMQP usage based on environment variables
def determine_amqp_usage():
    """Determine if AMQP should be used based on environment variables"""
    required_vars = ['RABBITMQ_HOST', 'RABBITMQ_PORT', 'RABBITMQ_USERNAME', 'RABBITMQ_PASSWORD']
    return all(os.getenv(var) for var in required_vars)

USE_AMQP = determine_amqp_usage()

# Initialize FastMCP server
mcp = FastMCP("chat_logger")

def ensure_logs_directory():
    """Ensure the logs directory exists"""
    if not os.path.exists("chat_logs"):
        os.makedirs("chat_logs")

def format_message(message: Dict[str, Any]) -> str:
    """Format message into Markdown format"""
    role = message.get("role", "unknown")
    content = message.get("content", "")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""
### {role.capitalize()} - {timestamp}

{content}

---
"""

@mcp.tool()
async def save_chat_history(messages: List[Dict[str, Any]], conversation_id: str = None) -> str:
    """
    Save chat history as a Markdown file and publish to RabbitMQ
    
    Args:
        messages: List of chat messages, each containing role and content
        conversation_id: Optional conversation ID for file naming
    """
    # 1. Validate messages parameter
    if not messages:
        return "❌ Error: messages parameter is empty or missing."
    
    if not isinstance(messages, list):
        return "❌ Error: messages must be a list."
    
    # 2. Validate individual messages
    for i, message in enumerate(messages):
        if not isinstance(message, dict):
            return f"❌ Error: Message #{i} is not in proper format."
        
        if 'role' not in message or 'content' not in message:
            return f"❌ Error: Message #{i} is missing 'role' or 'content'."
    
    
    ensure_logs_directory()
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_logs/chat_{conversation_id}_{timestamp}.md" if conversation_id else f"chat_logs/chat_{timestamp}.md"
    
    # Get source from environment variable
    source = os.getenv('MCP_SOURCE', 'claude')
    
    # Format content according to design specification
    formatted_content = "# Chat History\n\n"
    if conversation_id:
        formatted_content += f"Conversation ID: {conversation_id}\n"
    formatted_content += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    formatted_content += f"Source: {source}\n\n"
    
    for message in messages:
        formatted_content += format_message(message)
    
    # Save file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(formatted_content)
    
    result_message = f"Chat history has been saved to file: {filename}"
    
    # Publish message to RabbitMQ only if AMQP is enabled
    if USE_AMQP:
        try:
            additional_metadata = {
                "filename": filename,
                "file_size": os.path.getsize(filename),
                "message_count": len(messages),
                "save_timestamp": timestamp,
                "source": source
            }
            
            publish_success = publish_chat_message(
                messages=messages,
                conversation_id=conversation_id,
                message_type="chat",
                additional_metadata=additional_metadata
            )
            
            if publish_success:
                result_message += f"\n✓ RabbitMQ message published successfully (source: {source})"
            else:
                result_message += "\n⚠ RabbitMQ message publish failed (file saved successfully)"
                
        except Exception as e:
            result_message += f"\n⚠ RabbitMQ publish error: {str(e)} (file saved successfully)"
    else:
        result_message += f"\nℹ RabbitMQ not configured - file-only mode (source: {source})"
    
    return result_message

if __name__ == "__main__":
    # Get source for startup message
    source = os.getenv('MCP_SOURCE', 'claude')
    
    # Print startup message based on AMQP configuration
    if USE_AMQP:
        print(f"🔧 MCP Chat Logger starting with RabbitMQ enabled (source: {source})")
    else:
        print(f"🔧 MCP Chat Logger starting in file-only mode (source: {source})")
    
    # Initialize and run the server
    mcp.run(transport='stdio') 