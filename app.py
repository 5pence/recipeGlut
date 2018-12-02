from flask import Flask, render_template
from config import Config
from forms import LoginForm
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/recipeGlut'
app.config.from_object(Config)

mongo = PyMongo(app)

@app.route('/')
def index():
    user = {'username': 'spencer'}
    print(list(mongo.db.recipes.find()))
    return render_template('index.html', title="Home", user=user)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", title="Sign In", form=form)

if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.config['DEBUG'] = True
    app.run(host='127.0.0.1', debug=True)