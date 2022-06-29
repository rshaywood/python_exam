from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
bcrypt = Bcrypt(app) 

class Show:
    db = "tv_shows"

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.description = data['description']
        self.release_date = data['release_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.viewer = None

# CREATE - SQL

    @classmethod
    def add_show(cls, data):
        query = """
        INSERT INTO shows (title, network, description, release_date, user_id) 
        VALUES (%(title)s, %(network)s, %(description)s, %(release_date)s, %(user_id)s)
        ;"""
        show_id = connectToMySQL(cls.db).query_db(query,data)
        return show_id

# READ - SQL

    @classmethod
    def get_all_shows(cls):
        query = """SELECT * FROM shows;"""
        shows_from_db = connectToMySQL(cls.db).query_db(query)
        list_of_show_data = []
        for row in shows_from_db:
            list_of_show_data.append(cls(row))
        return list_of_show_data

    @classmethod
    def get_show_by_id(cls, data):
        query = """
        SELECT * FROM shows
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_one_show_with_user(cls, data):
        query = """
        SELECT *
        FROM shows
        LEFT JOIN users on shows.user_id = users.id
        WHERE shows.id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            return result
        current_show = result[0]
        one_show = cls(current_show)            
        this_viewer = {
            'id': current_show['users.id'],
            'first_name': current_show['first_name'],
            'last_name': current_show['last_name'],
            'email': current_show['email'],
            'password': current_show['password'],
            'created_at': current_show['users.created_at'],
            'updated_at': current_show['users.updated_at'],
        }
        print("^^^^^^^^^^^^^^^^^^^^^", this_viewer)
        one_show.viewer = user.User(this_viewer)
        return one_show

# UPDATE - SQL

    @classmethod
    def edit_show(cls, data):
        query = """
        UPDATE shows SET title = %(title)s, description = %(description)s, release_date = %(release_date)s, network = %(network)s, created_at = NOW(), updated_at = NOW()
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

# DELETE - SQL

    @classmethod
    def remove_show(cls, id):
        data = { 'id': id }
        query = "DELETE FROM shows WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

# VALIDATE - SQL

    @staticmethod
    def validate_show_info(show):
        is_valid = True
        query = "SELECT * FROM shows WHERE id = %(id)s;"
        results = connectToMySQL(Show.db).query_db(query, show)
        print(results)
        if not show['title']:
            flash("Title of the show must be at least 3 characters.","create_show")
            is_valid= False
        if len(show['description']) < 3:
            flash("Description of show must be at least 3 characters.","create_show")
            is_valid= False
        if len(show['release_date']) < 1:
            flash("Please include a release date!","create_show")
            is_valid= False
        if len(show['network']) < 1:
            flash("Please include the network the show aired on!","create_show")
            is_valid= False         
        return is_valid
