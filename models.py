from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from flask import jsonify, request
import random, requests
from sqlalchemy.exc import IntegrityError

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

    __table_args__ = ( CheckConstraint('year BETWEEN 1900 AND 2000', name='check_birth_year'), CheckConstraint("color IN ('red', 'green', 'orange', 'blue')", name="check_color")
    )

    def __repr__(self):
        return f"<User {self.id} name={self.name} year={self.year} email={self.email} fave_color={self.color}>"
    
    def get_lucky_num(user):
        num_rand_num=random.randint(1, 100)
        num_res = requests.get(f"http://numbersapi.com/{num_rand_num}")
        num_fact = num_res.text

        year_year = user.year
        year_res=requests.get(f"http://numbersapi.com/{year_year}/year")
        year_fact=year_res.text

        response = {
            "num": {"fact": num_fact, "num": num_rand_num},
            "year": {"fact": year_fact, "year": year_year}
        }
        return response


