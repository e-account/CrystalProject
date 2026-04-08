# importing an instance of os to help open or read files and interact with system specific functionality
import os
# class instances listed below:
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
# importing the dotenv instance to store important environment variables within the .env file
from dotenv import load_dotenv
load_dotenv()
# main application constructor classes
app = Flask(__name__)
bootstrap = Bootstrap(app)
# set to allow for direct access to the root path of the application environment
basedir = os.path.abspath(os.path.dirname(__file__))
# Secret key for securing the config part of the application
app.config['SECRET_KEY'] = os.getenv('SECURITY')
# sqlalchemy database pathway config that will track updates to the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASECONFIG') + os.path.join(basedir, os.getenv('DATABASENAME'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQL-TRACK-MOD')
# database object constructor
db = SQLAlchemy(app)
# Debug variable held externally from the app.run command to allow for easier debug management
Debug = os.getenv('DEBUG')
# Universal variables to check for the current user access across accounts
active_user = os.getenv('USER')
active_admin = os.getenv('ADMIN')

# constructor class for the database table "user"
class User(db.Model):
    __tablename__ = 'user'
    # an auto-incrementing value that acts as the primary identifier for user data
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    forename = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Integer, nullable=False, default=0)

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
    verif = db.Column(db.Integer, default=0, nullable=False)

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
        return f'<Team: {self.name}, Crystal Type: {self.type}, Team Size: {self.size}>'

# constructor class for the website main menu
class MainMenu(FlaskForm):
    signup = SubmitField('signup')
    login = SubmitField('login')

# constructor class for the website Signup page
class Signup(FlaskForm):
    # each object has the validator that requires all user inputs for the form to be submitted
    username = StringField('Input Username:', validators=[DataRequired(), Length(min=5, max=128)])
    password = StringField('Input Password:', validators=[DataRequired(), Length(min=5, max=128)])
    forename = StringField('Input Forename:', validators=[DataRequired(), Length(min=2, max=128)])
    surname = StringField('Input Surname:', validators=[DataRequired(), Length(min=2, max=128)])
    submit = SubmitField('Submit')

# constructor class for the website Login class
class Login(FlaskForm):
    # each object has the validator that requires all user inputs for the form to be submitted
    username = StringField('Input Username:', validators=[DataRequired(), Length(min=5, max=128)])
    password = StringField('Input Password:', validators=[DataRequired(), Length(min=5, max=128)])
    submit = SubmitField('Submit')

# constructor class for the homepage for user interaction
class Homepage(FlaskForm):
    # each field is a submitfield/button that will allow users to follow through to other aspects of the website
    newticket = SubmitField('Create Ticket')
    viewticket = SubmitField('View Tickets')
    viewaccount = SubmitField('View Account')
    logout = SubmitField('Log Out')

# constructor class for the admin homepage
class Admin(FlaskForm):
    # each field is a submitfield/button that will allow users to follow through to other aspects of the website
    viewticket = SubmitField('View Tickets')
    viewusers = SubmitField('View Users')
    newteams = SubmitField('Create Team')
    viewteams = SubmitField('View Teams')
    logout = SubmitField('Log Out')

