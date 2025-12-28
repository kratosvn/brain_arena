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
- **Framework**: Django 5.0+ (with Django REST Framework)
- **Admin Panel**: Django Admin (built-in)
- **WebSocket**: Django Channels
- **Task Queue**: Celery + Redis (cho background tasks)
- **API**: Django REST Framework (DRF)

**Lý do chọn Django:**
- ✅ Django Admin mạnh mẽ cho quản lý câu hỏi, người chơi
- ✅ ORM tốt, dễ quản lý database
- ✅ Authentication & Permission system có sẵn
- ✅ Ecosystem lớn, nhiều packages
- ✅ Phù hợp cho vận hành và scale

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
│      Django Backend             │
│  ┌──────────┬────────────────┐  │
│  │ Django   │ Django         │  │
│  │ Admin    │ REST Framework │  │
│  └──────────┴────────────────┘  │
│  ┌──────────┬────────────────┐  │
│  │ Django   │ Django         │  │
│  │ Channels │ Celery Tasks   │  │
│  └──────────┴────────────────┘  │
│  ┌──────────┬────────────────┐  │
│  │ Business │ AI Services    │  │
│  │ Logic    │                │  │
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

#### Django Project Structure
```
brain_arena/
├── manage.py
├── config/                  # Project settings
│   ├── __init__.py
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py             # For Django Channels
├── apps/
│   ├── users/              # User management
│   │   ├── models.py
│   │   ├── admin.py        # Django Admin config
│   │   ├── views.py
│   │   ├── serializers.py  # DRF serializers
│   │   └── urls.py
│   ├── questions/          # Question bank management
│   │   ├── models.py
│   │   ├── admin.py        # Admin for questions
│   │   ├── views.py
│   │   └── management/
│   │       └── commands/   # Custom commands
│   ├── games/              # Game logic
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── views.py
│   │   └── services.py
│   ├── shop/               # Shop & payments
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── views.py
│   │   └── payment_gateways.py
│   ├── ai/                 # AI services
│   │   ├── services/
│   │   │   ├── question_generator.py
│   │   │   ├── hint_generator.py
│   │   │   └── tts_service.py
│   │   └── views.py
│   └── pvp/                # PvP & WebSocket
│       ├── consumers.py    # Django Channels consumers
│       ├── routing.py
│       └── services.py
├── static/
├── media/
├── templates/
│   └── admin/              # Custom admin templates
└── requirements.txt
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

## 4. Django Admin Configuration

### 4.1 Questions Admin

```python
# apps/questions/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Question, Category

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_preview', 'category', 'difficulty', 'level', 'source', 'times_used', 'correct_rate_display', 'created_at']
    list_filter = ['category', 'difficulty', 'level', 'source', 'created_at']
    search_fields = ['question_text', 'id']
    readonly_fields = ['times_used', 'correct_rate', 'created_at']
    
    fieldsets = (
        ('Câu Hỏi', {
            'fields': ('question_text', 'category', 'difficulty', 'level')
        }),
        ('Đáp Án', {
            'fields': ('answer_a', 'answer_b', 'answer_c', 'answer_d', 'correct_answer')
        }),
        ('Metadata', {
            'fields': ('source', 'explanation', 'times_used', 'correct_rate', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def question_preview(self, obj):
        return obj.question_text[:100] + '...' if len(obj.question_text) > 100 else obj.question_text
    question_preview.short_description = 'Câu hỏi'
    
    def correct_rate_display(self, obj):
        if obj.correct_rate is None:
            return '-'
        color = 'green' if obj.correct_rate > 70 else 'orange' if obj.correct_rate > 50 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, obj.correct_rate
        )
    correct_rate_display.short_description = 'Tỷ lệ đúng'
    
    actions = ['mark_as_ai_generated', 'mark_as_manual', 'export_to_json']
    
    def mark_as_ai_generated(self, request, queryset):
        updated = queryset.update(source='ai_generated')
        self.message_user(request, f'{updated} câu hỏi đã được đánh dấu là AI generated')
    mark_as_ai_generated.short_description = 'Đánh dấu là AI generated'
    
    def export_to_json(self, request, queryset):
        # Export logic here
        pass
    export_to_json.short_description = 'Export to JSON'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'question_count', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Số câu hỏi'
```

### 4.2 Users Admin

```python
# apps/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserCredits

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'display_name', 'elo_rating', 'rank', 'total_games', 'win_rate', 'is_vip', 'created_at']
    list_filter = ['rank', 'is_staff', 'is_superuser', 'created_at']
    search_fields = ['username', 'email', 'display_name']
    readonly_fields = ['created_at', 'updated_at', 'last_login']
    
    fieldsets = (
        ('Thông Tin Cơ Bản', {
            'fields': ('username', 'email', 'password', 'display_name', 'avatar')
        }),
        ('Game Stats', {
            'fields': ('elo_rating', 'rank', 'level', 'total_games', 'wins', 'losses', 'highest_score', 'perfect_games')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def win_rate(self, obj):
        if obj.total_games == 0:
            return '0%'
        rate = (obj.wins / obj.total_games) * 100
        return f'{rate:.1f}%'
    win_rate.short_description = 'Win Rate'
    
    def is_vip(self, obj):
        try:
            return obj.credits.is_vip
        except:
            return False
    is_vip.boolean = True
    is_vip.short_description = 'VIP'
    
    actions = ['grant_vip', 'revoke_vip', 'reset_elo']
    
    def grant_vip(self, request, queryset):
        from datetime import timedelta
        from django.utils import timezone
        
        for user in queryset:
            credits, created = UserCredits.objects.get_or_create(user=user)
            credits.is_vip = True
            credits.vip_expires_at = timezone.now() + timedelta(days=30)
            credits.save()
        
        self.message_user(request, f'{queryset.count()} người dùng đã được cấp VIP')
    grant_vip.short_description = 'Cấp VIP (30 ngày)'

@admin.register(UserCredits)
class UserCreditsAdmin(admin.ModelAdmin):
    list_display = ['user', 'ai_hint_credits', 'is_vip', 'vip_expires_at', 'updated_at']
    list_filter = ['is_vip']
    search_fields = ['user__username', 'user__email']
    raw_id_fields = ['user']
```

### 4.3 Games Admin

```python
# apps/games/admin.py
from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'game_mode', 'score_display', 'questions_answered', 'correct_answers', 'accuracy', 'result', 'created_at']
    list_filter = ['game_mode', 'result', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at']
    raw_id_fields = ['user', 'opponent']
    date_hierarchy = 'created_at'
    
    def score_display(self, obj):
        return f'{obj.score:,} VNĐ'
    score_display.short_description = 'Score'
    
    def accuracy(self, obj):
        if obj.questions_answered == 0:
            return '0%'
        acc = (obj.correct_answers / obj.questions_answered) * 100
        return f'{acc:.1f}%'
    accuracy.short_description = 'Độ chính xác'
    
    def has_add_permission(self, request):
        return False  # Không cho phép tạo game từ admin
```

### 4.4 Shop Admin

```python
# apps/shop/admin.py
from django.contrib import admin
from .models import Purchase, Package, VoiceSubscription

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'package_type', 'price_display', 'credits', 'is_active', 'sales_count']
    list_filter = ['package_type', 'is_active']
    search_fields = ['name', 'description']
    
    def price_display(self, obj):
        return f'{obj.price:,} VNĐ'
    price_display.short_description = 'Giá'
    
    def sales_count(self, obj):
        return obj.purchases.filter(status='completed').count()
    sales_count.short_description = 'Đã bán'

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'package', 'price_display', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['user__username', 'transaction_id']
    readonly_fields = ['transaction_id', 'created_at']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Thông Tin Giao Dịch', {
            'fields': ('user', 'package', 'price', 'payment_method', 'transaction_id')
        }),
        ('Trạng Thái', {
            'fields': ('status', 'created_at', 'expires_at')
        }),
    )
    
    def price_display(self, obj):
        return f'{obj.price:,} VNĐ'
    price_display.short_description = 'Giá'
    
    actions = ['mark_as_completed', 'mark_as_failed']
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} giao dịch đã được đánh dấu hoàn thành')
    mark_as_completed.short_description = 'Đánh dấu hoàn thành'

