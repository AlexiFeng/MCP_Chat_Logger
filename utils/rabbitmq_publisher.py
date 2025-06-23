"""
RabbitMQ Message Publishing Module

This module provides functionality to publish chat logs to RabbitMQ queues.
RabbitMQ connection settings are managed through environment variables.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import pika
from pika.exceptions import AMQPConnectionError, AMQPChannelError

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RabbitMQPublisher:
    """Class responsible for RabbitMQ message publishing"""
    
    def __init__(self):
        """Load RabbitMQ configuration from environment variables and initialize"""
        self.host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.port = int(os.getenv('RABBITMQ_PORT', '5672'))
        self.username = os.getenv('RABBITMQ_USERNAME', 'guest')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'guest')
        self.virtual_host = os.getenv('RABBITMQ_VIRTUAL_HOST', '/')
        # Updated to use 'pkms' exchange as per design specification
        self.exchange = os.getenv('RABBITMQ_EXCHANGE', 'pkms')
        self.routing_key = os.getenv('RABBITMQ_ROUTING_KEY', 'llm_logger')
        self.queue_name = os.getenv('RABBITMQ_QUEUE_NAME', 'llm_logger')
        
        # Connection settings - 더 보수적인 값으로 설정
        self.connection_timeout = int(os.getenv('RABBITMQ_CONNECTION_TIMEOUT', '10'))
        self.heartbeat = int(os.getenv('RABBITMQ_HEARTBEAT', '300'))
        self.blocked_connection_timeout = int(os.getenv('RABBITMQ_BLOCKED_CONNECTION_TIMEOUT', '60'))
        
        self.connection = None
        self.channel = None
        
        logger.info(f"RabbitMQ Publisher initialized - Host: {self.host}:{self.port}, Exchange: {self.exchange}")
    
    def _create_connection(self) -> bool:
        """Create and configure RabbitMQ connection"""
        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.virtual_host,
                credentials=credentials,
                connection_attempts=5,  # 재시도 횟수 증가
                retry_delay=1,  # 짧은 대기 시간
                socket_timeout=self.connection_timeout,
                heartbeat=self.heartbeat,
                blocked_connection_timeout=self.blocked_connection_timeout,
                # IPv6 문제 해결을 위한 추가 옵션
                tcp_options={
                    'TCP_KEEPIDLE': 600,
                    'TCP_KEEPINTVL': 30,
                    'TCP_KEEPCNT': 3
                }
            )
            
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declare exchange (create if not exists)
            self.channel.exchange_declare(
                exchange=self.exchange,
                exchange_type='direct',
                durable=True
            )
            
            # Declare queue (create if not exists)
            self.channel.queue_declare(
                queue=self.queue_name,
                durable=True
            )
            
            # Bind queue to exchange
            self.channel.queue_bind(
                exchange=self.exchange,
                queue=self.queue_name,
                routing_key=self.routing_key
            )
            
            logger.info("RabbitMQ connection and configuration completed")
            return True
            
        except AMQPConnectionError as e:
            logger.error(f"RabbitMQ connection failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during RabbitMQ setup: {e}")
            return False
    
    def _close_connection(self):
        """Close RabbitMQ connection"""
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.close()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            logger.info("RabbitMQ connection closed")
        except Exception as e:
            logger.error(f"Error closing RabbitMQ connection: {e}")
    
    def publish_chat_log(self, 
                        messages: list, 
                        conversation_id: Optional[str] = None,
                        message_type: str = "chat",
                        additional_metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Publish chat log to RabbitMQ according to design specification
        
        Args:
            messages: List of chat messages
            conversation_id: Conversation ID (optional)
            message_type: Type of message (chat, analysis, etc.)
            additional_metadata: Additional metadata (optional)
            
        Returns:
            bool: Whether publishing was successful
        """
        # 재시도 로직 구현
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # 연결 상태 확인 및 생성
                if not self.connection or self.connection.is_closed:
                    if not self._create_connection():
                        if attempt < max_retries - 1:
                            logger.warning(f"Connection attempt {attempt + 1} failed, retrying...")
                            continue
                        return False
                
                # 채널 상태 확인
                if not self.channel or self.channel.is_closed:
                    if not self._create_connection():
                        if attempt < max_retries - 1:
                            logger.warning(f"Channel creation attempt {attempt + 1} failed, retrying...")
                            continue
                        return False
                
                # Get source from environment variable (MCP_SOURCE)
                source = os.getenv('MCP_SOURCE', 'claude')
                
                # Compose message payload according to design specification
                payload = {
                    "source": source,
                    "type": message_type,
                    "conversation_id": conversation_id,
                    "sending_at": datetime.now().strftime("%Y%m%d %H%M%S"),
                    "contents": messages,
                    "metadata": additional_metadata or {}
                }
                            
                # Serialize to JSON
                message_body = json.dumps(payload, ensure_ascii=False, indent=2)
                
                # Publish message
                self.channel.basic_publish(
                    exchange=self.exchange,
                    routing_key=self.routing_key,
                    body=message_body.encode('utf-8'),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # Message persistence
                        content_type='application/json',
                        content_encoding='utf-8',
                        timestamp=int(datetime.now().timestamp())
                    )
                )
                
                logger.info(f"Message published successfully - Source: {source}, Type: {message_type}, Conversation ID: {conversation_id}, Message count: {len(messages)}")
                return True
                
            except AMQPChannelError as e:
                logger.error(f"RabbitMQ channel error: {e}")
                # Attempt to reset connection on channel error
                self._close_connection()
                if attempt < max_retries - 1:
                    logger.warning(f"Channel error on attempt {attempt + 1}, retrying...")
                    continue
                return False
            except Exception as e:
                logger.error(f"Error during message publishing: {e}")
                if attempt < max_retries - 1:
                    logger.warning(f"Publishing attempt {attempt + 1} failed, retrying...")
                    continue
                return False
    
    def test_connection(self) -> bool:
        """
        Test RabbitMQ connection
        
        Returns:
            bool: Whether connection test was successful
        """
        try:
            if self._create_connection():
                self._close_connection()
                logger.info("RabbitMQ connection test successful")
                return True
            else:
                logger.error("RabbitMQ connection test failed")
                return False
        except Exception as e:
            logger.error(f"Error during connection test: {e}")
            return False
    
    def get_configuration(self) -> str:
        """
        Get current RabbitMQ configuration as formatted string
        
        Returns:
            str: Configuration information
        """
        config = f"""RabbitMQ Configuration:
Host: {self.host}:{self.port}
Virtual Host: {self.virtual_host}
Exchange: {self.exchange} (direct)
Queue: {self.queue_name}
Routing Key: {self.routing_key}
Username: {self.username}
Source: {os.getenv('MCP_SOURCE', 'claude')}

Connection Settings:
- Connection Timeout: {self.connection_timeout}s
- Heartbeat: {self.heartbeat}s
- Blocked Connection Timeout: {self.blocked_connection_timeout}s"""
        
        return config
    
    def __enter__(self):
        """Context manager entry"""
        self._create_connection()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self._close_connection()


# Global publisher instance
_publisher_instance = None


def get_publisher() -> RabbitMQPublisher:
    """
    Return RabbitMQ publisher instance using singleton pattern
    
    Returns:
        RabbitMQPublisher: Publisher instance
    """
    global _publisher_instance
    if _publisher_instance is None:
        _publisher_instance = RabbitMQPublisher()
    return _publisher_instance


def publish_chat_message(messages: list, 
                        conversation_id: Optional[str] = None,
                        message_type: str = "chat",
                        additional_metadata: Optional[Dict[str, Any]] = None) -> bool:
    """
    Convenient function to publish chat messages
    
    Args:
        messages: List of chat messages
        conversation_id: Conversation ID (optional)
        message_type: Type of message (chat, analysis, etc.)
        additional_metadata: Additional metadata (optional)
        
    Returns:
        bool: Whether publishing was successful
    """
    publisher = get_publisher()
    return publisher.publish_chat_log(messages, conversation_id, message_type, additional_metadata)
