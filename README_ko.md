# MCP Chat Logger

[![smithery badge](https://smithery.ai/badge/@AlexiFeng/MCP_Chat_Logger)](https://smithery.ai/server/@AlexiFeng/MCP_Chat_Logger)

<div align="center">
  <a href="README.md">中文</a> | <a href="README_en.md">English</a>
</div>

---

MCP Chat Logger는 채팅 기록을 Markdown 형식으로 저장하는 간단하면서도 강력한 도구입니다. RabbitMQ를 통한 실시간 메시지 발행 기능도 지원하며, 개발환경과 운영환경을 모두 지원합니다.

## 🚀 빠른 시작

### 1. 프로젝트 설정

```bash
# 저장소 클론
git clone https://github.com/yourusername/MCP_Chat_Logger.git
cd MCP_Chat_Logger

# 의존성 설치
uv add "mcp[cli]>=1.6.0"
uv add "pika>=1.3.0" 
uv add "python-dotenv>=1.0.0"
```

### 2. 환경 선택

이 프로젝트는 **개발환경**과 **운영환경** 두 가지 설정을 지원합니다:

#### 🛠️ 개발환경 (로컬 Docker RabbitMQ)

개발 및 테스트용으로 로컬 Docker를 사용한 RabbitMQ 환경입니다.

```bash
# 환경변수 파일 생성
cp dev-tools/.env.example .env

# Docker로 RabbitMQ 서버 시작
cd dev-tools
docker-compose up -d

# 연결 테스트
uv run test_rabbitmq.py

# MCP 서버 실행
cd ..
uv run chat_logger.py
```

#### ☁️ 운영환경 (CloudAMQP 권장)

실제 서비스 운영을 위해서는 **CloudAMQP**와 같은 관리형 RabbitMQ 서비스 사용을 권장합니다.

```bash
# .env 파일 직접 생성
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

# MCP 서버 실행
uv run chat_logger.py
```

#### 📂 파일 전용 모드 (RabbitMQ 없이)

RabbitMQ 없이 파일 저장만 사용하려는 경우, 환경변수를 설정하지 않으면 자동으로 파일 전용 모드로 실행됩니다:

```bash
# 환경변수 없이 실행 (자동으로 파일 전용 모드)
uv run chat_logger.py
```

### 3. 자동 모드 감지

MCP Chat Logger는 환경변수 설정 여부에 따라 자동으로 모드를 결정합니다:

- **RabbitMQ 모드**: `RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_USERNAME`, `RABBITMQ_PASSWORD` 모두 설정된 경우
- **파일 전용 모드**: 위 환경변수 중 하나라도 없는 경우

```bash
# 실행 (환경변수에 따라 자동으로 모드 결정)
uv run chat_logger.py
```

## 📋 환경별 상세 설정

### 개발환경 설정

#### 환경변수 파일

`dev-tools/.env.example`을 복사하여 `.env` 파일을 생성하세요:

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

#### Docker 명령어

```bash
# RabbitMQ 서버 시작
cd dev-tools
docker-compose up -d

# RabbitMQ 서버 정지
docker-compose down

# 로그 확인
docker-compose logs rabbitmq

# 웹 관리 UI 접속: http://localhost:15672 (guest/guest)
```

#### 개발 도구 실행

```bash
# RabbitMQ 연결 테스트
cd dev-tools
uv run test_rabbitmq.py

# 또는 프로젝트 루트에서
uv run dev-tools/test_rabbitmq.py
```

### 운영환경 설정

#### CloudAMQP 설정 (권장)

1. [CloudAMQP](https://www.cloudamqp.com/) 계정 생성
2. RabbitMQ 인스턴스 생성
3. 연결 정보를 `.env` 파일에 설정

```bash
# CloudAMQP 연결 예시
RABBITMQ_HOST=your-instance.cloudamqp.com
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=your-username
RABBITMQ_PASSWORD=your-password
RABBITMQ_VIRTUAL_HOST=your-vhost
RABBITMQ_EXCHANGE=llmLogger
RABBITMQ_ROUTING_KEY=llm_logger
RABBITMQ_QUEUE_NAME=llm_logger

# 선택적 연결 설정
RABBITMQ_CONNECTION_TIMEOUT=30
RABBITMQ_HEARTBEAT=600
RABBITMQ_BLOCKED_CONNECTION_TIMEOUT=300
```

## 기능 특점

- 🐰 **RabbitMQ 통합**: 실시간 메시지 발행 및 구독 지원
- 📝 **Markdown 저장**: 채팅 기록을 깔끔한 Markdown 형식으로 저장
- ⏰ **타임스탬프**: 각 메시지에 자동으로 타임스탬프 추가
- 📁 **커스텀 디렉토리**: 사용자 정의 저장 디렉토리 지원
- 🔍 **세션 관리**: 세션 ID를 통한 서로 다른 대화 식별 지원
- 🛠️ **환경변수**: `.env` 파일을 통한 설정 관리
- ☁️ **다중 환경**: 개발환경(Docker)과 운영환경(CloudAMQP) 지원

### Exchange 설계

- **Exchange 이름**: `llmLogger`
- **Exchange 타입**: `direct`
- **라우팅 키**: `llm_logger`
- **큐 이름**: `llm_logger`
- **바인딩**: 큐 `llm_logger`가 Exchange `llmLogger`에 라우팅 키 `llm_logger`로 바인딩됨

### 사용 가능한 MCP 도구

**save_chat_history**: 채팅 기록을 Markdown 파일로 저장하고 RabbitMQ로 발행 (환경변수가 설정된 경우)

## Claude Desktop / Cursor 설정

### RabbitMQ 모드 (환경변수 설정)

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

### 파일 전용 모드 (환경변수 없음)

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

## 프로젝트 구조

```
MCP_Chat_Logger/
├── chat_logger.py         # 메인 MCP 서버
├── utils/                 # 유틸리티 모듈
│   └── rabbitmq_publisher.py  # RabbitMQ 메시지 발행 모듈
├── dev-tools/            # 개발환경 도구
│   ├── docker-compose.yml    # RabbitMQ Docker 구성
│   ├── .env.example          # 개발용 환경변수 예시
│   └── test_rabbitmq.py      # RabbitMQ 연결 테스트 스크립트
├── chat_logs/            # 기본 저장 디렉토리
├── pyproject.toml        # 프로젝트 설정 및 의존성
├── .env                  # 환경변수 설정 파일 (사용자 생성)
├── README.md             # 프로젝트 설명 (중문)
├── README_ko.md          # 한국어 설명
├── README_en.md          # 영어 설명
└── .gitignore            # Git 무시 파일
```

## 설치 옵션

### Smithery를 통한 자동 설치

[Smithery](https://smithery.ai/server/@AlexiFeng/MCP_Chat_Logger)를 통해 Claude Desktop용 MCP Chat Logger를 자동으로 설치할 수 있습니다:

```bash
npx -y @smithery/cli install @AlexiFeng/MCP_Chat_Logger --client claude
```

## 다음 단계

- Overview 기능 추가
- 메시지 포맷 커스터마이징 옵션
- 추가 메시지 브로커 지원
- 고가용성 설정 가이드

## 기여 방법

문제 제기와 풀 리퀘스트를 환영합니다! 코드 기여를 원하시면 다음 단계를 따라주세요:

1. 이 저장소를 Fork하세요
2. 기능 브랜치를 생성하세요 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋하세요 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시하세요 (`git push origin feature/amazing-feature`)
5. Pull Request를 열어주세요

## 라이센스

이 프로젝트는 MIT 라이센스 하에 있습니다 - 자세한 내용은 LICENSE 파일을 참조하세요. 