@admin.register(VoiceSubscription)
class VoiceSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'voice_name', 'price_display', 'is_active', 'expires_at', 'created_at']
    list_filter = ['voice_id', 'is_active', 'created_at']
    search_fields = ['user__username', 'voice_name']
    raw_id_fields = ['user']
    
    def price_display(self, obj):
        return f'{obj.price:,} VNĐ/tháng'
    price_display.short_description = 'Giá'
```

### 4.5 Custom Admin Dashboard

```python
# config/admin.py
from django.contrib import admin
from django.utils.html import format_html

admin.site.site_header = 'Đấu Trường Tri Thức - Admin'
admin.site.site_title = 'Brain Arena Admin'
admin.site.index_title = 'Quản Lý Hệ Thống'

# Custom admin index view
from django.contrib.admin import AdminSite
from django.shortcuts import render

class CustomAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        from apps.users.models import User
        from apps.games.models import Game
        from apps.questions.models import Question
        from apps.shop.models import Purchase
        from django.utils import timezone
        from datetime import timedelta
        
        # Statistics
        stats = {
            'total_users': User.objects.count(),
            'active_users_today': User.objects.filter(
                last_login__gte=timezone.now() - timedelta(days=1)
            ).count(),
            'total_games': Game.objects.count(),
            'games_today': Game.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=1)
            ).count(),
            'total_questions': Question.objects.count(),
            'ai_questions': Question.objects.filter(source='ai_generated').count(),
            'revenue_today': Purchase.objects.filter(
                status='completed',
                created_at__gte=timezone.now() - timedelta(days=1)
            ).aggregate(total=models.Sum('price'))['total'] or 0,
        }
        
        extra_context = extra_context or {}
        extra_context['stats'] = stats
        
        return super().index(request, extra_context)

