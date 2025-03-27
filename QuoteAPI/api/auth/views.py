from api.models.user import UserModel
from api.auth.forms import LoginForm, RegistrationForm
from flask import render_template, request, redirect, url_for, abort, session, Blueprint, flash
from api import db

auth = Blueprint('auth', __name__)


@auth.get("/auth")
@auth.get("/auth/home")
def home():
    return render_template("home.html")


@auth.route("/auth/register", methods=["GET, POST"])
def register():
    #проверка тотЁ что пользователь уже залогинен
    #если он залогиненЁ то он уже есть в сессии
    if session.get("username"):
        flash("You are already logged in", "info")
        return redirect(url_for('auth.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        #проверка на наличие такого же пользователя
        existing_username = db.session.scalars(db.select(UserModel).where(UserModel.username.like("%"+username+"%")))

        if existing_username:
            flash("This user already exists. Try another name", "waring")
            return render_template("register.html", form=form)

        user = UserModel(username, password)
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(503, f'Database error: {str(e)}')
        flash("You are now registered! Please log in.", "success")
        return redirect(url_for("auth.login"))
    
    if form.errors:
        flash(form.errors, "danger")
    #GET request
    return render_template("register.html", form=form)


@auth.route("/auth/login", methods=["GET, POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            existing_username = db.session.scalars(db.select(UserModel).where(UserModel.username==username)).one_or_none()
        except Exception as e:
            abort(503, f'Database error: {str(e)}')

        if not (existing_username and existing_username.verify_password(password)):
            flash("Invalid password or username. Please try again", "danger")
            return render_template("login.html", form=form)
        
        #если пользователь существлует, то мы сохраняем его в сессию
        session["username"] = username
        flash("You are successfully registered", "success")
        return redirect(url_for("auth.home"))
    
    if form.errors:
        flash(form.errors, "danger")
    #GET request
    return render_template("login.html", form=form)


@auth.route("/auth/logout")
def logout():
    if "username" in session:
        session.pop("username")
        flash("You are successfully logout", "success")
    return redirect(url_for("auth.home"))