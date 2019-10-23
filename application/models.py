from application import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return ''.join(['User ID: ', str(self.id), '\r\n', 
            'Email: ', self.email, '\r\n',
            'Name:', self.first_name, ' ', self.last_name])

class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return "{}".format(self.name)

class Album(db.Model):
    """"""
    __tablename__ = "album"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.String)
    publisher = db.Column(db.String)
    media_type = db.Column(db.String)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"))
    artist = db.relationship("Artist", backref=db.backref(
        "album", order_by=id), lazy=True)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))