# Use custom admin site
admin_site = CustomAdminSite(name='custom_admin')
```

---

## 5. Redis Cache Structure

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
# apps/ai/services/question_generator.py
import google.generativeai as genai
from typing import Dict
import json
from django.conf import settings

class AIQuestionService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_question(
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
        
        response = self.model.generate_content(prompt)
        question_data = json.loads(response.text)
        
        return question_data

# apps/ai/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.question_generator import AIQuestionService

class GenerateQuestionView(APIView):
    def post(self, request):
        level = request.data.get('level')
        difficulty = request.data.get('difficulty')
        category = request.data.get('category')
        
        service = AIQuestionService()
        question = service.generate_question(level, difficulty, category)
        
        return Response(question, status=status.HTTP_200_OK)
```

### 6.2 AI Hint Service

```python
# apps/ai/services/hint_generator.py
class AIHintService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_hint(
        self, 
        question: str, 
        answers: list
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
        
        response = self.model.generate_content(prompt)
        hint_data = json.loads(response.text)
        
        return hint_data
```

### 6.3 TTS Service (VieNeu-TTS)

```python
# apps/ai/services/tts_service.py
import torch
from vieneu_tts import VieNeuTTS
import numpy as np
from django.conf import settings

class TTSService:
    def __init__(self):
        self.model = VieNeuTTS.from_pretrained(settings.VIENEU_TTS_MODEL_PATH)
        self.model.eval()
    
    def synthesize(
        self, 
        text: str, 
        voice_id: str,
        speed: float = 1.0
    ) -> bytes:
        """
        Synthesize speech from text using VieNeu-TTS
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
        voice_path = f"{settings.MEDIA_ROOT}/voices/{voice_id}.wav"
        # Load and return audio
        pass
    
    def _to_wav_bytes(self, audio: np.ndarray) -> bytes:
        """Convert audio array to WAV bytes"""
        pass
```

---

## 7. WebSocket Implementation (Django Channels)

