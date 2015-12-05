__author__ = 'Peter'

from flask_wtf import Form
from wtforms import StringField,BooleanField
from wtforms.validators import DataRequired

class AddSeriesForm(Form):
    title = StringField(
        'title',
        validators=[
            DataRequired()
        ]
    )
    watching = BooleanField(
        'watching'
    )
    finished = BooleanField(
        'finished'
    )

class EditSeriesForm(Form):
    watching = BooleanField(
        'watching'
    )
    finished = BooleanField(
        'finished'
    )