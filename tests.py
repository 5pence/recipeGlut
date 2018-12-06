'''
Run with:
    python -m unittest
'''

import unittest
import re

from flask_pymongo import PyMongo

import app as app_module

app = app_module.app

app.config["TESTING"] = True
app.config["WTF_CSRF_ENABLED"] = False
app.config['MONGO_URI'] = 'mongodb://localhost:27017/recipeGlutTesting'

mongo = PyMongo(app)
app_module.mongo = mongo


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            mongo.db.users.delete_many({})
            mongo.db.recipes.delete_many({})


class AppTests(AppTestCase):
    def test_index(self):
        res = self.client.get('/')
        data = res.data.decode('utf-8')
        assert res.status == '200 OK'
        assert 'A Glut of Recipes' in data

    def test_recipes(self):
        res = self.client.get('/recipes')
        data = res.data.decode('utf-8')
        assert res.status == '200 OK'
        assert 'features' in data

    def test_register_mismatch_passwords(self):
        """Entering mismatched passwords on the registration form -- needs fixing weird email thing"""
        res = self.client.post('/register', data=dict(
            username='fred',
            password='joijqwdoijqwoid',
            password2='qoijwdoiqwjdoiqwd',
            email='fred@aol.com',
        ))
        data = res.data.decode('utf-8')
        assert 'Passwords must match' in data

    def test_register_duplicate_username(self):
        res = self.client.post('/register', follow_redirects=True, data=dict(
            username='fred',
            password='asdfasdfasdf',
            password2='asdfasdfasdf',
            email='fred@aol.com',
        ))
        data = res.data.decode('utf-8')
        assert 'A Glut of Recipes' in data
        res = self.client.post('/register', follow_redirects=True, data=dict(
            username='fred',
            password='asdfasdfasdf',
            password2='asdfasdfasdf',
            email='fred@aol.com',
        ))
        data = res.data.decode('utf-8')
        assert res.status == '200 OK'
        assert 'that username is already taken' in data

    def test_register_successful(self):
        res = self.client.post('/register', follow_redirects=True, data=dict(
            username='freddie',
            password='asdfasdfasdf',
            password2='asdfasdfasdf',
            email='freddie@aol.com',
        ))
        data = res.data.decode('utf-8')
        assert res.status == '200 OK'
        assert 'A Glut of Recipes' in data


class LoggedInTests(AppTestCase):
    def setUp(self):
        super().setUp()
        res = self.client.post('/register', follow_redirects=True, data=dict(
            username='fred3',
            password='asdfasdfasdf',
            password2='asdfasdfasdf',
            email='fred3@aol.com',
        ))
        res = self.client.post('/create_recipe', follow_redirects=True, data={
            'title': 'Mac and cheese',
            'short_description': 'Get this mac and cheese',
            'ingredients': '8 spring onions',
            'method': 'Put all the ingredients',
            'tags': 'cheese, slow',
            'image': 'some image link'
        })
        data = res.data.decode('utf-8')
        assert 'You feed me' in data

    def test_create_recipe(self):
        """"""
        res = self.client.post('/create_recipe', follow_redirects=True, data={
            'title': 'Slow - cooker vegan bean chilli',
            'short_description': 'Get this vegan',
            'ingredients': '8 spring onions',
            'method': 'Put all the ingredients',
            'tags': 'vegan, slow',
            'image': 'some image link'
        })
        data = res.data.decode('utf-8')
        assert 'You feed me' in data

    def test_recipe_page(self):
        """Viewing a recipe page"""
        res = self.client.get('/recipes')
        ids = re.findall(r'href="/recipe/(\w+)"', res.data.decode("utf8"))
        assert len(ids) > 0
        res = self.client.get('/recipe/{}'.format(ids[0]))
        data = res.data.decode('utf-8')
        assert res.status == '200 OK'
        assert 'Mac and cheese' in data

    def test_edit_recipe(self):
        res = self.client.get('/recipes')
        ids = re.findall(r'href="/recipe/(\w+)"', res.data.decode("utf8"))
        assert len(ids) > 0
        res = self.client.get('/edit_recipe/{}'.format(ids[0]))
        data = res.data.decode('utf-8')
        assert res.status == '200 OK'
        assert 'Mac and cheese' in data
        res = self.client.post('/edit_recipe/'.format(ids[0]), follow_redirects=True, data={
            'title': 'Mac and cheese',
            'short_description': 'Get this maccy and cheese',
            'ingredients': '8 blocks of cheddar',
            'method': 'Put all the ingredients',
            'tags': 'cheese, slow',
            'image': 'some image link'
        })
        assert res.status == '200 OK'

    def test_delete_recipe(self):
        res = self.client.get('/recipes')
        ids = re.findall(r'href="/recipe/(\w+)"', res.data.decode("utf8"))
        assert len(ids) > 0
        res = self.client.post('/delete_recipe/{}'.format(ids[0]), follow_redirects=True)
        data = res.data.decode('utf-8')
        assert res.status == '200 OK'
        assert 'Mac and cheese' not in data