```python
# apps/pvp/consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from typing import Dict, List
import json

class PvPConsumer(AsyncJsonWebsocketConsumer):
    matchmaking_queue = []
    active_games = {}
    
    async def connect(self):
        self.user = self.scope['user']
        self.user_id = str(self.user.id)
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        await self.accept()
        
        # Add to user's personal channel
        await self.channel_layer.group_add(
            f'user_{self.user_id}',
            self.channel_name
        )
    
    async def disconnect(self, close_code):
        # Remove from matchmaking queue if present
        if self.user_id in self.matchmaking_queue:
            self.matchmaking_queue.remove(self.user_id)
        
        # Leave user's personal channel
        await self.channel_layer.group_discard(
            f'user_{self.user_id}',
            self.channel_name
        )
    
    async def receive_json(self, content):
        message_type = content.get('type')
        
        if message_type == 'join_matchmaking':
            await self.join_matchmaking()
        
        elif message_type == 'answer_question':
            await self.handle_answer(content)
        
        elif message_type == 'use_help':
            await self.handle_help(content)
    
    async def join_matchmaking(self):
        """Add user to matchmaking queue"""
        if self.user_id not in self.matchmaking_queue:
            self.matchmaking_queue.append(self.user_id)
        
        # If 2 players in queue, create match
        if len(self.matchmaking_queue) >= 2:
            player1_id = self.matchmaking_queue.pop(0)
            player2_id = self.matchmaking_queue.pop(0)
            
            await self.create_match(player1_id, player2_id)
    
    async def create_match(self, player1_id: str, player2_id: str):
        """Create a new PvP match"""
        game_id = f"game_{player1_id}_{player2_id}"
        
        # Create game in database
        game = await self.create_game_db(player1_id, player2_id)
        
        # Store in active games
        self.active_games[game_id] = {
            'players': [player1_id, player2_id],
            'current_question': 1,
            'scores': {player1_id: 0, player2_id: 0}
        }
        
        # Notify both players
        await self.channel_layer.group_send(
            f'user_{player1_id}',
            {
                'type': 'match_found',
                'opponent_id': player2_id,
                'game_id': game_id
            }
        )
        
        await self.channel_layer.group_send(
            f'user_{player2_id}',
            {
                'type': 'match_found',
                'opponent_id': player1_id,
                'game_id': game_id
            }
        )
    
    async def match_found(self, event):
        """Send match found notification to client"""
        await self.send_json({
            'type': 'match_found',
            'opponent_id': event['opponent_id'],
            'game_id': event['game_id']
        })
    
    async def handle_answer(self, content):
        """Handle player's answer"""
        game_id = content.get('game_id')
        answer = content.get('answer')
        
        # Process answer logic here
        pass
    
    @database_sync_to_async
    def create_game_db(self, player1_id, player2_id):
        """Create game record in database"""
        from apps.games.models import Game
        from apps.users.models import User
        
        player1 = User.objects.get(id=player1_id)
        player2 = User.objects.get(id=player2_id)
        
        game = Game.objects.create(
            user=player1,
            opponent=player2,
            game_mode='pvp'
        )
        
        return game

# apps/pvp/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/pvp/', consumers.PvPConsumer.as_asgi()),
]

# config/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.pvp import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
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

## 12. Platform Deployment

### 12.1 Facebook Instant Games (Priority 1) 🎮

#### Overview
Facebook Instant Games là nền tảng tốt nhất để bắt đầu:
- ✅ Open platform (không cần partnership)
- ✅ Dễ submit và publish
- ✅ Global reach (2.9B users)
- ✅ Built-in monetization
- ✅ Viral features (share, challenge)

#### Requirements

**Technical Requirements:**
```
- HTML5 game
- Bundle size < 5MB (initial load)
- HTTPS hosting
- Mobile-first design
- No external dependencies
```

**Developer Requirements:**
```
1. Facebook Developer Account
2. App ID
3. Business verification (for monetization)
```

#### Setup Steps

**1. Create Facebook App**
```bash
# Visit: https://developers.facebook.com/apps/
# Create New App → Gaming → Instant Game
```

**2. Install Facebook SDK**
```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Đấu Trường Tri Thức</title>
    <script src="https://connect.facebook.net/en_US/fbinstant.7.1.js"></script>
</head>
<body>
    <div id="game-container"></div>
    <script src="game.js"></script>
</body>
</html>
```

**3. Initialize SDK**
```javascript
// game.js
let playerName = '';
let playerPhoto = '';

// Initialize Facebook Instant Games
FBInstant.initializeAsync()
  .then(() => {
    console.log('FB Instant Games initialized');
    
    // Show loading progress
    FBInstant.setLoadingProgress(50);
    
    // Load game assets
    return loadGameAssets();
  })
  .then(() => {
    FBInstant.setLoadingProgress(100);
    
    // Start game
    return FBInstant.startGameAsync();
  })
  .then(() => {
    // Get player info
    playerName = FBInstant.player.getName();
    playerPhoto = FBInstant.player.getPhoto();
    
    // Start game logic
    startGame();
  })
  .catch(err => {
    console.error('Initialization error:', err);
  });

