from flask import Flask, Blueprint, render_template # Import Blueprint and render_template from flask
from flask_login import  login_required, current_user # Import login_required and current_user from flask_login

views = Blueprint('views',__name__)     # Blueprint is a way to organize a group of related views and other code. Rather than registering views and other code directly with an application, they are registered with a blueprint. Then the blueprint is registered with the application when it is available in the factory function.

@views.route('/') # Define route for home page
@login_required # Require user to be logged in

def home(): # Define home function
    
    return render_template("home.html", user = current_user) # Render home page