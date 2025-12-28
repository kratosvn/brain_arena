# Đấu Trường Tri Thức (Brain Arena)
**Only the Smart Survive**

Vietnamese quiz game với AI features, PvP mode, và monetization system.

## Spec
- https://github.com/kratosvn/brain_arena/blob/main/GAME_SPEC.md
## Technical docs
- https://github.com/kratosvn/brain_arena/blob/main/TECHNICAL_DOCS.md


## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- MySQL 8.0+ (for production)
- Redis 7.0+ (for caching & WebSocket)

### Installation

```bash
# Clone repository
git clone <repo-url>
cd brain-arena

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Server sẽ chạy tại: http://localhost:8000
Django Admin: http://localhost:8000/admin

## 📁 Project Structure

```
brain-arena/
├── config/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/             # User management
│   ├── questions/         # Question bank
│   ├── games/             # Game logic
│   ├── shop/              # Shop & payments
│   ├── ai/                # AI services
│   └── pvp/               # PvP & WebSocket
├── static/                # Static files
├── media/                 # User uploads
├── templates/             # HTML templates
├── manage.py
├── requirements.txt
└── .env
```

## 🎮 Features

- ✅ Django Admin for content management
- ✅ REST API with Django REST Framework
- ✅ Token authentication
- ✅ CORS enabled for frontend
- ⏳ AI Question Generator (Gemini API)
- ⏳ AI Voice Narrator (VieNeu-TTS)
- ⏳ PvP mode (Django Channels)
- ⏳ Payment integration (MoMo/ZaloPay/VNPay)

## 📚 Documentation

- [Game Specification](GAME_SPEC.md)
- [Technical Documentation](TECHNICAL_DOCS.md)

## 🔧 Development

```bash
# Run development server
python manage.py runserver

# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic
```

## 🌐 API Endpoints

- `/admin/` - Django Admin
- `/api/auth/` - Authentication
- `/api/questions/` - Questions
- `/api/games/` - Games
- `/api/shop/` - Shop & Payments
- `/api/ai/` - AI Services
- `/api/pvp/` - PvP

## 📝 License

Private project

## 👨‍💻 Author

kratosvn