# constructor class for the main ticket input page
class NewTicket(FlaskForm):
    type = SelectField('Ticket Classification: ', choices=[('Task - Low Priority', 'Task - Low Priority'), ('Task - Medium Priority', 'Task - Medium Priority'), ('Task - High Priority', 'Task - High Priority'),
                                                           ('Change - Low Priority', 'Change - Low Priority'), ('Change - Medium Priority', 'Change - Medium Priority'), ('Change - High Priority', 'Change - High Priority'),
                                                           ('Bug - Low Priority', 'Bug - Low Priority'), ('Bug - Medium Priority', 'Bug - Medium Priority'), ('Bug - High Priority', 'Bug - High Priority')])

    title = StringField('Ticket Title: ', validators=[DataRequired(), Length(min=2, max=128)])
    desc = TextAreaField('Ticket Description: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

# constructor class for the admin ticket approval
class TicketApproval(FlaskForm):
    approve = SubmitField('Approve')

# constructor class for the admin and user ticket deletion
class TicketDeletion(FlaskForm):
    delete = SubmitField('Delete')

# constructor class to create EditAccount Class
class EditAccount(FlaskForm):
    username = StringField('Change Username:', validators=[DataRequired(), Length(min=5, max=128)])
    password = StringField('Change Password:', validators=[DataRequired(), Length(min=5, max=128)])
    forename = StringField('Change Forename:', validators=[DataRequired(), Length(min=2, max=128)])
    surname = StringField('Change Surname:', validators=[DataRequired(), Length(min=2, max=128)])
    submit = SubmitField('Submit')

# constructor class to create EditTeam CLass
class EditTeam(FlaskForm):
    name = StringField('Change Team Name: ', validators=[DataRequired(), Length(min=5, max=128)])
    type = SelectField('Change Crystal Type: ', choices=[('Clear - 1-6 Members', 'Clear - 1-6 Members'),
                                                  ('Yellow - 7-20 Members', 'Yellow - 7-20 Members'),
                                                  ('Orange - 21-40 Members', 'Orange - 21-40 Members'),
                                                  ('Red - 41-100 Members', 'Red - 41-100 Members')])
    size = IntegerField('Change Team Size: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

# constructor class to create Delete Account class
class DeleteAccount(FlaskForm):
    delete = SubmitField('Submit')

# constructor class to create Team Creation Class
class Teams(FlaskForm):
    name = StringField('Team Name: ', validators=[DataRequired(), Length(min=5, max=128)])
    type = SelectField('Crystal Type: ', choices=[('Clear - 1-6 Members', 'Clear - 1-6 Members'), ('Yellow - 7-20 Members', 'Yellow - 7-20 Members'),
                                                  ('Orange - 21-40 Members', 'Orange - 21-40 Members'), ('Red - 41-100 Members', 'Red - 41-100 Members')])
    size = IntegerField('Team Size: ', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Shell integration that helps to recall objects and debug the Sqlite database within instance
@app.shell_context_processor
def make_shell_context():
    # dictionary terms used for interfacing with the database in the python shell
    return dict(db=db, User=User, Ticket=Ticket, Team=Team)

# creates an application instance for the website homepage
@app.route('/', methods=['GET', 'POST'])
def main():
    global active_user, active_admin  # allows the app route to have access to the active variables
    active_user = False
    active_admin = False
    title = "Welcome to Crystal"
    form = MainMenu()
    if form.validate_on_submit():
        if request.method == 'POST':
            if 'signup' in request.form:
                return redirect('/signup')
            if 'login' in request.form:
                return redirect('/login')
    return render_template('home.html', title=title, form=form)

# creates an application instance for '/signup' webpage
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global active_user, active_admin  # allows the app route to have access to the active variables
    active_user = False
    active_admin = False
    # text that will be added to the html templates using bootstrap for efficiency, allowing templates to be reused
    title = "Crystal: Signup"
    formheader = "Create an account with Crystal"
    formtext = "Input your user details below to create an account:"
    # using the signup() flaskform template with bootstrap to create the webform templates
    form = Signup()
    if form.validate_on_submit():
        # account_search is a query that will check the sqlite database for the existence of an account with the same name as the user form input
        account_search = User.query.filter_by(username=form.username.data).first()
        if account_search is None:
            # if the account_search comes back with nothing then the user input will be formatted to be executed within a session to the database
            # even though it is preset within the class above, setting the admin to False here ensures that admin access isn't naturally set to true for accounts
            new_user = User(username=form.username.data, password=form.password.data,
                            forename=form.forename.data, surname=form.surname.data, admin=0)
            # opens a session with the database and commits the new account to memory
            db.session.add(new_user)
            db.session.commit()
            # sends the user to the login page to help with user experience with the website
            return redirect('/login')
        else:
            # sends the user back to the signup page to restart the signup process
            return redirect('/signup')
    return render_template('menu.html', title=title, form=form,
                           formheader=formheader, formtext=formtext)

# creates an application instance for '/login' webpage
@app.route('/login', methods=['GET', 'POST'])
def login():
    global active_user, active_admin  # allows the app route to have access to the active variables
    active_user = False
    active_admin = False
    # text that will be added to the html templates using bootstrap for efficiency, allowing templates to be reused
    title = "Crystal: Login"
    formheader = "Login to your Crystal account"
    formtext = "Input your user details below to login to your account:"
    form = Login()
    # queries to check whether a user exists and then can be used later to validate whether the user is an admin
    login_query = User.query.filter(User.username.in_([form.username.data]), User.password.in_([form.password.data])).first()
    if form.validate_on_submit():  # validation of login menu
        if login_query.admin == 0:
            active_user = True
            return redirect(url_for('user', users=form.username.data))
        elif login_query.admin == 1:
            active_admin = True
            return redirect(url_for('admin', users=form.username.data))
        else:  # else function that prevents non-logged in people from accessing the site through inputting random urls
            return redirect('/login')
    return render_template('menu.html', form=form, title=title,
                           formheader=formheader, formtext=formtext)

# creates an application instance for '/user/username' webpage
@app.route('/user/<string:users>', methods=['GET', 'POST'])
def user(users):
    global active_user, active_admin  # allows the app route to have access to the active variables
    # text that will be added to the html templates using bootstrap for efficiency, allowing templates to be reused
    title = "Crystal: Homepage"
    formheader = "Welcome ".join([users])  + " to your Crystal account"
    formtext = "Warning: Misuse of these systems can lead to legal consequences"
    form = Homepage()
    # search queries that validate the existence of a user account and whether that account is an admin or standard user account
    account_search = User.query.filter(User.username.in_([users])).first()
    if account_search is not None:
        if active_user == True:
            if form.validate_on_submit():  # redirects to different webpages based on the submitfield pressed within the form
                if 'newticket' in request.form:
                    return redirect(url_for('newticket', users=users))
                if 'viewticket' in request.form:
                    return redirect(url_for('viewticket', users=users))
                if 'viewaccount' in request.form:
                    return redirect(url_for('viewuser', users=users))
                if 'logout' in request.form:
                    active_user = False
                    return redirect('/')
            return render_template('menu.html', title=title, form=form,
                                   formheader=formheader, formtext=formtext)
        else: # if the user input is incorrect it will redirect to the homepage
            return redirect('/')
    else: # if the user input is incorrect it will redirect to the homepage
        return redirect('/')


@app.route('/admin/<string:users>', methods=['GET', 'POST'])
def admin(users):
    global active_user, active_admin # allows the app route to have access to the active variables
    # text that will be added to the html templates using bootstrap for efficiency, allowing templates to be reused
    title = "Crystal: Admin"
    formheader = "Welcome ".join([users]) + " to your Crystal account"
    formtext = "Warning: Misuse of these systems can lead to legal consequences"
    form = Admin()
    # search queries that validate the existence of a user account and whether that account is an admin or standard user account
    account_search = User.query.filter(User.username.in_([users])).first()
    if account_search is not None:
        if active_admin == True:
            if form.validate_on_submit():  # redirects to different webpages based on the submitfield pressed within the form
                if 'viewticket' in request.form:
                    return redirect(url_for('viewticket', users=users))
                if 'viewusers' in request.form:
                    return redirect(url_for('viewuser', users=users))
                if 'newteams' in request.form:
                    return redirect(url_for('newteam', users=users))
                if 'viewteams' in request.form:
                    return redirect(url_for('viewteams', users=users))
                if 'logout' in request.form:
                    active_admin = False
                    return redirect('/')
            return render_template('menu.html', title=title, form=form,
                                   formheader=formheader, formtext=formtext)
        else: # if the user input is incorrect it will redirect to the homepage
            return redirect('/')
    else: # if the user input is incorrect it will redirect to the homepage
        return redirect('/')

# creates application instance for '/user/username/new_ticket'
@app.route('/user/<string:users>/new_ticket', methods=['GET', 'POST'])
def newticket(users):
    global active_user, active_admin  # allows the app route to have access to the active variables
    title = "Crystal: New Ticket"
    formheader = "Crystal ticket template creator"
    formtext = "Ensure that the data inputted is correct"
    form = NewTicket()
    # search queries that validate the existence of a user account and whether that account is an admin or standard user account
    account_search = User.query.filter(User.username.in_([users])).first()
    if account_search is not None:
        if active_user == True:
            if form.validate_on_submit():
                new_ticket = Ticket(type=form.type.data, title=form.title.data,
                                    desc=form.desc.data, userkey=users, verif=0)
                db.session.add(new_ticket)
                db.session.commit()
                return redirect(url_for('user', users=users))
            return render_template('menu.html', form=form, title=title,
                                   formheader=formheader, formtext=formtext)
        else: # if the user input is incorrect it will redirect to the homepage
            return redirect('/')
    else:  # else function that prevents non-logged in people from accessing the site through inputting random urls
        return redirect(url_for('main'))

# creates application instance for '/tickets/username' where tickets assigned to each user will be shown and admin accounts can see all accounts relating to each user
@app.route('/tickets/<string:users>')
def viewticket(users):
    global active_user, active_admin  # allows the app route to have access to the active variables
    # variables to check whether the user is a standard user or admin
    tick = False
    # search queries that validate the existence of a user account and whether that account is an admin or standard user account
    account_query = User.query.filter(User.username.in_([users])).first()
    if account_query.admin == 1 & active_admin == True:
        tick = True
        title = "Crystal: Admin Ticket View"
        formheader = "View Tickets: Admin"
        formtext = "Ensure to manage all tickets correctly"
        tickets = Ticket.query.filter(Ticket.id).all()  # database query to show all tickets in the database
        return render_template('ticketviewer.html', tickets=tickets, users=users, title=title,
                               formheader=formheader, formtext=formtext, tick=tick)
    if account_query.admin == 0 & active_user == True:
        tick = True
        title = "Crystal: View Tickets"
        formheader = "View Tickets"
        formtext = "Ensure that the data inputted is correct"
        tickets = Ticket.query.filter(Ticket.userkey == users)  # database query to show user's current tickets
        return render_template('ticketviewer.html', tickets=tickets, users=users, title=title,
                               formheader=formheader, formtext=formtext, tick=tick)
    else:  # else function that prevents non-logged in people from accessing the site through inputting random urls
        return redirect(url_for('main'))

# creates the application instance for '/tickets/user/ticketid' where admins and users can view all their respective tickets
@app.route('/tickets/<string:users>/<string:id>', methods=['GET', 'POST'])
def viewtickets(users, id):
    global active_user, active_admin  # allows the app route to have access to the active variables
    use = False
    aduse = False
    form = TicketApproval()
    form1 = TicketDeletion()
    # validation to check for the user's admin access as well as the current ticket that was selected within the viewticket section
    account_query = User.query.filter(User.username.in_([users])).first()
    idticket = Ticket.query.filter(Ticket.id.in_([id])).first()
    title = ': Ticket No. ' + id + ", " + idticket.title
    if account_query.admin == 1 & active_admin == True:
        aduse = True
        formheader = "View Tickets: Admin"
        formtext = "Ensure to manage all tickets correctly"
        if form.validate_on_submit(): # flaskform for the approval form
            if 'approve' in request.form:
                idticket.allowed = True
                db.session.add(idticket)
                db.session.commit()
                return redirect(url_for('viewtickets', users=users, id=id))  # reroutes to main menu once ticket is updated
        if form1.validate_on_submit(): # flaskform for the deletion form
            if 'delete' in request.form:
                db.session.delete(idticket)
                db.session.commit()
                return redirect(url_for('viewtickets', users=users, id=id))  # reroutes to main menu once ticket is deleted
        return render_template('ticketviewer.html', idticket=idticket, title=title,
                               form=form, form1=form1, formheader=formheader, formtext=formtext, aduse=aduse)
    if account_query.admin == 0 & active_user == True:
        use = True
        formheader = "View Tickets: Admin"
        formtext = "Ensure to manage all tickets correctly"
        if form1.validate_on_submit(): # flaskform for the deletion form
            if 'delete' in request.form:
                db.session.delete(idticket)
                db.session.commit()
                return redirect(url_for('viewtickets', users=users, id=id))  # reroutes to main menu once ticket is deleted
        return render_template('ticketviewer.html', idticket=idticket, title=title,
                               form1=form1, formheader=formheader, formtext=formtext, use=use)

    # creates application instance for '/admin/<string:users>/viewuser' where admins will be able to view all user accounts
@app.route('/account/<string:users>/viewuser', methods=['GET', 'POST'])
def viewuser(users):
    global active_user, active_admin  # allows the app route to have access to the active variables
    aduse = False
    title = 'Crystal: View User'
    account_query = User.query.filter(User.username.in_([users])).first()
    adused = User.query.filter(User.admin == 0).all()
    if account_query.admin == 1 & active_admin == True:
        formheader = "View Accounts: Admin"
        formtext = "Manage User accounts below"
        aduse = True
        return render_template('userviewer.html', adused=adused, users=users, title=title,
                                   formheader=formheader, formtext=formtext, aduse=aduse)
    elif account_query.admin == 0 & active_user == True:
        return redirect(url_for('userview', users=users, id=account_query.id))
    else:  # else function that prevents non-logged in people from accessing the site through inputting random urls
        return redirect(url_for('main'))

# creates an application instance for the account/users/viewuser/id pathway
@app.route('/account/<string:users>/viewuser/<string:id>', methods=['GET', 'POST'])
def userview(users, id):
    global active_user, active_admin  # allows the app route to have access to the active variables
    aduse = False
    form = EditAccount()
    form1 = DeleteAccount()
    used = User.query.filter_by(id=id, admin=False).first()
    new_username = User.query.filter_by(username=form.username.data).first()
    account_query = User.query.filter(User.username.in_([users])).first()
    username = used.username
    title = 'Crystal Account: ' + username
    formheader = "Crystal Account Edit: "
    formtext = "Manage User accounts below"
    if used:
        if active_admin == True or active_user == True:
            if form.validate_on_submit():  # validation of account edit
                if new_username is None:  # updates the username against the database to ensure no values are committed while overlapping
                    used.username = form.username.data
                    used.password = form.password.data
                    used.forename = form.forename.data
                    used.surname = form.surname.data
                    db.session.add(used)
                    db.session.commit()
                    if account_query.admin == 1:  # send back to viewuser page to update other accounts
                        return redirect(url_for('viewuser', users=users))
                    elif account_query.admin == 0:  # send back to main menu for the user to access their account with new login credentials
                        active_admin = False
                        return redirect('/')
                else:
                    return redirect(url_for('userview', users=users, id=id))
            if form1.validate_on_submit():  # validation of account deletion
                if 'delete' in request.form:
                    delete_user = User.query.filter_by(id=id,
                                                       admin=False).first()  # ensures the selected user cannot be an admin account
                    db.session.delete(delete_user)  # deletes the selected user
                    db.session.commit()
                    delete_tickets = Ticket.query.filter(Ticket.userkey == username).all()
                    for x in delete_tickets:
                        # deletes each ticket in the delete_tickets query so no unlinked tickets are left in db
                        db.session.delete(x)
                        db.session.commit()
                    if account_query.admin == 1:  # send back to viewuser page to update other accounts
                        return redirect(url_for('viewuser', users=users))
                    elif account_query.admin == 0:  # send user back to homepage as the account and respective tickets have been deleted
                        active_user = False
                        return redirect('/')
            return render_template('userviewer.html', used=used, title=title, form=form, form1=form1,
                                   formheader=formheader, formtext=formtext, aduse=aduse)
        else: # security to ensure those without an account can't impact the website
            return('/')
    else: # security to ensure those without an account can't impact the website
        return('/')

# creates an application instance for the admin/user/newteam pathway
@app.route('/admin/<string:users>/newteam', methods=['GET', 'POST'])
def newteam(users):
    global active_user, active_admin  # allows the app route to have access to the active variables
    # text that will be added to the html templates using bootstrap for efficiency, allowing templates to be reused
    title = "Crystal: Team Creator"
    formheader = "Crystal Team Creator"
    formtext = "Warning: Misuse of these systems can lead to legal consequences"
    form = Teams()
    new_team = Team.query.filter_by(name=form.name.data).first()
    account_query = User.query.filter(User.username.in_([users])).first()
    if account_query.admin == 1:
        if form.validate_on_submit():
            if new_team is None:
                a_team = Team(name=form.name.data, type=form.type.data,
                              size=form.size.data, teamkey=account_query.username)
                db.session.add(a_team)
                db.session.commit()
                return redirect(url_for('admin', users=users))
            else:
                return redirect(url_for('admin', users=users))
        return render_template('menu.html', title=title, form=form,
                               formheader=formheader, formtext=formtext)
    else:
        return redirect('/')

    # creates application instance for '/admin/<string:users>/viewuser' where admins will be able to view all user accounts
@app.route('/admin/<string:users>/viewteams', methods=['GET', 'POST'])
def viewteams(users):
    global active_user, active_admin  # allows the app route to have access to the active variables
    title = 'Crystal: View Teams'
    account_query = User.query.filter(User.username.in_([users])).first()
    current_team = Team.query.filter(Team.teamkey == users)
    if account_query.admin == 1 & active_admin == True:
        return render_template('teamviewer.html', users=users, current_team=current_team, title=title)
    else:  # else function that prevents non-logged in people from accessing the site through inputting random urls
        return redirect(url_for('main'))

# creates an application instance for the account/users/viewuser/id pathway
@app.route('/admin/<string:users>/viewteams/<string:id>', methods=['GET', 'POST'])
def teamview(users, id):
    global active_user, active_admin  # allows the app route to have access to the active variables
    form = EditTeam()
    form1 = DeleteAccount()
    teams = Team.query.filter_by(id=id).first()
    new_teams = Team.query.filter_by(name=form.name.data).first()
    account_query = User.query.filter(User.username.in_([users])).first()
    teamtitle = teams.name
    title = 'Crystal Team: ' + teamtitle
    formheader = "Crystal Team Edit: "
    formtext = "Manage Crystal teams below"
    if account_query.admin == 1 & active_admin == True:
        if form.validate_on_submit():  # validation of account edit
            if new_teams is None:
                new_teams.name = form.name.data
                new_teams.type = form.type.data
                new_teams.size = form.size.data
                db.session.add(new_teams)
                db.session.commit()
                return redirect(url_for('admin', users=users))
            else:
                return redirect(url_for('admin', users=users))
        if form1.validate_on_submit():  # validation of account deletion
            if 'delete' in request.form:
                delete_team = Team.query.filter_by(id=id).first()
                db.session.delete(delete_team)  # deletes the selected team
                db.session.commit()
                return redirect(url_for('admin', users=users))
        return render_template('ateam.html', title=title, form=form, form1=form1,
                               formheader=formheader, formtext=formtext, teams=teams)
    else: # security to ensure those without an account can't impact the website
        return('/')

# command that runs the application in a debug mode
if __name__ == '__main__':
    app.run(debug=Debug)