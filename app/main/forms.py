from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')


class CreateGameForm(FlaskForm):
    week = IntegerField('Week', validators=[DataRequired()])
    away_id = StringField('Away Team', validators=[DataRequired()])
    away_value = IntegerField('Point Value', validators=[DataRequired()])
    home_id = StringField('Home Team', validators=[DataRequired()])
    home_value = IntegerField('Point Value', validators=[DataRequired()])
    winner_id = StringField('Winner')
    submit = SubmitField('Submit')


class SelectGameForm(FlaskForm):
    week = IntegerField('Week', validators=[DataRequired()])
    team = StringField('Either Team Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
