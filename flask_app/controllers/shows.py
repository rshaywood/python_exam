from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import show
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

# CREATE - ROUTES

@app.route('/show/form')
def new_show_form():
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('add.html', this_user=this_user)


@app.route('/show/create', methods=['POST'])
def add_show():
    if "user_id" not in session:
        return redirect('/')
    if not show.Show.validate_show_info(request.form):
        return redirect('/show/form')
    data = {
        "title": request.form['title'],
        "description": request.form['description'],
        "release_date": request.form['release_date'],
        "network": request.form['network'],
        "user_id" : session['user_id']
    }
    show.Show.add_show(data)
    return redirect('/dashboard')

# READ - ROUTES

@app.route('/dashboard')
def view_dashboard():
    all_shows = show.Show.get_all_shows()
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('view_dash.html', all_shows = all_shows, this_user=this_user)

@app.route('/show/display/<int:id>')
def display_one_show(id):
    data = {"id":id}
    one_show_with_user = show.Show.get_one_show_with_user(data)
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('view_one.html', one_show_with_user = one_show_with_user, this_user=this_user)

# UPDATE - ROUTES

@app.route('/show/edit/<int:id>')
def display_edit_show_form(id):
    data = {"id":id}
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('edit.html', one_show = show.Show.get_show_by_id(data), this_user=this_user)

@app.route('/show/edit', methods=['POST'])
def update_show():
    if "user_id" not in session:
        return redirect('/')
    if not show.Show.validate_show_info(request.form):
        return redirect('/show/edit/<')
    data = {
        "title": request.form['title'],
        "description": request.form['description'],
        "release_date": request.form['release_date'],
        "network": request.form['network'],
        "user_id" : session['user_id'],
        'id': request.form['id']
    }
    show.Show.edit_show(data)
    return redirect('/dashboard')

# DELETE - ROUTES

@app.route('/show/delete/<int:id>')
def remove_show(id):
    show.Show.remove_show(id)
    return redirect('/dashboard')

# @app.route('/show/delete/<int:id>')
# def remove_show(id):
#     # data = {"id":id}
#     # this_show = show.Show.get_show_by_id(data)
#     # if this_show.user_id == session['user_id']:
#     all_shows = show.Show.get_all_shows()
#     this_user = user.User.get_user_by_id(session['user_id'])
#     show.Show.remove_show(id)
#     return render_template('view_dash.html', this_user=this_user, all_shows=all_shows)
#     # return render_template('nope.html')