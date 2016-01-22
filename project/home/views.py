__author__ = 'Peter'

from project.models import * # pragma: no cover
from flask import render_template,Blueprint,flash,redirect,url_for,request,session # pragma: no cover
from flask_wtf import Form  # pragma: no cover
from wtforms import RadioField,HiddenField  # pragma: no cover
from wtforms.validators import DataRequired  # pragma: no cover
from flask.ext.login import login_required # pragma: no cover
from project.home.form import AddSeriesForm, EditSeriesForm # pragma: no cover
from project import db # pragma: no cover
import json, requests
from html.parser import HTMLParser



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

    class MLStripper(HTMLParser):
        def __init__(self):
            super(MLStripper,self).__init__()
            self.reset()
            self.fed = []
        def handle_data(self, d):
            self.fed.append(d)
        def get_data(self):
            return ''.join(self.fed)

    def strip_tags(html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    response=requests.get("http://api.tvmaze.com/search/shows?q="+session['title'])
    print(response)
    json_data=json.loads(response.text)
    options = []

    #
    # TODO: Add check for certain json parts not existing
    #

    for item in json_data:
        options.append(
            (
                str(item['show']['id']),
                item['show']['name'],
                (
                    item['show']['network']['name'] if item['show']['network'] else item['show']['webChannel']['name'],
                    strip_tags(item['show']['summary']),
                    item['show']['image']['medium'])
            )
        )




    class FancyRadioField(RadioField):
        def __init__(self, **kwds):
            super(FancyRadioField,self).__init__(**kwds)

        def iter_choices(self):
            for value, label, extra_data in self.choices:
                yield (value, label, extra_data, self.coerce(value) == self.data)

        def __iter__(self):
            opts = dict(widget=self.option_widget, _name=self.name, _form=None, _meta=self.meta)
            for i, (value, label,extra_data, checked) in enumerate(self.iter_choices()):
                opt = self._Option(label=label, id='%s-%d' % (self.id, i), **opts)
                opt.process(None, value)
                opt.checked = checked
                opt.extra_data=extra_data
                yield opt

        def validate(self, form, extra_validators=tuple()):
            print('validating')
            return super(FancyRadioField,self).validate(form, extra_validators)
            print('done validating')

        def pre_validate(self, form):
            for v, _, extra_data in self.choices:
                if self.data == v:
                    print("valid choice:" + str(self.data))
                    break
            else:
                raise ValueError(self.gettext('Not a valid choice'))


    F.selection = FancyRadioField(
        label='selection',
        choices=options,
        validators=[DataRequired()]
       )

    F.title = HiddenField(
        label='title'
    )


    form = F(request.form)

    #
    # TODO: Add a check to see if this series is already in the DB
    #

    #print(options)

    if form.validate_on_submit():
        print("In the if statement")
        print(form.data.items())
        show = Show(
            title=form.title.data,
            watching=session['watching'],
            finished=session['finished'],
            tvmaze_id = form.selection.data
        )
        test = db.session.query(Show).filter(Show.title == show.title).first()
        print("Show title: " + show.title)
        print(test)
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