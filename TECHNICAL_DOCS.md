# Technical Documentation - Đấu Trường Tri Thức
**Brain Arena: Only the Smart Survive**

## 1. Technology Stack

### 1.1 Frontend
- **HTML5**: Cấu trúc web
- **CSS3**: Styling, animations
- **JavaScript (ES6+)**: Logic game
- **Framework**: React hoặc Vue.js (recommended)
- **WebSocket Client**: Socket.IO client cho PvP real-time

### 1.2 Backend
- **Language**: Python 3.12+
- **Framework**: FastAPI (async, high performance)
- **WebSocket**: FastAPI WebSocket hoặc Socket.IO Python
- **Task Queue**: Celery + Redis (cho background tasks)

### 1.3 Database
- **Primary Database**: MySQL 8.0+
  - User profiles
  - Game history
  - Leaderboard
  - Purchases & subscriptions
- **Cache**: Redis 7.0+
  - Session management
  - Leaderboard cache
  - Matchmaking queue
  - AI response cache

### 1.4 AI Services

#### AI Question Generator
- **API**: Google Gemini API
- **Alternative**: OpenAI GPT-4, Claude API
- **Purpose**: Tạo câu hỏi trắc nghiệm tự động

#### AI Hint Generator
- **API**: Google Gemini API
- **Purpose**: Phân tích câu hỏi và đưa ra gợi ý thông minh

