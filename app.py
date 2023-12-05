from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("index.html")

@app.route('/api/get-lucky-num', methods=['GET', 'POST'])
def create_lucky_num_profile():
    """Create lucky num from user form data & return it.
    Return JSON {'user':{id, name, email, birth_year, fave_color}}"""

    name = request.json["name"]
    email = request.json["email"]
    birth_year = request.json["birth_year"]
    fave_color = request.json["fave_color"]

    new_user = User(name=name, email=email, birth_year=birth_year, fave_color=fave_color)


    return