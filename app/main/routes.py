from flask import Blueprint, render_template
from flask_login import login_required
from ..models import Player, Team

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    """Public home."""
    return render_template("home.html")

@main_bp.route("/dashboard")
@login_required
def dashboard():
    """Protected area for logged-in users."""
    stats = {
        "teams": Team.query.count(),
        "players": Player.query.count(),
        "free_players": Player.query.filter_by(team_id=None).count(),
    }
    return render_template("dashboard.html", stats=stats)