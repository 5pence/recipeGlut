from flask import render_template
from app import app
from forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'spencer'}
    return render_template('index.html', title="Home", user=user)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", title="Sign In", form=form)

