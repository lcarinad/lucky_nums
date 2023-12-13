from flask import Flask, render_template, request, jsonify, flash
from sqlalchemy.exc import IntegrityError, DataError
from models import db, connect_db, User
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lucky_nums_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

app.app_context().push()

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")

# *****************************
# RESTFUL JSON API
# *****************************

@app.route('/api/get-lucky-num', methods=['POST'])
def get_lucky_num():
    """Create lucky num from user form data & return it.
    Return JSON {
        'num':{fact:'rand fact', num:67}, "year":{"fact:"randfact", "year":birthyear}"""
    errors = {}
    try:
        required_fields=['name', 'year', 'email', 'color']
        for field in required_fields:
            if not request.json.get(field) or request.json[field] == '':
                errors[field]=['Input required'] 
        if errors:
            return jsonify({"errors":errors}), 400


        new_user=User(name=request.json["name"],year=request.json["year"], email=request.json["email"],color=request.json["color"] )

        db.session.add(new_user)
        db.session.commit()

        lucky_num=User.get_lucky_num(new_user)

        return lucky_num, 201
    
    except (IntegrityError, DataError):
        if request.json['year'] not in range(1900,2000):
            errors['year'] = ['Invalid year. Birth year should be between 1900-2000']
        if 'color' not in request.json:
            errors['color'] = ['This field is required']
        if request.json['color'] not in ['red', 'green', 'orange', 'blue']:
            errors['color'] = ['Invalid value, must be red, green, orange, or blue']
        
        db.session.rollback()

        return jsonify({"errors": errors}), 400

    
   
    