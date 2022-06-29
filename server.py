from flask import Flask
from flask_app import app
from flask_app.controllers import shows, users
from flask_app.models import show
from flask_app.models import user

if __name__ == "__main__":
    app.run(debug=True)