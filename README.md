# Torneo

A Flask tournament manager for teams and players.

## Features

- User registration and login
- Dashboard with tournament stats
- Team creation, editing, deletion, and detail pages
- Player creation, editing, deletion, and team assignment
- SQLite by default, with PostgreSQL available through Docker Compose

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file for local secrets if needed.

## Run

```bash
python run.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Database

This project uses Flask-Migrate/Alembic:

```bash
flask db upgrade
```