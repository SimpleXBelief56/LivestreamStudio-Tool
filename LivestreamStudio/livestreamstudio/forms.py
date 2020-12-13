from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, InputRequired


class RequestVerses(FlaskForm):
   Book = StringField('Book', validators=[DataRequired()])
   Chapter = IntegerField('Chapter', validators=[DataRequired()])
   Verse1 = IntegerField('Verse 1', validators=[DataRequired()])
   Verse2 = IntegerField('Verse 2', validators=[DataRequired()])
   submit = SubmitField('Parse Verses')

