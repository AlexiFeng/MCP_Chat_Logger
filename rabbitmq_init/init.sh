#!/bin/bash
# RabbitMQ 초기화 스크립트
# Docker 컨테이너 시작시 자동으로 Exchange와 Queue를 설정합니다.

set -e

# RabbitMQ가 완전히 시작될 때까지 대기
sleep 10

echo "🔧 RabbitMQ 초기 설정 시작..."

# Exchange 생성
rabbitmqadmin declare exchange name=llmLogger type=direct durable=true

# Queue 생성
rabbitmqadmin declare queue name=llm_logger durable=true

# Queue를 Exchange에 바인딩
rabbitmqadmin declare binding source=llmLogger destination=llm_logger routing_key=llm_logger

echo "✅ RabbitMQ 초기 설정 완료!"
echo "📊 Exchange: llmLogger (direct)"
echo "📦 Queue: llm_logger"
echo "🔗 Binding: llm_logger -> llmLogger (routing_key: llm_logger)"
