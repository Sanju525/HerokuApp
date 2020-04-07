from flask import Flask, render_template,request, flash,session, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import create_engine
import os
import psycopg2 #
# import psycopg2_binary #


engine = create_engine('postgres://zxfdnzvyrrwmpy:86c26a4f57b0edf1e3909c4e73b69778f079ad66663a290c26eab1e4d91c649f@ec2-54-159-112-44.compute-1.amazonaws.com:5432/d8mm5gghspjd2h')
connection = engine.raw_connection()

app=Flask(__name__)
Bootstrap(app)


ENV = 'prod'

if ENV == 'dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:saisanju525@localhost/GAK'

else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zxfdnzvyrrwmpy:86c26a4f57b0edf1e3909c4e73b69778f079ad66663a290c26eab1e4d91c649f@ec2-54-159-112-44.compute-1.amazonaws.com:5432/d8mm5gghspjd2h'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database creds
db_host = "localhost"
db_port = "5432" #default postgres port
db_dbname = "GAK"
db_user = "postgres"
db_pw = "saisanju525"
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
        cur = db_cursor
        # resultValue = cur.execute("SELECT * FROM user WHERE username = %s", ([username]))
        # resultValue=db.session.query(GAK).filter(GAK.username == username ).count();
        # CheckPAssword=db_cursor.execute("SELECT * FROM user WHERE username = %s",([username]))
        # cur.execute("use GAK;")
        # CheckPAssword=cur.execute("SELECT password FROM public.user WHERE username='sanju5';")
        CheckUser = GAK.query.filter_by(username=username).first()
        print(CheckUser.username) #return value in none ------------------------------ for the above cmd????????????

        if CheckUser is not None:
            # user = cur.fetchone()

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
            # cur.close()
            flash('User not found', 'danger')
            return render_template('login.html')
        # cur.close()
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