#### AI Voice (TTS)
- **Engine**: [VieNeu-TTS](https://github.com/kratosvn/VieNeu-TTS)
- **Features**:
  - Vietnamese TTS with instant voice cloning
  - On-device inference
  - Real-time CPU inference
  - 24kHz audio quality
- **Model**: Qwen 0.5B LLM + NeuCodec
- **Training Data**: VieNeu-TTS-1000h (443,641 Vietnamese samples)
- **Deployment**: 
  - GGUF Q4/Q8 quantized models cho CPU
  - Gradio web UI hoặc Python API

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────┐
│   Frontend  │ (React/Vue.js)
│   (Browser) │
└──────┬──────┘
       │ HTTP/WebSocket
       ↓
┌─────────────────────────────────┐
│      FastAPI Backend            │
│  ┌──────────┬────────────────┐  │
│  │ REST API │ WebSocket API  │  │
│  └──────────┴────────────────┘  │
│  ┌──────────┬────────────────┐  │
│  │ Auth     │ Game Logic     │  │
│  │ Service  │ Service        │  │
│  └──────────┴────────────────┘  │
│  ┌──────────┬────────────────┐  │
│  │ AI       │ Payment        │  │
│  │ Service  │ Service        │  │
│  └──────────┴────────────────┘  │
└────────┬────────────────────┬───┘
         │                    │
    ┌────▼────┐         ┌────▼────┐
    │  MySQL  │         │  Redis  │
    │Database │         │  Cache  │
    └─────────┘         └─────────┘
         │
    ┌────▼─────────────────────┐
    │  External Services       │
    │  - Gemini API            │
    │  - VieNeu-TTS            │
    │  - Payment Gateway       │
    └──────────────────────────┘
```

### 2.2 Component Details

#### FastAPI Backend Structure
```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration
│   ├── database.py          # MySQL connection
│   ├── redis_client.py      # Redis connection
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── game.py
│   │   ├── question.py
│   │   └── purchase.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── user.py
│   │   ├── game.py
│   │   └── ai.py
│   ├── api/                 # API routes
│   │   ├── auth.py
│   │   ├── game.py
│   │   ├── ai.py
│   │   ├── pvp.py
│   │   ├── shop.py
│   │   └── leaderboard.py
│   ├── services/            # Business logic
│   │   ├── auth_service.py
│   │   ├── game_service.py
│   │   ├── ai_service.py
│   │   ├── tts_service.py
│   │   └── payment_service.py
│   ├── websocket/           # WebSocket handlers
│   │   └── pvp_handler.py
│   └── utils/               # Utilities
│       ├── security.py
│       └── helpers.py
├── requirements.txt
└── .env
```

---

## 3. Database Schema (MySQL)

### 3.1 Users Table
```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  display_name VARCHAR(100),
  avatar_url VARCHAR(255),
  elo_rating INT DEFAULT 1000,
  rank VARCHAR(20) DEFAULT 'Đồng',
  level INT DEFAULT 1,
  total_games INT DEFAULT 0,
  wins INT DEFAULT 0,
  losses INT DEFAULT 0,
  highest_score BIGINT DEFAULT 0,
  perfect_games INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_username (username),
  INDEX idx_email (email),
  INDEX idx_elo_rating (elo_rating DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3.2 Games Table
```sql
CREATE TABLE games (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  game_mode VARCHAR(20), -- 'solo', 'pvp'
  score BIGINT,
  questions_answered INT,
  correct_answers INT,
  helps_used JSON, -- {"50_50": true, "ai_hint": 2, "time_freeze": true, "swap": true}
  duration_seconds INT,
  opponent_id INT, -- NULL nếu solo
  result VARCHAR(10), -- 'win', 'lose', 'quit'
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (opponent_id) REFERENCES users(id) ON DELETE SET NULL,
  INDEX idx_user_id (user_id),
  INDEX idx_created_at (created_at DESC),
  INDEX idx_game_mode (game_mode)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3.3 Questions Table
```sql
CREATE TABLE questions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  question_text TEXT NOT NULL,
  answers JSON NOT NULL, -- [{"id": "A", "text": "...", "correct": true}, ...]
  category VARCHAR(50),
  difficulty VARCHAR(20), -- 'easy', 'medium', 'hard'
  level INT, -- 1-15
  source VARCHAR(20), -- 'ai_generated', 'manual'
  explanation TEXT,
  times_used INT DEFAULT 0,
  correct_rate FLOAT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_level (level),
  INDEX idx_difficulty (difficulty),
  INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3.4 Leaderboard Table
```sql
CREATE TABLE leaderboard (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT UNIQUE NOT NULL,
  rank INT,
  score BIGINT,
  elo_rating INT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_elo_rating (elo_rating DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3.5 Purchases Table
```sql
CREATE TABLE purchases (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  package_type VARCHAR(20), -- 'ai_hint_basic', 'ai_hint_pro', 'ai_hint_vip'
  amount INT, -- Số lượng (3, 10, hoặc unlimited)
  price DECIMAL(10,2),
  payment_method VARCHAR(50), -- 'momo', 'zalopay', 'vnpay', 'card'
  transaction_id VARCHAR(100) UNIQUE,
  status VARCHAR(20), -- 'pending', 'completed', 'failed'
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP NULL, -- NULL nếu không hết hạn
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_user_id (user_id),
  INDEX idx_status (status),
  INDEX idx_transaction_id (transaction_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3.6 User Credits Table
```sql
CREATE TABLE user_credits (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT UNIQUE NOT NULL,
  ai_hint_credits INT DEFAULT 0,
  is_vip BOOLEAN DEFAULT FALSE,
  vip_expires_at TIMESTAMP NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3.7 Voice Subscriptions Table
```sql
CREATE TABLE voice_subscriptions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  voice_id VARCHAR(50), -- 'lai_van_sam', 'giao_su_xoay', 'phan_dang', 'all_voices'
  voice_name VARCHAR(100),
  price DECIMAL(10,2),
  expires_at TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  UNIQUE KEY unique_user_voice (user_id, voice_id),
  INDEX idx_user_id (user_id),
  INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 3.8 Achievements Table
```sql
CREATE TABLE achievements (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  achievement_type VARCHAR(50), -- 'first_win', 'perfect_game', '10_win_streak', etc.
  unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  UNIQUE KEY unique_user_achievement (user_id, achievement_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 4. Redis Cache Structure

```python
# Matchmaking Queue
"matchmaking:queue:ranked" → List[user_id]

# Active Games
"game:active:{game_id}" → {
    "players": [user_id1, user_id2],
    "current_question": 5,
    "scores": {user_id1: 3000000, user_id2: 2000000}
}

# User Session
"session:{user_id}" → {
    "token": "jwt_token",
    "last_active": timestamp
}

# Leaderboard Cache (TTL: 5 minutes)
"leaderboard:global" → Sorted Set by ELO (Top 100)

# AI Response Cache (TTL: 1 hour)
"ai:question:{category}:{level}:{difficulty}" → question_json
"ai:hint:{question_id}" → hint_json
```

---

## 5. API Endpoints

### 5.1 Authentication
```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
GET    /api/auth/profile
```

### 5.2 Game
```
POST   /api/game/start
POST   /api/game/answer
POST   /api/game/use-help
POST   /api/game/quit
GET    /api/game/history
```

### 5.3 AI Features
```
POST   /api/ai/generate-question
POST   /api/ai/hint
POST   /api/ai/chat
POST   /api/ai/voice/synthesize
GET    /api/ai/voice/list
GET    /api/ai/voice/subscriptions
```

### 5.4 PvP
```
POST   /api/pvp/matchmaking
POST   /api/pvp/challenge
GET    /api/pvp/active-games
POST   /api/pvp/tournament/join
```

### 5.5 Leaderboard
```
GET    /api/leaderboard
GET    /api/leaderboard/:user_id
```

### 5.6 Shop & Payment
```
GET    /api/shop/packages
POST   /api/shop/purchase
GET    /api/shop/history
POST   /api/payment/momo
POST   /api/payment/zalopay
POST   /api/payment/vnpay
GET    /api/payment/verify
```

---

## 6. AI Services Implementation

### 6.1 AI Question Generator Service

```python
# services/ai_service.py
import google.generativeai as genai
from typing import Dict, List
import json

class AIQuestionService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_question(
        self, 
        level: int, 
        difficulty: str, 
        category: str
    ) -> Dict:
        prompt = f"""
        Tạo 1 câu hỏi trắc nghiệm tiếng Việt:
        - Độ khó: {difficulty}
        - Chủ đề: {category}
        - Level: {level}
        
        Format JSON:
        {{
            "question": "Câu hỏi ở đây?",
            "answers": [
                {{"id": "A", "text": "Đáp án A", "correct": true}},
                {{"id": "B", "text": "Đáp án B", "correct": false}},
                {{"id": "C", "text": "Đáp án C", "correct": false}},
                {{"id": "D", "text": "Đáp án D", "correct": false}}
            ],
            "explanation": "Giải thích ngắn gọn"
        }}
        """
        
        response = await self.model.generate_content_async(prompt)
        question_data = json.loads(response.text)
        
        return question_data
```

### 6.2 AI Hint Service

```python
class AIHintService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_hint(
        self, 
        question: str, 
        answers: List[Dict]
    ) -> Dict:
        prompt = f"""
        Phân tích câu hỏi và đưa ra gợi ý thông minh:
        
        Câu hỏi: {question}
        Đáp án: {json.dumps(answers, ensure_ascii=False)}
        
        Hãy:
        1. Loại bỏ 1 đáp án sai chắc chắn
        2. Giải thích ngắn gọn (1-2 câu) tại sao
        3. Đưa ra độ tin cậy (70-95%)
        
        Format JSON:
        {{
            "eliminate": "C",
            "explanation": "Đáp án C có thể loại bỏ vì...",
            "confidence": 85
        }}
        """
        
        response = await self.model.generate_content_async(prompt)
        hint_data = json.loads(response.text)
        
        return hint_data
```

### 6.3 TTS Service (VieNeu-TTS)

```python
# services/tts_service.py
import torch
from vieneu_tts import VieNeuTTS
import numpy as np

class TTSService:
    def __init__(self, model_path: str):
        self.model = VieNeuTTS.from_pretrained(model_path)
        self.model.eval()
    
    async def synthesize(
        self, 
        text: str, 
        voice_id: str,
        speed: float = 1.0
    ) -> bytes:
        """
        Synthesize speech from text using VieNeu-TTS
        
        Args:
            text: Text to synthesize
            voice_id: Voice ID (e.g., 'nam_mien_bac_1', 'lai_van_sam')
            speed: Speech speed (0.8-1.2)
        
        Returns:
            Audio bytes (WAV format)
        """
        # Load reference voice
        reference_audio = self._load_reference_voice(voice_id)
        
        # Generate speech
        with torch.no_grad():
            audio = self.model.generate(
                text=text,
                reference_audio=reference_audio,
                speed=speed
            )
        
        # Convert to WAV bytes
        audio_bytes = self._to_wav_bytes(audio)
        
        return audio_bytes
    
    def _load_reference_voice(self, voice_id: str) -> np.ndarray:
        """Load reference voice sample for cloning"""
        voice_path = f"voices/{voice_id}.wav"
        # Load and return audio
        pass
    
    def _to_wav_bytes(self, audio: np.ndarray) -> bytes:
        """Convert audio array to WAV bytes"""
        # Convert to WAV format
        pass
```

---

## 7. WebSocket Implementation (PvP)

```python
# websocket/pvp_handler.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List

class PvPConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.matchmaking_queue: List[str] = []
    
    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    
    async def join_matchmaking(self, user_id: str):
        self.matchmaking_queue.append(user_id)
        
        # If 2 players in queue, create match
        if len(self.matchmaking_queue) >= 2:
            player1 = self.matchmaking_queue.pop(0)
            player2 = self.matchmaking_queue.pop(0)
            
            await self._create_match(player1, player2)
    
    async def _create_match(self, player1_id: str, player2_id: str):
        game_id = f"game_{player1_id}_{player2_id}"
        
        # Notify both players
        await self.send_to_user(player1_id, {
            "type": "match_found",
            "opponent_id": player2_id,
            "game_id": game_id
        })
        
        await self.send_to_user(player2_id, {
            "type": "match_found",
            "opponent_id": player1_id,
            "game_id": game_id
        })
    
    async def send_to_user(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_json(message)

manager = PvPConnectionManager()

@app.websocket("/ws/pvp/{user_id}")
async def pvp_websocket(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "join_matchmaking":
                await manager.join_matchmaking(user_id)
            
            elif data["type"] == "answer_question":
                # Handle answer submission
                pass
                
    except WebSocketDisconnect:
        manager.disconnect(user_id)
```

---

## 8. Security & Performance

### 8.1 Security

#### JWT Authentication
```python
# utils/security.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

#### Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/ai/generate-question")
@limiter.limit("10/minute")  # Max 10 requests per minute
async def generate_question(request: Request):
    pass
```

### 8.2 Performance Optimization

#### Database Connection Pooling
```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

#### Redis Caching
```python
# Decorator for caching
def cache_result(ttl: int = 3600):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            
            # Try to get from cache
            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            await redis.setex(cache_key, ttl, json.dumps(result))
            
            return result
        return wrapper
    return decorator

@cache_result(ttl=3600)
async def get_leaderboard():
    # Expensive database query
    pass
```

---

## 9. Deployment

### 9.1 Docker Setup

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+aiomysql://user:pass@mysql:3306/game_db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - mysql
      - redis
  
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: game_db
      MYSQL_USER: user
      MYSQL_PASSWORD: pass
    volumes:
      - mysql_data:/var/lib/mysql
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  mysql_data:
  redis_data:
```

### 9.2 Environment Variables

```bash
# .env
DATABASE_URL=mysql+aiomysql://user:pass@localhost:3306/game_db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
MOMO_API_KEY=your-momo-key
ZALOPAY_API_KEY=your-zalopay-key
VNPAY_API_KEY=your-vnpay-key
```

---

## 10. Infrastructure Costs

### Monthly Estimate
- **Hosting**: $20-50 (DigitalOcean/AWS/GCP)
- **Database (MySQL)**: $15-30 (Managed MySQL)
- **Redis**: $10-20 (Managed Redis)
- **AI API (Gemini)**: $50-200 (depends on usage)
- **TTS (VieNeu-TTS)**: $0 (self-hosted) hoặc $30-100 (cloud GPU)
- **CDN**: $10-20 (Cloudflare/BunnyCDN)
- **Payment Gateway**: 2-3% per transaction

**Total Fixed**: ~$130-400/month
**Total Variable**: Depends on traffic and transactions

---

## 11. Development Setup

### 11.1 Prerequisites
```bash
# Python 3.12+
python --version

# MySQL 8.0+
mysql --version

# Redis 7.0+
redis-cli --version
```

### 11.2 Installation

```bash
# Clone repository
git clone <repo-url>
cd brain-arena

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
mysql -u root -p < database/schema.sql

# Run migrations
alembic upgrade head

# Start Redis
redis-server

# Run development server
uvicorn app.main:app --reload
```

### 11.3 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_game_service.py
```

---

**Version**: 1.0  
**Last Updated**: 2025-12-28  
**Tech Stack**: Python + FastAPI + MySQL + Redis + VieNeu-TTS
