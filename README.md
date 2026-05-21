# 💕 Together — Private Long-Distance Couple Platform

> A premium, full-stack relationship platform where long-distance couples can chat, play games, save memories, and stay emotionally close — no matter the distance.

![Together Platform](https://img.shields.io/badge/Django-5.0-green) ![Python](https://img.shields.io/badge/Python-3.11-blue) ![Channels](https://img.shields.io/badge/Django%20Channels-4.0-purple) ![License](https://img.shields.io/badge/License-MIT-pink)

---

## ✨ Features

| Feature | Description |
|---|---|
| 💬 Real-Time Chat | WebSocket-powered messaging with typing indicators, image sharing, emoji |
| 📸 Memory Timeline | Shared photo album with categories, favorites, captions |
| 🎯 This or That | Compatibility game with match percentage tracking |
| 💌 Open When Messages | Emotional locked messages for special moments |
| 🌟 Bucket List | Shared couple goals and dream tracking |
| 😊 Mood Sharing | Live mood updates with emoji and message |
| 💑 Date Ideas | Virtual and in-person date idea generator |
| 🧠 Couple Quiz | "How well do you know your partner?" quiz game |
| 🎲 Truth or Dare | Romantic, cute, funny, and deep prompts |
| 🔔 Notifications | Real-time system notifications |
| 🌙 Dark Mode | Full light/dark theme toggle |
| 📱 Mobile Responsive | Works on all screen sizes |

---

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/together
cd together

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
# Copy example env
cp .env.example .env

# Edit .env with your values
nano .env
```

### 3. Database Setup

```bash
cd together_project

# Run migrations
python manage.py migrate

# Seed sample data
python manage.py seed_data  # or use the shell script below

# Create superuser
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
# Start with Daphne (supports WebSockets)
daphne -p 8000 together_project.asgi:application

# OR standard Django server (no WebSockets)
python manage.py runserver
```

Visit: http://localhost:8000

---

## 👥 Sample Accounts

| Username | Password | Role |
|---|---|---|
| alice | password123 | User (coupled with bob) |
| bob | password123 | User (coupled with alice) |
| admin | admin123 | Superuser |

---

## 📁 Project Structure

```
together_project/
├── together_project/        # Main Django project
│   ├── settings.py          # Development settings
│   ├── settings_prod.py     # Production settings
│   ├── urls.py              # Root URL config
│   ├── asgi.py              # ASGI + WebSocket config
│   └── wsgi.py              # WSGI config
│
├── accounts/                # Auth + User profiles
│   ├── models.py            # Custom User model
│   ├── views.py             # Auth views + dashboard
│   ├── urls.py
│   └── forms.py
│
├── chat/                    # Real-time chat
│   ├── consumers.py         # WebSocket consumer
│   ├── routing.py           # WebSocket routing
│   ├── models.py            # Message model
│   └── views.py
│
├── memories/                # Photo memories
│   ├── models.py
│   └── views.py
│
├── games/                   # Games (This or That, Quiz, etc.)
│   ├── models.py
│   └── views.py
│
├── features/                # Open When, Date Ideas, Notifications
│   ├── models.py
│   └── views.py
│
├── templates/               # All HTML templates
│   ├── base.html            # Base layout with sidebar
│   ├── landing.html         # Landing page
│   ├── dashboard.html       # Main dashboard
│   ├── accounts/
│   ├── chat/
│   ├── memories/
│   ├── games/
│   └── features/
│
└── static/
    └── css/
        └── together.css     # Main stylesheet
```

---

## 🌐 Deployment

### Render

1. Create a new **Web Service** on [render.com](https://render.com)
2. Connect your GitHub repo
3. Set these settings:
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command:** `daphne -b 0.0.0.0 -p $PORT together_project.asgi:application`
4. Add environment variables (see below)

### Railway

```bash
railway init
railway add postgresql
railway add redis
railway deploy
```

### Environment Variables

```env
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=together_db
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
REDIS_URL=redis://your-redis-host:6379
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## 🔧 Tech Stack

- **Backend:** Python 3.11, Django 5.0
- **Real-time:** Django Channels 4.0, WebSockets
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Frontend:** HTML5, CSS3, Vanilla JS
- **Fonts:** DM Serif Display, DM Sans, Caveat
- **Static:** WhiteNoise
- **Server:** Daphne (ASGI) / Gunicorn

---

## 📸 Design System

- **Primary:** `#FF6B8A` (Rose)
- **Secondary:** `#C084FC` (Mauve)
- **Accent:** `#818CF8` (Indigo)
- **Background:** Soft gradient (light/dark)
- **Cards:** Glassmorphism with backdrop blur
- **Typography:** DM Serif Display (headings), DM Sans (body), Caveat (handwriting)

---

## 🤝 How Coupling Works

1. User A signs up → gets a unique `invite_code` (UUID)
2. User A shares code with User B
3. User B signs up → goes to "Connect Partner" → enters User A's code
4. Both users are now linked: `user.partner` ↔ `partner.partner`
5. All shared content (chat, memories, games) is scoped to the couple

---

## 🔒 Security

- CSRF protection on all forms
- Login required on all authenticated views
- Couple scoping: users can only see their partner's content
- Session-based authentication
- Production: HTTPS enforced, secure cookies, HSTS

---

Made with 💕 for long-distance love
