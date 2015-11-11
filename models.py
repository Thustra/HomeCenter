__author__ = 'Peter'

from app import db

class Show(db.Model):

    __tablename__ = "shows"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    finished = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self,title,finished):
        self.title = title
        self.finished = finished

    def __repr__(self):
        return '<title {}'.format(self.title)

