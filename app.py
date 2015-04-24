from flask import Flask, render_template, url_for, request, redirect, session,\
        flash, g
from functools import wraps
import sqlite3

app = Flask(__name__)

app.secret_key = 'my precious'
app.database = 'sample.db'


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# Home page.  Shows off posts from the posts table.
# Only accessible when logged in.  Redirects to the login page
# if accessed without logging in.
@app.route('/')
@login_required
def home():
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(title=row[0], description=row[1])
            for row in cur.fetchall()]
    g.db.close()
    return render_template('index.html', posts=posts)


# Welcome page
@app.route('/welcome')
def welcome():
    return render_template("welcome.html")


# Login page.
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'admin':
            error = 'Invalid credentials.  Please try again.'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('home'))
    return render_template("login.html", error=error)


# Log out page.  Requires the user to log in.
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))


def connect_db():
    return sqlite3.connect(app.database)


if __name__ == "__main__":
    app.run(debug=True)