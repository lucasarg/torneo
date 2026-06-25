from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class TeamForm(FlaskForm):
    """Form for creating or editing a team."""
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=120)])
    city = StringField("City", validators=[Optional(), Length(max=120)])
    submit = SubmitField("Save")