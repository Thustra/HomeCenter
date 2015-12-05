__author__ = 'Peter'

from project.models import * # pragma: no cover
from flask import render_template,Blueprint,flash,redirect,url_for,request # pragma: no cover
from flask.ext.login import login_required, current_user # pragma: no cover
from project.home.form import AddSeriesForm, EditSeriesForm # pragma: no cover
from project import db # pragma: no cover


##########
# Config #
##########

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
) # pragma: no cover

##########
# Routes #
##########

@home_blueprint.route('/')
@login_required
def home():
    shows = db.session.query(Show).order_by(Show.title).all()
    files = db.session.query(Download).all()
    return render_template('index.html', shows=shows, downloads=files)

@home_blueprint.route('/welcome')
def welcome():
    return render_template('welcome.html')

@home_blueprint.route('/add', methods=['GET','POST'])
@login_required
def add():
    form = AddSeriesForm(request.form)
    if form.validate_on_submit():
        show = Show(
            title=form.title.data,
            watching=form.watching.data,
            finished=form.finished.data
        )
        db.session.add(show)
        db.session.commit()
        flash("Successfully added!")
        return redirect(url_for('home.home'))
    return render_template('add.html', form=form)

@home_blueprint.route('/edit/<show>', methods=['GET','POST'])
@login_required
def edit(show):
    form = EditSeriesForm(request.form)
    if form.validate_on_submit():
        show_to_edit = Show.query.filter_by(title=show).first()
        show_to_edit.watching = form.watching.data
        db.session.commit()
        flash("Successfully edited!")
        return redirect(url_for('home.home'))
    return render_template('edit.html', form=form, show=show)