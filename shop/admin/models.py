from shop import db
from shop import app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    profile =  db.Column(db.String(180), unique=False, nullable=False,default='profile.jpg0')
    
    def __repr__(self):
        return '<User %r>' %self.username
    

with app.app_context():
    db.create_all()