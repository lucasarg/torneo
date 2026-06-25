from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required
from ..extensions import db
from ..models import Player, Team
from .forms import TeamForm

teams_bp = Blueprint("teams", __name__, url_prefix="/teams")

@teams_bp.route("/")
@login_required
def list_teams():
    """
    List all teams with a count of players.
    """
    teams = Team.query.order_by(Team.name.asc()).all()
    return render_template("teams/list.html", teams=teams)

@teams_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_team():
    """
    Create a new team using a Flask-WTF form.
    """
    form = TeamForm()

    if form.validate_on_submit():
        name = form.name.data.strip()
        city = (form.city.data or "").strip()

        if Team.query.filter_by(name=name).first():
            flash("Team name already exists", "danger")
        else:
            team = Team(name=name, city=city or None)
            db.session.add(team)
            db.session.commit()
            flash("Team created", "success")
            return redirect(url_for("teams.list_teams"))

    return render_template("teams/new.html", form=form, mode="create")

@teams_bp.route("/<int:team_id>")
@login_required
def detail_team(team_id: int):
    """
    Show one team with its roster.
    """
    team = Team.query.get_or_404(team_id)
    players = Player.query.filter_by(team_id=team.id).order_by(Player.name.asc()).all()
    return render_template("teams/detail.html", team=team, players=players)

@teams_bp.route("/<int:team_id>/edit", methods=["GET", "POST"])
@login_required
def edit_team(team_id: int):
    """
    Edit an existing team.
    """
    team = Team.query.get_or_404(team_id)
    form = TeamForm(obj=team)

    if form.validate_on_submit():
        name = form.name.data.strip()
        city = (form.city.data or "").strip()
        existing_team = Team.query.filter(Team.name == name, Team.id != team.id).first()

        if existing_team:
            flash("Team name already exists", "danger")
        else:
            team.name = name
            team.city = city or None
            db.session.commit()
            flash("Team updated", "success")
            return redirect(url_for("teams.list_teams"))

    return render_template("teams/new.html", form=form, mode="edit", team=team)

@teams_bp.route("/<int:team_id>/delete", methods=["POST"])
@login_required
def delete_team(team_id: int):
    """
    Delete a team and leave its players unassigned.
    """
    team = Team.query.get_or_404(team_id)
    player_count = Player.query.filter_by(team_id=team.id).count()

    Player.query.filter_by(team_id=team.id).update({"team_id": None})
    db.session.delete(team)
    db.session.commit()

    if player_count:
        flash(f"Team deleted. {player_count} players are now without a team.", "info")
    else:
        flash("Team deleted", "info")

    page = request.args.get("page")
    if page:
        return redirect(url_for("teams.list_teams", page=page))
    return redirect(url_for("teams.list_teams"))