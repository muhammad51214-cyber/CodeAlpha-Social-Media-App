# CodeAlpha Social Media App

A modern, minimal social platform built with Django as part of the CodeAlpha Internship (Task 2). It mixes familiar UI patterns from Instagram, Facebook, and YouTube: a public timeline, profile pages, likes, comments, and follows — all wrapped in a clean, responsive dark theme.

## ✨ Features

- Public feed showing posts from all users (no login needed to browse)
- Post creation (authenticated users)
- Likes and comments (authenticated users)
- Profiles with bio and post list
- Follow/unfollow users (authenticated users)
- Modern, responsive UI (dark theme, 3‑column layout, cards, action bars)
- Auth: signup, login, logout (secure POST logout)

## 🧱 Tech Stack

- Python 3.12, Django 5.1
- SQLite (default dev DB)
- HTML templates + vanilla CSS

## 🚀 Quickstart

1) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Apply database migrations

```bash
python manage.py migrate
```

4) Run the development server

```bash
python manage.py runserver 0.0.0.0:8000
```

Then open http://127.0.0.1:8000/ in your browser.

Notes for Codespaces/containers:
- `ALLOWED_HOSTS` includes `localhost`, `127.0.0.1`, and `0.0.0.0` for local dev.
- When using Codespaces, the forwarded URL is auto‑allowed.

## 🔐 Auth shortcuts

- Create a superuser (optional):

```bash
python manage.py createsuperuser
```

## 🗂️ Project structure

```
manage.py
core/                # app with models, views, urls, forms
social/              # project settings and root urls
templates/           # base.html, feed, auth, profiles, posts
static/css/          # style.css (dark theme)
requirements.txt
README.md
```

## 📷 Screenshots (optional)

Add screenshots of:
- Feed page (public)
- Profile page
- Post detail with comments
- Login / Signup

## ✅ Internship submission notes

- Task: Build a mini social media application
- What’s implemented:
	- Public feed of all posts
	- Post/like/comment/follow interactions
	- User auth (signup/login/logout), profile with bio
	- Modernized UI/UX, responsive layout
- How to run: see Quickstart above
- Repo: https://github.com/muhammad51214-cyber/CodeAlpha-Social-Media-App

## 📄 License

This project is for educational purposes as part of the CodeAlpha Internship.
