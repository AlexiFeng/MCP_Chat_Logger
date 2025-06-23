#!/usr/bin/env python3
"""
RabbitMQ Setup and Test Utility

This script tests RabbitMQ connection and sets up necessary Exchange and Queue.
"""

import os
import sys
from dotenv import load_dotenv
from MCP_Chat_Logger.utils.rabbitmq_publisher import RabbitMQPublisher

def main():
    """Main function"""
    print("🐰 RabbitMQ Setup and Test Utility")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Display RabbitMQ configuration
    publisher = RabbitMQPublisher()
    print(f"""
📋 Current RabbitMQ Configuration:
- Host: {publisher.host}:{publisher.port}
- Virtual Host: {publisher.virtual_host}
- Username: {publisher.username}
- Exchange: {publisher.exchange}
- Routing Key: {publisher.routing_key}
- Queue Name: {publisher.queue_name}
    """)
    
    # Test connection
    print("🔍 Testing RabbitMQ connection...")
    if publisher.test_connection():
        print("✅ RabbitMQ connection test successful!")
        
        # Publish test message
        print("\n📤 Publishing test message...")
        test_messages = [
            {
                "role": "user",
                "content": "This is a test message."
            },
            {
                "role": "assistant", 
                "content": "Yes, I received the test message well!"
            }
        ]
        
        if publisher.publish_chat_log(
            messages=test_messages,
            conversation_id="test_conversation",
            additional_metadata={"test": True, "utility_script": True}
        ):
            print("✅ Test message published successfully!")
            print("🎉 All tests completed successfully!")
        else:
            print("❌ Test message publishing failed")
            sys.exit(1)
            
    else:
        print("❌ RabbitMQ connection test failed")
        print("\n🔧 Please check the following:")
        print("1. Verify RabbitMQ server is running")
        print("2. Check .env file configuration is correct")
        print("3. Check network connection status")
        print("4. Check firewall settings")
        sys.exit(1)

if __name__ == "__main__":
    main()
