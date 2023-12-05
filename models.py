from flask_sqlalchemy import SQLAlchemy, CheckConstraint

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

    __table_args__ = (
        CheckConstraint('year BETWEEN 1900 AND 2000', name='check_birth_year'),CheckConstraint("color IN ('red', 'green', 'orange', 'blue')", name="check_color"),
    )
    

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