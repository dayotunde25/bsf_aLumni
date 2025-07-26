
# Baptist Student Fellowship Alumni Management System

## 🧠 Final Developer Agent Prompt

**Project Name**: Baptist Student Fellowship Alumni Management System  
**Objective**: Build a complete, responsive, and scalable web application that connects past and present student members of the fellowship with chat, service history, events, birthday features, and a robust media archive.

---

## 🧱 Tech Stack

- **Backend**: Python (Django 4+ with Django REST Framework)
- **Frontend**: Django templates + Bootstrap 5 *(OR React.js if separated from backend)*
- **Database**: PostgreSQL
- **Real-time Chat**: Django Channels (WebSocket)
- **Deployment Ready**: Heroku/Render with `.env`, Gunicorn, static/media config

---

## ✅ Features to Implement

### 🔐 User Management
- Registration & login with email/phone & password
- Roles: Student, Alumnus, Admin
- Store:
  - Full name, email, phone
  - **Birthday** (month and day only)
  - **Multiple executive roles** with session (e.g., President - 2020/2021)
  - **Multiple workers' units** with session (e.g., Choir - 2019/2020)
  - Fellowship attendance years
- User profile view & edit

### 💬 Real-Time Chat
- One-on-one chat between verified users
- Admin broadcast message to all
- Optional: Group chats by unit or session
- WebSocket with read receipts & typing indicators

### 🎂 Birthday System
- Users enter birthday (MM-DD only)
- Daily task checks today’s birthdays
- Show banner on dashboard:
  > 🎉 Today’s Birthdays: [Names] – Happy Birthday! 🎂
- Optional: Email notification to celebrants

### 🖼️ Gallery / Media Archive
- Users or admins can upload:
  - Photos or videos
  - Tied to event (e.g., Bible Day, Cultural Day)
  - Tied to session
- Public gallery with filters (event type, year)
- Admin moderation for uploads

### 📢 Announcements & Events
- Admin can create announcements with:
  - Title, message, type
  - Optional RSVP for events
- Display upcoming events on dashboard

### 🧾 Alumni Directory
- Search and filter by:
  - Name
  - Session
  - Role or Unit
- Mini-profile view with full service history

### 📚 Resource Hub
- Upload/download of:
  - Sermon files (PDF, audio, video)
  - Devotionals
  - Manuals
- Categorized for easy access

### 🙏 Prayer Wall & Testimony Board
- Users post prayer requests
- Others can mark “I’m praying” or comment
- Requests can be marked "answered"
- Users can post testimonies
- Admin moderation

### 💼 Job Board
- Alumni post jobs or internship opportunities
- Fields: title, description, link/contact, deadline
- Filter by category or location
- Admin approval before publishing

### 🤝 Mentorship Matching
- Alumni can register as mentors
- Students request mentorship by interest/department
- System matches mentor/mentee
- Optional private chat between matched users

### 🕰️ Fellowship History Timeline
- Visual display of historical milestones:
  - Founding year
  - Past presidents/executives
  - Revival/Outreach dates
- Styled with cards or interactive timeline

### 🛠️ Admin Dashboard
- User stats: total, active, birthdays this week
- Approve media uploads, job posts, prayer/testimony content
- Export CSV reports (user list, birthdays, attendance years)

---

## 🎨 Branding
- Name: **Baptist Student Fellowship**
- Official Color: **Light Green**
  - Primary: `#A8D5BA`
  - Accent: `#DFF0D8`
  - Text: `#2D4739`
- Use existing logo (uploaded separately)
- Responsive and mobile-friendly layout

---

## 🔧 Deployment & Testing
- Production-ready deployment setup:
  - `.env` for secrets
  - Gunicorn for WSGI
  - Static/media file handling
- Unit & integration tests for major features
- Secure password hashing
- README + Admin Setup Guide

---

## 📁 Project Structure (Django)
```
baptist_fellowship/
├── users/              # Custom user logic, profile, roles
├── chat/               # WebSocket-based chat
├── birthdays/          # Birthday tracker
├── gallery/            # Media archive
├── events/             # Announcements & RSVP
├── prayer/             # Prayer wall & testimonies
├── jobs/               # Job board
├── mentorship/         # Mentor-mentee system
├── resources/          # Resource Hub
├── history/            # Fellowship timeline
├── dashboard/          # Homepages and admin stats
├── static/
├── templates/
└── manage.py
```

---

## 🔚 Deliverables
- Complete Django codebase with all apps and templates
- Django admin enabled for all models
- Environment setup (`requirements.txt`, `.env.example`)
- Test coverage for key modules
- Deployment-ready (Heroku/Render or Docker)
- README file with setup and usage instructions
