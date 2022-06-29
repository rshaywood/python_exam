from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'tv_shows'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.shows = []

# CREATE - SQL

    @classmethod
    def create_user(cls, data):
        if not cls.validate_user_reg_info(data):
            return False
        data = cls.parse_reg_info(data)
        query = """
        INSERT INTO users (first_name,last_name,email,password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query,data)
        session['user_id'] = user_id
        return user_id

# READ - SQL

    @classmethod
    def get_user_by_email(cls, email):
        print(email)
        data = {'email' : email}
        query = """
        SELECT * FROM users
        WHERE email = %(email)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
            print(result)
        return result

    @classmethod
    def get_user_by_id(cls, id):
        print(id)
        data = {'id' : id}
        query = """
        SELECT * FROM users
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
            print(result)
        return result

# VALIDATE - SQL

    @staticmethod
    def validate_user_reg_info(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        print(results)
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters!","register")
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters!","register")
            is_valid= False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!","register")
            is_valid=False
        if User.get_user_by_email(user['email'].lower()):
            flash("Email already taken!","register")
            is_valid=False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters!","register")
            is_valid= False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match!","register")
            is_valid = False
        return is_valid

    @staticmethod
    def login(data):
        this_user = User.get_user_by_email(data['email'].lower())
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                return True
        flash("Your credentials are incorrect!", "login")
        return False

    @staticmethod
    def parse_reg_info(data):
        user_data = {}
        user_data['first_name'] = data['first_name']
        user_data['last_name'] = data['last_name']
        user_data['password'] = bcrypt.generate_password_hash(data['password'])
        user_data['email'] = data['email'].lower()
        return user_data