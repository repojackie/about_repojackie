"""
ABOUT_REPOJACKIE -> Backend using Python-Flask

Used tutorials from PrettyPrinted among other to learn about WTForms
TO-DO: 
    [] Backend for blog - Create an account and allow people to post on certain circumstances? 
"""
from flask import Flask, request, render_template, redirect, url_for
from flask_socketio import SocketIO
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from datetime import datetime

"""
I will look into splitting this into separate files as times goes on-- look up Flask blueprinting?
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mySHITTYbeingisSURREAL'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
socketio = SocketIO(app)

# associated with each users identity
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

# for when a user decides to post
class BlogPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    true_author = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(30), unique=True, nullable=False)
    blurb = db.Column(db.Text(), nullable=False)
    time = db.Column(db.DateTime(), default=datetime.utcnow)

db.create_all()
db.session.commit()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'),Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

# homepage 
@app.route("/")
def hello():
    return render_template("homepage.html")

# portfolio
@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

# chat room
@app.route("/chatroom", methods=['GET', 'POST'])
def chatroom(methods=['GET', 'POST']):
    return render_template("chatroom.html")

#############################################################################

# blog
@app.route("/blog")
def blog():
    return render_template("blog.html")

# for editing new posts
@app.route("/blog/new_post", methods=["GET", "POST"])
@login_required
def blog_new_post():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        blurb = request.form['blurb']
        
        new_post = BlogPosts(title=title, author=author, blurb=blurb, true_author=current_user.username)

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("blog"))
    return render_template("blog_new_post.html", name=current_user.username)

# sign up for blog posting 
@app.route("/blog/signup", methods=["GET", "POST"])
def blog_signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1> NEW USER HAS BEEN CREATED! </h1>'
    return render_template("blog_signup.html", form=form)

# sign in for blog 
@app.route("/blog/login", methods=["GET", "POST"])
def blog_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                print(url_for('blog'))
                return redirect(url_for('blog'))                        
                
        return '<h1> INVALID USERNAME OR PASSWORD </h1>'
    return render_template("blog_login.html", form=form)


#######################################################################


# external links and outlook
@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print("received an event: " + str(json))
    if (len(json) > 1):
        # not emitting preliminary connection message!
        socketio.emit('my response', json, callback=messageReceived)

if __name__ == "__main__":
    socketio.run(app, debug=True)
