__author__ = 'Peter'

from project import db # pragma: no cover
from project import bcrypt # pragma: no cover

from sqlalchemy import ForeignKey # pragma: no cover
from sqlalchemy.orm import relationship # pragma: no cover


class Show(db.Model):

    __tablename__ = "shows"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    watching = db.Column(db.Boolean, nullable=True, default=False)
    finished = db.Column(db.Boolean, nullable=False, default=False)
    tvmaze_id = db.Column(db.Integer, nullable=True, unique=True)
    downloads = relationship("Download", backref="show")

    def __init__(self,title,watching,finished,tvmaze_id):
        self.title = title
        self.watching = watching
        self.finished = finished
        self.tvmaze_id = tvmaze_id

    def __repr__(self):
        return '<title {}'.format(self.title)


class Download(db.Model):

    __tablename__ = "downloads"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    size = db.Column(db.BigInteger, nullable=False)
    location = db.Column(db.String, nullable=False)
    season = db.Column(db.Integer, nullable=False)
    download_timestamp = db.Column(db.DateTime, nullable=False)

    show_id = db.Column(db.Integer, ForeignKey("shows.id"))

    def __init__(self,filename,size,location,timestamp,season):
        self.filename = filename
        self.size = size
        self.location = location
        self.download_timestamp = timestamp
        self.season = season

    def __repr__(self):
        return '<File {}'.format(self.filename)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self,name,password):
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode()

    def __repr__(self):
        return 'User {}'.format(self.name)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
