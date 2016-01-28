
from flask import Blueprint,render_template,request
from flask.ext.login import login_required # pragma: no cover
from flask_wtf import Form  # pragma: no cover
from project.budget.form import AddExpenseForm

##########
# Config #
##########

budget_blueprint = Blueprint(
    'budget', __name__,
    template_folder='templates'
) # pragma: no cover

##########
# Routes #
##########

@budget_blueprint.route('/budget')
@login_required
def budget():
    return render_template('budget.html')


@budget_blueprint.route('/expense',methods=['GET','POST'])
@login_required
def add():
    addExpenseForm = AddExpenseForm(request.form)

    if addExpenseForm.validate_on_submit():
        # Add stuff to DB
        print('adding stuff to DB')
        return render_template('budget.html')
    return render_template('budget_add.html',form=addExpenseForm)