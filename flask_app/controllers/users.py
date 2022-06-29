from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

# CREATE - ROUTES

@app.route('/user/create', methods=['POST'])
def create_user():
    new_user = User.create_user(request.form)
    if new_user:
        return redirect('/dashboard')
    return redirect('/')

# READ - ROUTES

@app.route('/')
def landing_page():
    return render_template('reg_login.html')

# LOGiIN/OUT - ROUTES

@app.route('/user/login', methods=['POST'])
def login():
    if User.login(request.form):
        return redirect('/dashboard')
    return redirect('/')

@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')