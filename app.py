from flask import Flask, render_template, request, jsonify

from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lucky_nums_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)

@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")

# *****************************
# RESTFUL JSON API
# *****************************

@app.route('/api/get-lucky-num', methods=['POST'])
def create_lucky_num_profile():
    """Create lucky num from user form data & return it.
    Return JSON {'user':{id, name, email, year, color}}"""
    data = request.get_json()

    #validation for required fields
    errors = {}
    if 'name' not in data:
        errors['name'] = ['This field is required']
    if 'email' not in data:
        errors['email'] = ['This field is required']
    if 'year' not in data:
        errors['year'] = ['This field is required']
    if 'color' not in data:
        errors['color'] = ['This field is required']
    elif data['color'] not in ['red', 'green', 'orange', 'blue']:
        errors['color'] = ['Invalid value, must be red, green, orange, or blue']
    
    if errors:
        return jsonify({"errors": errors}), 400

    #if validations pass, create and save User
    name = data["name"]
    email = data["email"]
    year = data["year"]
    color = data["color"]

    new_user = User(name=name, email=email, year=year, color=color)

    db.session.add(new_user)
    db.session.commit()
    response_json = jsonify(new_user.serialize())

    return (response_json, 201)