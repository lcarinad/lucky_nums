from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from flask import jsonify, request

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

    @classmethod
    def validate(cls):
        """Validates user submitted data"""
        errors = {}
        if 'name' not in request.json:
            errors['name'] = ['This field is required']
        if 'email' not in request.json:
            errors['email'] = ['This field is required']
        if 'year' not in request.json:
            errors['year'] = ['This field is required']
        elif request.json['year'] not in range(1900,2000):
            errors['year'] = ['Invalid year. Birth year should be between 1900-2000']
        if 'color' not in request.json:
            errors['color'] = ['This field is required']
        elif request.json['color'] not in ['red', 'green', 'orange', 'blue']:
            errors['color'] = ['Invalid value, must be red, green, orange, or blue']
        
        if errors:
            return jsonify({"errors": errors}), 400

        #if validations pass, create and save User
        name = request.json["name"]
        email = request.json["email"]
        year = request.json["year"]
        color = request.json["color"]

        new_user = User(name=name, email=email, year=year, color=color)
        return new_user

    def serialize(self):
        """Returns a dict representation of user instance, which allows us to turn to JSON.  From the dict representation, the instance can be jsonified"""

        return {
            "id": self.id,
            "name": self.name,
            "year": self.year,
            "email": self.email,
            "color": self.color
        }
    
    def __repr__(self):
        return f"<User {self.id} name={self.name} year={self.year} email={self.email} fave_color={self.color}>"