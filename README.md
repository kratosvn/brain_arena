# Đấu Trường Tri Thức (Brain Arena)
**Only the Smart Survive**

Vietnamese quiz game với AI features, PvP mode, và monetization system.

## 📁 Project Structure

```
brain-arena/
├── backend/                # Django Backend
│   ├── apps/
│   │   ├── users/         # User management & authentication
│   │   ├── questions/     # Question bank management
│   │   ├── games/         # Game logic & history
│   │   ├── shop/          # Shop & payment integration
│   │   ├── ai/            # AI services (Gemini, TTS)
│   │   └── pvp/           # PvP & WebSocket (Django Channels)
│   ├── config/            # Django settings
│   ├── static/            # Static files
│   ├── media/             # User uploads
│   ├── templates/         # HTML templates
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/              # Vue.js Frontend
│   ├── src/
│   │   ├── views/        # Page components (Home, Game, Shop, etc.)
│   │   ├── components/   # Reusable components
│   │   ├── stores/       # Pinia state management
│   │   ├── services/     # API client (axios)
│   │   ├── router/       # Vue Router
│   │   ├── assets/       # Images, sounds
│   │   └── utils/        # Utility functions
│   ├── public/
│   ├── package.json
│   └── .env
│
├── GAME_SPEC.md          # Game specification
├── TECHNICAL_DOCS.md     # Technical documentation
└── README.md             # This file
```

## 🚀 Quick Start

### Backend Setup (Django)

```bash
cd backend

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
Backend runs at: **http://localhost:8000**  
Django Admin: **http://localhost:8000/admin**

### Frontend Setup (Vue.js)

```bash
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env
# Edit .env if needed

# Run development server
npm run dev
```

Frontend runs at: **http://localhost:5173**

## 🎮 Features

### ✅ Implemented
- Django backend with REST API
- Vue.js frontend with Vue Router
- State management with Pinia
- API client with authentication
- Beautiful dark theme UI
- Responsive design

### ⏳ In Development
- User authentication & profiles
- Question bank management
- Game logic (15 questions, 4 answers)
- Help features (50:50, Time Freeze, Swap)
- AI Question Generator (Gemini API)
- AI Voice Narrator (VieNeu-TTS)
- PvP mode (Django Channels)
- Shop & payment integration
- Leaderboard & ranking system

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 6.0
- **API**: Django REST Framework
- **Database**: SQLite (dev) / MySQL (prod)
- **Cache**: Redis
- **WebSocket**: Django Channels
- **AI**: Google Gemini API, VieNeu-TTS
- **Payment**: MoMo, ZaloPay, VNPay

### Frontend
- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **Router**: Vue Router 4
- **State**: Pinia
- **HTTP Client**: Axios
- **Styling**: Tailwind CSS (planned)

## 📚 Documentation

- [Game Specification](GAME_SPEC.md) - Detailed game design & features
- [Technical Documentation](TECHNICAL_DOCS.md) - Architecture & implementation

## 🔧 Development

### Backend Commands

```bash
# Run server
python manage.py runserver

python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test
```

### Frontend Commands

```bash
# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🌐 API Endpoints

- `/admin/` - Django Admin Panel
- `/api/auth/` - Authentication
- `/api/questions/` - Questions
- `/api/games/` - Games
- `/api/shop/` - Shop & Payments
- `/api/ai/` - AI Services
- `/api/pvp/` - PvP

## 📝 Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_NAME=brain_arena
GEMINI_API_KEY=your-gemini-key
REDIS_URL=redis://localhost:6379/0
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## 🎯 Roadmap

See [GAME_SPEC.md](GAME_SPEC.md) for detailed roadmap.

**Phase 1**: MVP Web Version (3-4 weeks)  
**Phase 2**: Backend + AI Integration (4-5 weeks)  
**Phase 3**: Monetization + Premium Features (3-4 weeks)  
**Phase 4**: PvP + Ranking System (4-5 weeks)  
**Phase 5**: Polish + Optimization (2-3 weeks)  
**Phase 6**: Platform Deployment (Optional)

## 📄 License

Private project

## 👨‍💻 Author

kratosvn
