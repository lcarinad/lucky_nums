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

@app.route('/api/get-lucky-num', methods=['GET', 'POST'])
def create_lucky_num_profile():
    """Create lucky num from user form data & return it.
    Return JSON {'user':{id, name, email, year, color}}"""

    name = request.json["name"]
    email = request.json["email"]
    year = request.json["year"]
    color = request.json["color"]

    new_user = User(name=name, email=email, year=year, color=color)

    db.session.add(new_user)
    db.session.commit()
    response_json = jsonify(new_user.serialize())

    return response_json