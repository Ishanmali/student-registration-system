from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///signup.db'
app.config["SQLALCHEMY_BINDS"] = {'register': 'sqlite:///register.db'}
app.secret_key = 'iikdjgkxjkhdk'

db = SQLAlchemy(app)

class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Register(db.Model):
    __bind_key__ = "register"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    birthday = db.Column(db.String(10))
    Address = db.Column(db.String(500))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100), unique=True, nullable=False)
    course = db.Column(db.String(100)) 

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Signup.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['email'] = user.email
            session['password'] = user.password
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid user')

    return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        existing_user = Signup.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already used', category='error')
        elif password != password2:
            flash('Passwords do not match!', category='error')
        elif len(password) < 5:
            flash('Password must have a minimum of 5 characters', category='error')
        else:
            new_user = Signup(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', category='success')
            return redirect('/login')

    return render_template('signup.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        birthday = request.form['birthday']
        Address = request.form['Address']
        phone = request.form['phone']
        email = request.form['email']
        course = request.form['course']  

        existing_register =  Register.query.filter_by(email=email).first()
        if existing_register:
            flash('You already Registed', category='error')
        elif len(phone)< 10:
             flash('Mobile number too short', category='error')
        else:    
            new_register = Register(name=name, birthday=birthday, Address=Address, phone=phone, email=email, course=course)
            db.session.add(new_register)
            db.session.commit()
            flash('you successfully registed!', category='success')
            return redirect(url_for('home'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

