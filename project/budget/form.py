__author__ = 'Peter'

from flask_wtf import Form
from wtforms import SelectField,IntegerField
from wtforms.validators import DataRequired,NumberRange
from wtforms.fields.html5 import DateField

class AddExpenseForm(Form):
    amount = IntegerField(
        'amount',
        validators=[
            DataRequired(),
            NumberRange(min=0)
        ]
    )
    date = DateField(
        'date',
        validators=[
            DataRequired()
        ]
    )
    category = SelectField(
        'category',
        choices=[('a','A'),('b','B')],
        validators=[
            DataRequired()
        ]
    )

