# app/players/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ..extensions import db
from ..models import Player, Team
from .forms import PlayerForm

players_bp = Blueprint("players", __name__, url_prefix="/players")

def _fill_team_choices(form: PlayerForm):
    """Populate SelectField with teams; add 'No team' option."""
    teams = Team.query.order_by(Team.name.asc()).all()
    form.team_id.choices = [(-1, "— No team —")] + [(t.id, t.name) for t in teams]

@players_bp.route("/", methods=["GET", "POST"])
@login_required
def list_create():
    """
    GET: list players (paginated) and show create form.
    POST: create new player.
    Uses one template for both list + create.
    """
    form = PlayerForm()
    _fill_team_choices(form)

    if form.validate_on_submit():
        team_id = None if form.team_id.data in (-1, None) else form.team_id.data
        player = Player(
            name=form.name.data.strip(),
            position=(form.position.data or "").strip() or None,
            age=form.age.data,
            team_id=team_id,
        )
        db.session.add(player)
        db.session.commit()
        flash("Player created", "success")
        return redirect(url_for("players.list_create"))

    # pagination
    page = request.args.get("page", 1, type=int)
    per_page = 10
    pagination = Player.query.order_by(Player.name.asc()).paginate(page=page, per_page=per_page)
    players = pagination.items

    return render_template(
        "players/manage.html",
        form=form,
        players=players,
        pagination=pagination,
        mode="create",  # template knows which header/button to show
    )

@players_bp.route("/<int:player_id>/edit", methods=["GET", "POST"])
@login_required
def edit(player_id: int):
    """Edit player using the same template."""
    player = Player.query.get_or_404(player_id)
    form = PlayerForm(obj=player)
    _fill_team_choices(form)
    # map None team -> -1 for the dropdown
    form.team_id.data = player.team_id if player.team_id is not None else -1

    if form.validate_on_submit():
        player.name = form.name.data.strip()
        player.position = (form.position.data or "").strip() or None
        player.age = form.age.data
        player.team_id = None if form.team_id.data in (-1, None) else form.team_id.data
        db.session.commit()
        flash("Player updated", "success")
        return redirect(url_for("players.list_create"))

    # list (same as list_create) for context while editing
    page = request.args.get("page", 1, type=int)
    per_page = 10
    pagination = Player.query.order_by(Player.name.asc()).paginate(page=page, per_page=per_page)
    players = pagination.items

    return render_template(
        "players/manage.html",
        form=form,
        players=players,
        pagination=pagination,
        mode="edit",
        editing=player,
    )

@players_bp.route("/<int:player_id>/delete", methods=["POST"])
@login_required
def delete(player_id: int):
    player = Player.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    flash("Player deleted", "info")
    # keep current page if provided
    page = request.args.get("page", 1, type=int)
    return redirect(url_for("players.list_create", page=page))
