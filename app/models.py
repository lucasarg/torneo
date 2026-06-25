from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db, login_manager

class User(UserMixin, db.Model):
    """
    Basic user model for authentication.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, password: str) -> None:
        """Hash and store a plaintext password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify a plaintext password against the stored hash."""
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id: str):
    """Flask-Login hook to load a user by ID stored in the session."""
    return User.query.get(int(user_id))

class Team(db.Model):
    """
    A football/soccer team. Players belong to a team (optional).
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True, index=True)
    city = db.Column(db.String(120), nullable=True, index=True)

    # One-to-many relationship: a team has many players
    players = db.relationship("Player", back_populates="team")

    def __repr__(self) -> str:
        return f"<Team {self.name}>"

class Player(db.Model):
    """
    A player who optionally belongs to a team.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    position = db.Column(db.String(50), nullable=True)  # e.g., GK, DF, MF, FW
    age = db.Column(db.Integer, nullable=True)

    team_id = db.Column(db.Integer, db.ForeignKey("team.id", ondelete="SET NULL"), nullable=True)
    team = db.relationship("Team", back_populates="players")

    def __repr__(self) -> str:
        return f"<Player {self.name}>"
