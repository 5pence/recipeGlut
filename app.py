from flask import Flask, render_template, flash, redirect, url_for, request, session
from config import Config
from forms import LoginForm, RegisterForm, CreateRecipeForm
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
import re

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/recipeGlut'
app.config.from_object(Config)

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    four_recipes = mongo.db.recipes.find().limit(4)
    # print(list(four_recipes))
    return render_template('index.html', title="Home", recipes=four_recipes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        if session['logged_in'] is True:
            return redirect(url_for('index', title="Sign In"))

    form = LoginForm()

    if form.validate_on_submit():
        users = mongo.db.users
        db_user = users.find_one({'name': request.form['username']})

        if db_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'),
                             db_user['password']) == db_user['password']:
                session['username'] = request.form['username']
                session['logged_in'] = True
                return redirect(url_for('index', title="Sign In", form=form))
            flash('Invalid username/password combination')
    return render_template("login.html", title="Sign In", form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hash_pass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'],
                          'password': hash_pass,
                          'email': request.form['email']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        flash('Sorry, that username is already taken - use another')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


@app.route('/create_recipe', methods=['GET', 'POST'])
def create_recipe():
    form = CreateRecipeForm(request.form)
    if form.validate_on_submit():
        recipes = mongo.db.recipes
        print('i am here')
        recipes.insert({
            'title': request.form['title'],
            'user': session['username'],
            'short_description': request.form['short_description'],
            'ingredients': request.form['ingredients'],
            'method': request.form['method'],
            'tags': request.form['tags'],
            'image': request.form['image']
        })
        return redirect(url_for('index', title='New Recipe Added'))
    return render_template('create_recipe.html', title='create a recipe', form=form)

@app.route('/search')
def search():
    orig_query = request.args['query']
    query = {'$regex': re.compile('.*{}.*'.format(orig_query)), '$options': 'i'}
    results = mongo.db.recipes.find({
        '$or': [
            {'title': query},
            {'tags': query},
            {'ingredients': query},
        ]
    })
    return render_template('search.html', query=orig_query, results=results)

@app.route('/recipes')
def recipes():
    all_recipes = mongo.db.recipes.find()
    return render_template('recipes.html', recipes=all_recipes)


@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    recipe = mongo.db.recipes.find_one_or_404({'_id': ObjectId(recipe_id)})
    return render_template('recipe.html', recipe=recipe)

@app.errorhandler(404)
def handle_404(exception):
    return render_template('404.html', exception = exception)

if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.config['DEBUG'] = True
    app.run(host='127.0.0.1', debug=True)