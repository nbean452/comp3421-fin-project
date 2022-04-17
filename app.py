from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'comp3421-fin-project'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    tasks = db.relationship('Task', backref='user')


class Task(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    ownerid = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(20), nullable=False)
    completion = db.Column(db.Boolean, nullable=False, default=False)
    desc = db.Column(db.String(400), nullable=True)
    creationdate = db.Column(db.DateTime, nullable=False,
                             default=datetime.now)
    duedate = db.Column(db.DateTime, nullable=False,
                        default=datetime.now)
    # id, ownerid, name, completion, description, creation date


class RegisterForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(
        min=2, max=20)], render_kw={"placeholder": "First Name"})
    lastname = StringField(validators=[Length(min=2, max=20)], render_kw={
                           "placeholder": "Last Name"})
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    msg = ""

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('todo'))
            else:
                msg = "Username / Password is incorrect."
                return render_template('login.html', form=form, msg=msg)
        else:
            msg = "Username / Password is incorrect."
            return render_template('login.html', form=form, msg=msg)

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(firstname=form.firstname.data, lastname=form.lastname.data,
                        username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect((url_for('register_success')))

    return render_template('register.html', form=form)


@app.route('/register/success')
def register_success():

    return render_template('success.html')


@app.route('/todo')
@login_required
def todo():
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('to-do.html', user=user)


@app.route('/addtask', methods=['POST'])
def addtask():

    taskname = request.form.get("taskName")
    taskdesc = request.form.get("descr")
    # the form returns a string of the date
    duedate_string = request.form.get("dueDate")

    # convert string to date object
    duedate = datetime.strptime(duedate_string, '%Y-%m-%d').date()

    new_task = Task(user=current_user, name=taskname,
                    desc=taskdesc, duedate=duedate)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('todo'))


@app.route('/updatetask/<int:task_id>')
@login_required
def updatetask(task_id):

    task = Task.query.filter_by(id=task_id).first()
    if current_user.id != task.ownerid:
        return redirect(url_for('todo'))
    task.completion = not task.completion
    db.session.commit()
    return redirect(url_for('todo'))


@app.route('/deletetask/<int:task_id>')
@login_required
def deletetask(task_id):

    task = Task.query.filter_by(id=task_id).first()
    if current_user.id != task.ownerid:
        return redirect(url_for('todo'))
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('todo'))


@app.route('/todo/calendar')
@login_required
def calendar():
    user = User.query.filter_by(username=current_user.username).first()
    tasks_list = []

    for task in user.tasks:
        task_dict = {}
        task_dict["name"] = task.name
        task_dict["date"] = task.duedate.strftime("%Y-%m-%d")
        tasks_list.append(task_dict)

    return render_template('calendar.html', user=user, tasks_list=tasks_list)


if __name__ == '__main__':

    db.create_all()

    app.run(debug=True, port=5500)