function loadGameAssets() {
  // Load your game assets here
  return new Promise((resolve) => {
    // Simulate loading
    setTimeout(resolve, 1000);
  });
}

function startGame() {
  console.log(`Welcome ${playerName}!`);
  // Your game logic here
}
```

**4. Implement Core Features**

```javascript
// Share Score
function shareScore(score) {
  FBInstant.shareAsync({
    intent: 'CHALLENGE',
    image: getBase64Screenshot(), // Your game screenshot
    text: `Tôi đã đạt ${score.toLocaleString()} VNĐ! Bạn có thắng được tôi không?`,
    data: { score: score }
  }).then(() => {
    console.log('Shared successfully');
  });
}

// Leaderboard
function updateLeaderboard(score) {
  FBInstant.getLeaderboardAsync('global_leaderboard')
    .then(leaderboard => {
      return leaderboard.setScoreAsync(score);
    })
    .then(() => {
      console.log('Score updated');
    });
}

// Get Leaderboard
function getLeaderboard() {
  FBInstant.getLeaderboardAsync('global_leaderboard')
    .then(leaderboard => {
      return leaderboard.getEntriesAsync(10, 0);
    })
    .then(entries => {
      entries.forEach(entry => {
        console.log(`${entry.getRank()}. ${entry.getPlayer().getName()}: ${entry.getScore()}`);
      });
    });
}

// Rewarded Ads (Monetization)
function showRewardedAd() {
  FBInstant.getRewardedVideoAsync('your-placement-id')
    .then(rewarded => {
      return rewarded.showAsync();
    })
    .then(() => {
      // Give reward (e.g., 1 AI Hint)
      giveReward('ai_hint', 1);
    })
    .catch(err => {
      console.error('Ad error:', err);
    });
}

// In-App Purchase
function purchaseAIHint() {
  FBInstant.payments.purchaseAsync({
    productID: 'ai_hint_pro',
    developerPayload: 'user_123'
  }).then(purchase => {
    console.log('Purchase successful:', purchase);
    // Grant AI Hint credits
    grantAIHintCredits(10);
  });
}
```

**5. Build & Upload**

```bash
# Build production bundle
npm run build

# Create ZIP file (< 5MB)
cd dist
zip -r game.zip *

# Upload to Facebook:
# 1. Go to your app dashboard
# 2. Instant Games → Web Hosting
# 3. Upload game.zip
# 4. Test in Instant Games Player
```

**6. Testing**

```bash
# Test URL format:
https://www.facebook.com/embed/instantgames/YOUR_APP_ID/player?game_url=https://localhost:8080

# Or use Facebook Instant Games SDK Tester
# Download: https://developers.facebook.com/docs/games/instant-games/test-publish-share
```

#### Monetization Options

```javascript
// 1. Interstitial Ads
FBInstant.getInterstitialAdAsync('your-placement-id')
  .then(interstitial => interstitial.showAsync())
  .catch(err => console.error(err));

// 2. Rewarded Video (recommended for free AI Hints)
// See showRewardedAd() above

// 3. In-App Purchases
// See purchaseAIHint() above

// 4. Subscriptions (for VIP)
FBInstant.payments.purchaseAsync({
  productID: 'vip_monthly',
  developerPayload: 'user_123'
});
```

---

### 12.2 Zalo Mini Game (Priority 2) 🇻🇳

#### Overview
Zalo Mini Game là platform tốt nhất cho thị trường Việt Nam:
- ✅ 70M+ users tại VN
- ✅ ZaloPay integration sẵn có
- ✅ Viral trong cộng đồng VN
- ✅ Dễ monetize với VN users

#### Requirements

**Technical Requirements:**
```
- HTML5 game
- Zalo Mini App SDK
- HTTPS hosting
- Mobile-first (Zalo chủ yếu mobile)
```

**Developer Requirements:**
```
1. Zalo Developer Account
2. Business verification
3. App registration
```

#### Setup Steps

**1. Register Zalo Mini App**
```bash
# Visit: https://mini.zalo.me/
# Đăng ký tài khoản developer
# Tạo Mini App mới
```

**2. Install Zalo SDK**
```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Đấu Trường Tri Thức</title>
    <script src="https://zalo-api.zadn.vn/api/sdk/zmp-sdk.js"></script>
