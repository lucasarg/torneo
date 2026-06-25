# app/players/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class PlayerForm(FlaskForm):
    """Single form for create/edit player."""
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=120)])
    position = StringField("Position", validators=[Optional(), Length(max=50)])  # GK/DF/MF/FW
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=10, max=60)])
    team_id = SelectField("Team", coerce=int, validators=[Optional()])  # filled dynamically
    submit = SubmitField("Save")
