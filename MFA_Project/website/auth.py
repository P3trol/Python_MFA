from flask import Blueprint, render_template, request, flash, redirect, url_for # Import flask dependencies 
from .models import User # Import login database table
from werkzeug.security import generate_password_hash, check_password_hash # Import password hashing
from . import db # Import db object from main app module
from flask_login import login_user,login_required, logout_user, current_user
import pyotp # Import pyotp for 2FA
from sqlalchemy.sql import text # for raw sql queries
from captcha.image import ImageCaptcha # Import captcha
import random # Import random  




auth = Blueprint('auth',__name__) # Blueprint is a way to organize a group of related views and other code.
secret = pyotp.random_base32() # Generate random secret for 2FA





@auth.route('/login' , methods=['GET', 'POST']) # Define route for login page
def login():# Define login function
    if request.method == 'POST': # If form is submitted
        username = request.form.get('username')# Get username from form
        password = request.form.get('password')# Get password from form
        otp_secret = request.form.get('otp_secret')# Get otp_secret from form
        otp = int(request.form.get("otp"))# Get otp from form
        captcha = (request.form.get("captcha"))# Get capcha from form

        allowed_chars = "abcdefghijklmnopqrstuvwxyz123456789" # Define allowed characters for captcha
        size = 6 # Define size of captcha

        def random_string_generator(allowed_chars, size):   # Define random string generator function
         return ''.join(random.choice(allowed_chars) for x in range(size)) # Return random string




        image = ImageCaptcha(width = 280, height = 90) # Define image size
        captcha_text = random_string_generator(allowed_chars, size) # Generate random string for captcha
        data = image.generate(captcha_text) # Generate captcha
        image.write(captcha_text, 'website/static/images/captcha.png') # Write captcha to file
        

        

       
        user = User.query.filter_by(username=username).first()# Get user from database
        psecret = str(db.select(text(user.otp_secret, otp_secret))) #secret pulled from database 
        secret = psecret[7:len(psecret)] # trims "SELECT " from pstring


        if user:
            if check_password_hash(user.password, password) and pyotp.TOTP(secret).verify(otp) and captcha == captcha_text: # Check if password is correct and 2FA is correct and captcha is correct
                flash('Logged in successfully!', category='success')# If password is correct, flash success message
                login_user(user, remember=True) # Log user in
                
                return redirect(url_for('views.home')) # Redirect to home page
            else:
                flash('Incorrect password/OTP/captcha, try again.', category='error')# If password is incorrect/OTP/capcha, flash error message
        else:
            flash('username does not exist.', category='error')# If username does not exist, flash error message

    return render_template("login.html", user = current_user )# If form is not submitted, render login page


@auth.route('/logout')# Define route for logout page
@login_required# Require user to be logged in
def logout():# Define logout function
    logout_user()# Log user out
    return redirect(url_for('auth.login'))# Redirect to login page


@auth.route('/register', methods=['GET', 'POST'])# Define route for register page
def register():# Define register function
   if request.method == "POST":# If form is submitted
        username = request.form.get('username')# Get username from form
        fname = request.form.get('fname')# Get fname from form
        lname = request.form.get('lname')# Get lname from form
        email = request.form.get('email')# Get email from form
        pass1 = request.form.get('pass1')# Get pass1 from form
        pass2 = request.form.get('pass2')# Get pass2 from form
        otp = int(request.form.get("otp"))# Get otp from form
        otp_secret = request.form.get("secret")# Get otp_secret from form
        

        if User.query.filter_by(username = username).first(): # Check if username already exists
            flash("This username is already taken, Please try again", category = 'error')  

        elif User.query.filter_by(email = email).first(): # Check if email already exists
            flash("This Email is already taken, Please try again", category = 'error') 
        
        elif not pyotp.TOTP(secret).verify(otp): # Check if 2FA is correct
            flash("The TOTP 2FA token is invalid", category = 'error')

        elif len(username)>10: # Check if username is too long
            flash("Username must be under 10 characters", category = 'error')  

        elif len(pass1) < 7:    # Check if password is too short
            flash('Password must be at least 7 characters.', category='error')
        
        elif pass1 != pass2:   # Check if passwords match
            flash("Passwords didn't match!", category = 'error')  
    
        elif not username.isalnum(): # Check if username is alphanumeric
            flash("The Username must only contain letters and numbers, Please try again", category = 'error')  
        
        else:
            new_user = User(username = username, first_name = fname, last_name = lname, email = email, password = generate_password_hash(pass1, method='sha256'), otp_secret = otp_secret) # Create new user
            db.session.add(new_user) # Add new user to database
            db.session.commit() # Commit changes to database
            pyotp.TOTP(secret).verify(otp) # Verify 2FA
            login_user(new_user, remember=True) # Log user in
            flash( "Account has been created.", category = 'success') # Flash success message
            return redirect(url_for('views.home')) # Redirect to home page
        
        
    
   return render_template("register.html", user= current_user, secret=secret ) # If form is not submitted, render register page
