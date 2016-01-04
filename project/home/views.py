__author__ = 'Peter'

from project.models import * # pragma: no cover
from flask import render_template,Blueprint,flash,redirect,url_for,request,session # pragma: no cover
from flask_wtf import Form  # pragma: no cover
from wtforms import RadioField,HiddenField  # pragma: no cover
from wtforms.validators import DataRequired  # pragma: no cover
from flask.ext.login import login_required # pragma: no cover
from project.home.form import AddSeriesForm, EditSeriesForm, AddTVmazeIDForm # pragma: no cover
from project import db # pragma: no cover
import json, requests



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

@home_blueprint.route('/show/<title>', methods=['GET','POST'])
@login_required
def show(show):
    current_show = Show.query.filter_by(title=show).first()
    pass

@home_blueprint.route('/add', methods=['GET','POST'])
@login_required
def add():
    form = AddSeriesForm(request.form)
    if form.validate_on_submit():
        session['title'] = form.title.data
        session['watching'] = form.watching.data
        session['finished'] = form.finished.data

        return redirect(url_for('home.set_tvmaze_id'))
    return render_template('add.html', form=form)

@login_required
@home_blueprint.route('/set_tvmaze_id', methods=['GET', 'POST'])
def set_tvmaze_id():

    class F(Form):
        pass

    response=requests.get("http://api.tvmaze.com/search/shows?q="+session['title'])
    print(response)
    json_data=json.loads(response.text)
    options = []
    for item in json_data:
        options.append(
            (
                str(item['show']['id']),
                item['show']['name']
             )
        )

    print(options)

    F.selection = RadioField(
        'selection',
        choices=options,
        validators=[
            DataRequired()
        ]
    )

    form = F(request.form)

    if form.validate_on_submit():
        print(form.selection.data)
        show = Show(
            title=session['title'],
            watching=session['watching'],
            finished=session['finished'],
            tvmaze_id = form.selection.data
        )
        #db.session.add(show)
        #db.session.commit()
        return redirect(url_for('home.home'))
    return render_template('set_tvmaze_id.html', form=form)


@home_blueprint.route('/edit/<show>', methods=['GET','POST'])
@login_required
def edit(show):
    form = EditSeriesForm(request.form)
    show_to_edit = Show.query.filter_by(title=show).first()

    if form.validate_on_submit():
        if request.form['btn'] == 'save':
            show_to_edit.watching = form.watching.data
            db.session.commit()
            flash("Successfully edited!")
            return redirect(url_for('home.home'))
        else:
            return redirect(url_for('home.home'))
    form.watching.data = show_to_edit.watching
    form.finished.data = show_to_edit.finished
    return render_template('edit.html', form=form, show=show)