from flask import Flask, render_template,request, flash,session, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import create_engine
import os
import psycopg2 #
# import psycopg2_binary #


engine = create_engine('postgres://vxxbdtrfdbkduh:55e6734be234734b9b746119746f69783826128cc99af69b7da1beb94a871534@ec2-34-193-232-231.compute-1.amazonaws.com:5432/d6if029a7f5jq1')
connection = engine.raw_connection()

app=Flask(__name__)
Bootstrap(app)


ENV = 'prod'

if ENV == 'dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:saisanju525@localhost/GAK'

else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vxxbdtrfdbkduh:55e6734be234734b9b746119746f69783826128cc99af69b7da1beb94a871534@ec2-34-193-232-231.compute-1.amazonaws.com:5432/d6if029a7f5jq1'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database creds
db_host = "ec2-34-193-232-231.compute-1.amazonaws.com"
db_port = "5432" #default postgres port
db_dbname = "d6if029a7f5jq1"
db_user = "vxxbdtrfdbkduh"
db_pw = "55e6734be234734b9b746119746f69783826128cc99af69b7da1beb94a871534"
db_conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_dbname, user=db_user, password=db_pw)
db_cursor = db_conn.cursor()


class GAK(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(100))

def __init__(self, first_name, last_name, username, email, password):
    # self.user_id = user_id
    self.first_name = first_name
    self.last_name = last_name
    self.username = username
    self.email = email
    self.password = password



app.config['SECRET_KEY'] = os.urandom(24)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userDetails = request.form
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match! Try again.', 'danger')
            return render_template('register.html')
        # cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO user(first_name, last_name, username, email, password) "\
        # "VALUES(%s,%s,%s,%s,%s)",(userDetails['first_name'], userDetails['last_name'], \
        # userDetails['username'], userDetails['email'], userDetails['password']))

        # mysql.connection.commit()
        # cur.close()
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        user_data = GAK(first_name=first_name, last_name=last_name, username=username, email =email, password = password)
        db.session.add(user_data)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        CheckUser = GAK.query.filter_by(username=username).first()

        if CheckUser is not None:
            if CheckUser.password == userDetails['password']:
                session['login'] = True
                session['firstName'] = CheckUser.first_name
                session['lastName'] = CheckUser.last_name
                flash('Welcome ' + session['firstName'] +'! You have been successfully logged in', 'success')
            else:
                cur.close()
                flash('Password does not match', 'danger')
                return render_template('login.html')
        else:
            flash('User not found', 'danger')
            return render_template('login.html')
        return redirect('/')
    return render_template('login.html')

@app.route('/logout/')
def logout():
    session.clear()
    flash("You have been logged out", 'info')
    return redirect('/')

if __name__ == '__main__':
    # app.debug = True
    app.run();
