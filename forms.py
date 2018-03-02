from initialize import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length, Email

class MainForm(FlaskForm):
	# search_type = RadioField('Search Type: ', choices=[('artist', 'artist'), ('track', 'track'), ('album', 'album')])
	search_name = StringField('Artist Name: ', validators=[InputRequired()])
	submit_button = SubmitField('Get Artist\'s info')
