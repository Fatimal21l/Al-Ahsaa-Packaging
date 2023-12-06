from flask import Flask, render_template, request, abort, flash, redirect, url_for
from constants import SLIDER_CONTENT, PACKAGES
from forms import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)

app.config['SECRET_KEY'] = "change-me-this-is-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///main.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app=app)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


with app.app_context():
    db.create_all()


@login_manager.user_loader
def user_loder(user_id):
    return User.query.get(user_id)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = request.form.get('email')
        is_email_registered = User.query.filter_by(email=email).first()
        if is_email_registered:
            login_password = request.form.get('password')
            is_password_match = check_password_hash(
                is_email_registered.password, login_password)
            if is_password_match:
                print("Logged in")
                login_user(is_email_registered)
                return redirect(url_for('packages'))
        flash('Wrong Email/Password')
    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if request.method == 'POST':
        is_user_exist = db.session.execute(
            db.select(User).where(User.email == request.form.get('email'))).scalar()
        if is_user_exist:
            print('user exist')
            flash('An account is registered with this email, login instead')
            return redirect(url_for('login'))
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.password = generate_password_hash(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created')
        print("Register successful")
        return redirect(url_for('packages'))
    return render_template("signup.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/about")
def about():
    return render_template("about.html", slides=SLIDER_CONTENT, logged_in=current_user.is_authenticated)


@app.route("/packages")
def packages():
    return render_template("packages.html", packages=PACKAGES, logged_in=current_user.is_authenticated)


@app.route("/package/<pid>")  # type: ignore
def package(pid):
    try:
        if int(pid) > 4:
            return abort(404)
        return render_template("package.html", package=PACKAGES[int(pid)-1], logged_in=current_user.is_authenticated)
    except ValueError:
        return abort(400)


@app.route("/checkout/<pid>")  # type: ignore
def checkout(pid):
    try:
        if int(pid) > 4:
            return abort(404)
        return render_template("checkout.html", packages=[PACKAGES[int(pid)-1]], total=PACKAGES[int(pid)-1]["price"], logged_in=current_user.is_authenticated)
    except ValueError:
        return abort(400)


@app.route("/thanks")
def thanks():
    return render_template("thanks.html", logged_in=current_user.is_authenticated)


if __name__ == "__main__":
    app.run(debug=True)