</head>
<body>
    <div id="game-container"></div>
    <script src="game.js"></script>
</body>
</html>
```

**3. Initialize SDK**
```javascript
// game.js
import zalo from 'zmp-sdk';

// Initialize
zalo.init({
  appId: 'YOUR_APP_ID',
  success: () => {
    console.log('Zalo SDK initialized');
    getUserInfo();
  },
  fail: (error) => {
    console.error('Init failed:', error);
  }
});

// Get user info
function getUserInfo() {
  zalo.getUserInfo({
    success: (data) => {
      const { userInfo } = data;
      console.log('User:', userInfo.name);
      startGame(userInfo);
    },
    fail: (error) => {
      console.error('Get user info failed:', error);
    }
  });
}
```

**4. Implement Core Features**

```javascript
// Share to Zalo
function shareToZalo(score) {
  zalo.shareMessage({
    message: `Tôi đã đạt ${score.toLocaleString()} VNĐ trong Đấu Trường Tri Thức! Chơi cùng tôi nhé!`,
    link: 'https://zalo.me/s/YOUR_MINI_APP_ID',
    success: () => {
      console.log('Shared successfully');
    },
    fail: (error) => {
      console.error('Share failed:', error);
    }
  });
}

// ZaloPay Payment
function purchaseWithZaloPay(packageType, amount) {
  zalo.payment.pay({
    amount: amount, // VNĐ
    description: `Mua ${packageType}`,
    orderId: generateOrderId(),
    success: (data) => {
      console.log('Payment success:', data);
      // Grant credits to user
      grantCredits(packageType);
    },
    fail: (error) => {
      console.error('Payment failed:', error);
    }
  });
}

// Example: Buy AI Hint Pro
function buyAIHintPro() {
  purchaseWithZaloPay('AI Hint Pro', 30000);
}

// Open Zalo Chat
function inviteFriend() {
  zalo.openChat({
    type: 'user',
    message: 'Chơi Đấu Trường Tri Thức với tôi!',
    link: 'https://zalo.me/s/YOUR_MINI_APP_ID'
  });
}

// Get Phone Number (for registration)
function getPhoneNumber() {
  zalo.getPhoneNumber({
    success: (data) => {
      console.log('Phone:', data.number);
      // Register user with phone
    },
    fail: (error) => {
      console.error('Get phone failed:', error);
    }
  });
}
```

**5. Backend Integration**

```python
# Django backend for Zalo payment verification
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import hmac
import hashlib

@csrf_exempt
def zalo_payment_callback(request):
    """Verify Zalo payment callback"""
    data = request.POST
    
    # Verify signature
    mac = data.get('mac')
    app_id = data.get('appid')
    order_id = data.get('orderId')
    amount = data.get('amount')
    
    # Calculate MAC
    mac_data = f"{app_id}|{order_id}|{amount}"
    calculated_mac = hmac.new(
        settings.ZALO_SECRET_KEY.encode(),
        mac_data.encode(),
        hashlib.sha256
    ).hexdigest()
    
    if mac == calculated_mac:
        # Payment verified
        # Grant credits to user
        user = User.objects.get(zalo_id=data.get('userId'))
        grant_credits(user, order_id)
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'failed'}, status=400)
```

**6. Deploy to Zalo**

```bash
# Build production
npm run build

# Upload to Zalo:
# 1. Go to Zalo Mini App Console
# 2. Upload source code
# 3. Submit for review
# 4. Wait for approval (1-3 days)
```

#### Monetization with ZaloPay

```javascript
// Pricing packages
const PACKAGES = {
  ai_hint_basic: {
    name: 'AI Hint Basic',
    price: 10000, // VNĐ
    credits: 3
  },
  ai_hint_pro: {
    name: 'AI Hint Pro',
    price: 30000,
    credits: 10
  },
  vip_monthly: {
    name: 'VIP Monthly',
    price: 50000,
    credits: -1 // unlimited
  }
};

