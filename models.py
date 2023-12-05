from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model"""
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.Text, nullable=False)
    year=db.Column(db.Integer, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    color = db.Column(db.Text, nullable = False)