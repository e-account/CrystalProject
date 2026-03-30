# importing an instance of os to help open or read files and interact with system specific functionality
import os
# class instances listed below:
import datetime
# flask functionality for building the webpages and broader infrastructure for a webapp, importing "all"
from flask import *
# a flask extension that helps import jinja macros and templates
from flask_bootstrap import Bootstrap
# flask wtf and wtforms act as an efficient template manager for webforms and inputs, importing all from wtforms
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
# a lightweight sqlite database to quick and efficient web development
from flask_sqlalchemy import SQLAlchemy
# main application constructor classes
app = Flask(__name__)
bootstrap = Bootstrap(app)
# set to allow for direct access to the root path of the application environment
basedir = os.path.abspath(os.path.dirname(__file__))
# Secret key for securing the config part of the application
app.config['SECRET_KEY'] = 'thisisaninvalidsecretkey'
# sqlalchemy database pathway config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# database object constructor
db = SQLAlchemy(app)
# Debug variable held externally from the app.run command to allow for easier debug management
Debug = True

# constructor class for the database table "user"
class User(db.Model):
    __tablename__ = 'user'
    # an auto-incrementing value that acts as the primary identifier for user data
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    forename = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    # a back-referenced link that allows for easier object referencing between the User and Ticket classes
    tickets = db.relationship('Ticket', backref='user', lazy=True)

    # a back-referenced link that allows for easier object referencing between the User and Team classes
    team = db.relationship('Team', backref='user', lazy=True)

    # __repr__ returns a string of the current object which helps for debugging and interacting with the database
    def __repr__(self):
        return f'<User: {self.username} ID[{self.id}], Is Admin: {self.admin}>'

# constructor class for the database table "ticket"
class Ticket(db.Model):
    __tablename__ = 'ticket'
    # an auto-incrementing value that acts as the primary identifier for user ticket data
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    verif = db.Column(db.Boolean, nullable=False, default=False)

    # linking two of the classes together with user.username as the primary key
    userkey = db.Column(db.String(128), db.ForeignKey('user.username'))

    # __repr__ returns a string of the current object which helps for debugging and interacting with the database
    def __repr__(self):
        return (f'<Ticket: {self.userkey}, Ticket No. {self.id}, Ticket: {self.title},'
                f' Type: {self.type}, Description: {self.desc}>')

class Team(db.Model):
    __tablename__ = 'team'
    # an auto-incrementing value that acts as the primary identifier for crystal team data
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    type = db.Column(db.String(128), nullable=False)
    size = db.Column(db.Integer, nullable=False)

    # linking two of the classes together with user.username as the primary key
    teamkey = db.Column(db.String(128), db.ForeignKey('user.username'))

    # __repr__ returns a string of the current object which helps for debugging and interacting with the database
    def __repr__(self):
        return (f'<Team: {self.name}, Crystal Type: {self.type}, Team Size: {self.size}>')

# Shell integration that helps to recall objects and debug the Sqlite database within instance
@app.shell_context_processor
def make_shell_context():
    # dictionary terms used for interfacing with the database in the python shell
    return dict(db=db, User=User, Ticket=Ticket, Team=Team)


@app.route('/', methods=['GET', 'POST'])
def main():
    maintitle= "welcome to the app"
    return render_template('base.html', maintitle=maintitle)

# Calls all contexts of the application to allow for the new database classes to be created
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=Debug)