// Purchase flow
function purchase(packageId) {
  const package = PACKAGES[packageId];
  
  zalo.payment.pay({
    amount: package.price,
    description: package.name,
    orderId: `ORDER_${Date.now()}`,
    success: (data) => {
      // Call backend to verify and grant credits
      fetch('/api/shop/verify-payment', {
        method: 'POST',
        body: JSON.stringify({
          orderId: data.orderId,
          packageId: packageId
        })
      });
    }
  });
}
```

---

### 12.3 PWA + iOS Deployment (Priority 1.5) 📱

#### Overview
PWA cho phép game chạy trên iPhone như native app:
- ✅ Cài đặt được trên home screen
- ✅ Offline support
- ✅ Push notifications
- ✅ Không cần App Store approval
- ✅ Update tự động

#### PWA Requirements

**Technical Requirements:**
```
- HTTPS (bắt buộc)
- Web App Manifest
- Service Worker
- Responsive design
- iOS-specific meta tags
```

#### Setup Steps

**1. Create Web App Manifest**

```json
// public/manifest.json
{
  "name": "Đấu Trường Tri Thức",
  "short_name": "Brain Arena",
  "description": "Vietnamese quiz game - Only the Smart Survive",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#1a1a2e",
  "theme_color": "#16213e",
  "orientation": "portrait",
  "icons": [
    {
      "src": "/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-152x152.png",
      "sizes": "152x152",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-384x384.png",
      "sizes": "384x384",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "screenshots": [
    {
      "src": "/screenshots/home.png",
      "sizes": "1170x2532",
      "type": "image/png"
    },
    {
      "src": "/screenshots/game.png",
      "sizes": "1170x2532",
      "type": "image/png"
    }
  ]
}
```

**2. Add iOS-Specific Meta Tags**

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
    <!-- PWA Manifest -->
    <link rel="manifest" href="/manifest.json">
    
    <!-- iOS Specific -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Brain Arena">
    
    <!-- iOS Icons -->
    <link rel="apple-touch-icon" href="/icons/icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/icons/icon-180x180.png">
    
    <!-- iOS Splash Screens -->
    <link rel="apple-touch-startup-image" href="/splash/iphone5.png" media="(device-width: 320px) and (device-height: 568px)">
    <link rel="apple-touch-startup-image" href="/splash/iphone6.png" media="(device-width: 375px) and (device-height: 667px)">
    <link rel="apple-touch-startup-image" href="/splash/iphoneplus.png" media="(device-width: 414px) and (device-height: 736px)">
    <link rel="apple-touch-startup-image" href="/splash/iphonex.png" media="(device-width: 375px) and (device-height: 812px)">
    <link rel="apple-touch-startup-image" href="/splash/iphonexr.png" media="(device-width: 414px) and (device-height: 896px)">
    <link rel="apple-touch-startup-image" href="/splash/iphonexsmax.png" media="(device-width: 414px) and (device-height: 896px)">
    
    <!-- Theme Color -->
    <meta name="theme-color" content="#16213e">
    
    <title>Đấu Trường Tri Thức</title>
</head>
<body>
    <div id="app"></div>
</body>
</html>
```

**3. Create Service Worker**

```javascript
// public/service-worker.js
const CACHE_NAME = 'brain-arena-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/static/css/main.css',
  '/static/js/main.js',
  '/icons/icon-192x192.png',
  '/sounds/background.mp3',
  '/sounds/correct.mp3',
  '/sounds/wrong.mp3'
];

// Install event
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch event
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Cache hit - return response
        if (response) {
          return response;
        }
        
        // Clone the request
        const fetchRequest = event.request.clone();
        
        return fetch(fetchRequest).then((response) => {
          // Check if valid response
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }
          
          // Clone the response
          const responseToCache = response.clone();
          
          caches.open(CACHE_NAME)
            .then((cache) => {
              cache.put(event.request, responseToCache);
            });
          
          return response;
        });
      })
  );
});

// Activate event
self.addEventListener('activate', (event) => {
  const cacheWhitelist = [CACHE_NAME];
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
```

**4. Register Service Worker**

```javascript
// src/main.js
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js')
      .then((registration) => {
        console.log('SW registered:', registration);
      })
      .catch((error) => {
        console.log('SW registration failed:', error);
      });
  });
}

// Detect iOS
const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
const isInStandaloneMode = ('standalone' in window.navigator) && (window.navigator.standalone);

// Show install prompt for iOS
if (isIOS && !isInStandaloneMode) {
  showIOSInstallPrompt();
}

function showIOSInstallPrompt() {
  const prompt = document.createElement('div');
  prompt.className = 'ios-install-prompt';
  prompt.innerHTML = `
    <div class="prompt-content">
      <p>Cài đặt Brain Arena trên iPhone của bạn:</p>
      <ol>
        <li>Nhấn nút Share <img src="/icons/ios-share.png" alt="share"></li>
        <li>Chọn "Add to Home Screen"</li>
      </ol>
      <button onclick="this.parentElement.parentElement.remove()">Đóng</button>
    </div>
  `;
  document.body.appendChild(prompt);
}
```

**5. iOS-Specific CSS**

```css
/* iOS safe area support */
body {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}

/* Disable iOS bounce effect */
body {
  position: fixed;
  overflow: hidden;
  width: 100%;
  height: 100%;
}

#app {
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  height: 100%;
}

/* iOS install prompt */
.ios-install-prompt {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  padding: 20px;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
  z-index: 9999;
}

/* Prevent zoom on input focus (iOS) */
input, select, textarea {
  font-size: 16px !important;
}
```

#### Testing on iOS

```bash
# 1. Deploy to HTTPS server (required for PWA)
# 2. Open Safari on iPhone
# 3. Navigate to your URL
# 4. Tap Share button
# 5. Tap "Add to Home Screen"
# 6. App will appear on home screen
```

#### Optional: Native iOS App (React Native)

Nếu muốn submit lên App Store:

```bash
# Install React Native CLI
npm install -g react-native-cli

# Create React Native project
npx react-native init BrainArena

# Install WebView
npm install react-native-webview

# App.js - Wrap your web app
import React from 'react';
import { WebView } from 'react-native-webview';

export default function App() {
  return (
    <WebView
      source={{ uri: 'https://your-domain.com' }}
      style={{ flex: 1 }}
      javaScriptEnabled={true}
      domStorageEnabled={true}
    />
  );
}

# Build for iOS
cd ios
pod install
cd ..
npx react-native run-ios
```

#### App Store Submission (If needed)

```bash
# 1. Create Apple Developer Account ($99/year)
# 2. Create App ID in App Store Connect
# 3. Configure app in Xcode
# 4. Create screenshots (required sizes):
#    - 6.5" (iPhone 14 Pro Max): 1284 x 2778
#    - 5.5" (iPhone 8 Plus): 1242 x 2208
# 5. Submit for review
# 6. Wait 1-3 days for approval
```

---

### 12.4 Deployment Strategy (Updated)

#### Phase 1: Web + PWA (Month 1-3)
```
Week 1-4: Core Web Development
  - Build web version (Phase 1-2 of roadmap)
  - Basic features + Backend
  
Week 5-8: PWA Setup
  - Add manifest.json
  - Implement service worker
  - iOS-specific optimizations
  - Test on iPhone/iPad
  
Week 9-12: Monetization + Polish
  - Shop system
  - Payment integration
  - Performance optimization
  - PWA testing
```

#### Phase 2: Facebook Instant Games (Month 4-5)
```
Week 1-2: Setup & Integration
  - Create Facebook App
  - Integrate FB SDK
  - Implement core features
  
Week 3-4: Testing & Optimization
  - Test on FB Instant Games Player
  - Optimize bundle size
  - A/B test monetization
  
Week 5-6: Launch & Marketing
  - Submit for review
  - Soft launch
  - Marketing campaign
```

#### Phase 3: Zalo Mini Game (Month 6-7)
```
Week 1-2: Zalo Integration
  - Register Zalo Mini App
  - Integrate Zalo SDK
  - ZaloPay integration
  
Week 3-4: Localization & Testing
  - Vietnamese optimization
  - Test payment flow
  - Beta testing
  
Week 5-6: Launch
  - Submit to Zalo
  - Launch campaign
  - Influencer marketing
```

#### Phase 4: Native iOS App (Optional, Month 8+)
```
Week 1-2: React Native Setup
  - Create RN project
  - WebView integration
  - Test on iOS devices
  
Week 3-4: App Store Preparation
  - Screenshots
  - App Store listing
  - Submit for review
  
Week 5-6: Launch
  - App Store approval
  - Marketing campaign
```

#### Phase 5: Cross-Platform Optimization (Ongoing)
```
- Sync user data across platforms
- Cross-platform leaderboard
- Unified payment system
- Analytics & optimization
```

---

## 13. Development Setup

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
