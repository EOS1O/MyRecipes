from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, session, render_template, redirect, url_for, g
import sqlite3
from sqlalchemy import exists

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + "9900database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "MyRecipe"

db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = "Users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    phone_number = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(32), nullable=False)
    photo = db.Column(db.Text, nullable=False)
    num_followers = db.Column(db.Integer, nullable=False)
    liked_id = db.Column(db.Text)
    subscribed_id = db.Column(db.Text)
    my_recipes = db.Column(db.Text)


class Recipes(db.Model):
    __tablename__ = "Recipes"
    recipes_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, nullable=False)
    recipes_name = db.Column(db.String(32), nullable=False)
    photo = db.Column(db.Text, nullable=False)
    create_date = db.Column(db.Text, nullable=False)
    modify_time = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    meal_type = db.Column(db.Text, nullable=False)
    methods = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    num_subscribed = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.String(32), nullable=False)


# @app.before_request
# def is_login():
#     if request.path == "/login":
#         return None
#
#     if not session.get("user"):
#         render_template("login.html")

@app.before_request
def before_request():
    # initialize user
    g.user = None
    # check login state before every request
    if 'email' in session:
        user = Users.query.filter_by(email=session['email']).first()
        g.user = user


@app.route("/profile123", methods=["GET", "POST"])
def profile123():
    return render_template("profile.html")


@app.route("/", methods=["GET", "POST"])
def homepage():
    # data = request.get_json()
    operation = request.form.get('operation')
    print(operation, "operation")
    input_email = request.form.get('email')
    if input_email:
        session.pop('email', None)
        # get_data = request.get_json()
        # email = get_data.get("email", None)
        # password = get_data.get("password", None)
        email = request.form.get("email")
        password = request.form.get("password")
        user = Users.query.filter_by(email=email).first()
        # Incomplete input
        if not all([email, password]):
            return jsonify(msg="Error Input")
        # user exists
        if user:
            # login success
            if user.password == password:
                session["email"] = user.email
                return render_template("homepage.html", userName=user.name, userId=user.user_id)
            # wrong password
            else:
                return jsonify(msg="Wrong password")
        # user not exist
        else:
            return jsonify(msg="User not exist")

    if operation == 'logout':
        session.pop("email", None)

    if operation == 'news':
        # return first three recipes temporarily
        recipe = Recipes.query.filter(Recipes.recipes_id <= 3)
        dic = []
        for r in recipe:
            content = {"description": r.description, "modify_time": r.modify_time, "photo": r.photo,
                       "create_date": r.create_date, "likes": r.likes}
            dic.append(content)
        res = {'news_data': dic}
        return jsonify(res)
    return render_template("homepage.html")


@app.route("/profile", methods=["GET", "POST", "DELETE"])
def profile():
    # delete the recipe that user has created before
    operation = request.form.get('operation')

    if operation == 'delete':
        # return jsonify({'result': 'delete success'})
        user_id = request.form.get("user_id")
        delete_id = request.form.get("recipes_id")
        user = Users.query.filter(Users.user_id == user_id).first()
        recipe_list = user.my_recipes.split(',')
        recipe_list.remove(delete_id)
        user.my_recipes = ','.join(recipe_list)
        db.session.commit()
        dic = []
        if len(recipe_list):
            for i in recipe_list:
                recipe = Recipes.query.filter(Recipes.recipes_id == i).first()
                content = {"recipes_id": recipe.recipes_id, "name": recipe.recipes_name, "photo": recipe.photo}
                dic.append(content)
        res = {'data': dic}
        return jsonify(res)
    # unlike a recipe
    if operation == 'unlike':
        data = request.get_json()
        user_id = data.get("user_id")
        unlike_id = data.get("recipes_id")
        user = Users.query.filter(Users.user_id == user_id).first()
        liked_list = user.liked_id.split(',')
        liked_list.remove(unlike_id)
        user.liked_id = ','.join(liked_list)
        db.session.commit()
        dic = []
        if len(liked_list):
            for i in liked_list:
                recipe = Recipes.query.filter(Recipes.recipes_id == i).first()
                content = {"recipes_id": recipe.recipes_id, "name": recipe.recipes_name, "photo": recipe.photo}
                dic.append(content)
        res = {'data': dic}
        return jsonify(res)


@app.route("/profile1", methods=["GET", "POST"])
def profile1():
    email = session.get('email')
    user = Users.query.filter(Users.email == email).first()
    recipes = get_user_recipe(user.name)
    likes = get_user_like(user.name)
    print(likes)
    subscripts = get_user_subscript(user.name)
    if user:
        return render_template("profile.html", photo=user.photo, username=user.name, email=email,
                               fans=user.num_followers, recipes=recipes, likes=likes, subscripts=subscripts)
    return render_template("profile.html")


@app.route("/userInfo", methods=["POST"])
def get_user_info():
    name = request.form.get("name")
    user = Users.query.filter(Users.name == name).first()
    if user:
        res = {'photo': user.photo}
        return jsonify(res)
    else:
        return jsonify({})


# @app.route("/userRecipe", methods=["POST"])
def get_user_recipe(name):
    # name = request.form.get("name")
    user = Users.query.filter(Users.name == name).first()
    res = dict()
    if user:
        recipe = user.my_recipes
        recipes = Recipes.query.filter(Recipes.recipes_id == recipe)
        for recipe in recipes:
            res[recipe.recipes_id] = {"name": recipe.recipes_name, "photo": recipe.photo, "recipe_id": recipe.recipes_id}
        # return jsonify(res)
    else:
        # return jsonify({})
        pass
    return res


# @app.route("/userLike", methods=["POST"])
def get_user_like(name):
    # name = request.form.get("name")
    user = Users.query.filter(Users.name == name).first()
    res = dict()
    if user:
        like_ids = str(user.liked_id).split(',')
        for like_id in like_ids:
            recipes = Recipes.query.filter(Recipes.recipes_id == like_id)
            for recipe in recipes:
                res[recipe.recipes_id] = {"name": recipe.recipes_name, "photo": recipe.photo}
        # return jsonify(res)
    else:
        pass
        # return jsonify({})
    return res

# @app.route("/userSubscript", methods=["POST"])
def get_user_subscript(name):
    # name = request.form.get("name")
    user = Users.query.filter(Users.name == name).first()
    res = dict()
    if user:
        subscribed_ids = str(user.subscribed_id).split(',')
        print(subscribed_ids)
        for subscribed_id in subscribed_ids:
            subscribed = Users.query.filter(Users.user_id == subscribed_id).first()
            res[subscribed.user_id] = {"name": subscribed.name, "photo": subscribed.photo}
        #     recipes = Users.query.filter(Users.user_id == subscript_id)
        #     print(recipes)
            # for recipe in recipes:
            #     res[recipe.recipes_id] = {"name": recipe.recipes_name, "photo": recipe.photo}
        # return jsonify(res)
    else:
        pass
        # return jsonify({})
    return res


app.run()
