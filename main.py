from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    birthdate = db.Column(db.Date())
    age = db.Column(db.Integer())

def __init__(self, name, email, birthdate, age):
    self.name = name
    self.email = email
    self.birthdate = birthdate
    self.age = age

def calculate_age(birthdate):
    today = datetime.today()
    born = datetime.strptime(birthdate, '%Y-%m-%d')
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return int(age)

def format_birthdate(birthdate):
    return datetime.strftime(birthdate, '%B %-d, %Y')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/users')
def index():
    users = User.query.all()
    for user in users:
        user.birthdate = format_birthdate(user.birthdate)

    return render_template('index.html', users=users)

@app.route('/users/new', methods = ['GET', 'POST'])
def new():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        birthdate = request.form['birthdate']

        errors = []
        if not name:
            errors.append('name')
        
        if not email:
            errors.append('email')
        
        if not birthdate or birthdate == 'dd/mm/yyyy':
            errors.append('date of birth')

        if errors:
            flash(f"Please enter fields {', '.join(errors)}.", 'error')
        else:
            user = User(
                name=name,
                email=email,
                birthdate=datetime.strptime(birthdate, '%Y-%m-%d'),
                age=calculate_age(birthdate)
            )
            db.session.add(user)
            db.session.commit()
            flash('Record was successfully added', 'success')
            return redirect(url_for('index'))
    return render_template('new.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)