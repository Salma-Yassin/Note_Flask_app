
from flask import Blueprint , render_template , request , flash , redirect ,  url_for
# What if the user entered a wrong pass or didn’t add in an email? You have to have a warning msg  
from .models import User 
from werkzeug.security import generate_password_hash , check_password_hash
from . import db ## this means import db from __init__.py 
from flask_login import login_user , login_required , logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login',methods = ['GET','POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!' , category = 'success')
                login_user(user , remember = True)
                return redirect(url_for('views.home')) # get the url for that function or route 
            else:
                flash('Incorrect password,try again.' , category = 'error')
        else:
            flash('Email does not exist' , category = 'error')

    return render_template("login.html" , user = current_user)

@auth.route('/logout')
@login_required # makes sure that the user is logged out only if they are logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up' , methods = [ 'GET' , 'POST' ])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # show messages to the user depending on their inputs 

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category = 'error')
        elif len(firstName) < 2:
            flash()
        elif password1 != password2:
            flash('First name must be greater tha 1 characters.' , category = 'error')
        elif len(password1) < 7 :
            flash('Passwords don\'t match.' , category = 'error')
        else:
            # Adding new user to the database
            new_user = User(email = email , first_name = firstName , password = generate_password_hash(password1 , method = 'sha256')) # name of the hashing algorithm 
            db.session.add(new_user)
            db.session.commit()
            login_user( new_user , remember = True)
            flash('Account created !' , category = 'success' )
            return redirect(url_for('views.home'))

    return render_template("sign_up.html" , user = current_user)