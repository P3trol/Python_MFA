from flask import Flask # Import Flask
from flask_sqlalchemy import SQLAlchemy # Import SQLAlchemy
from os import path # Import path
from flask_login import LoginManager # Import LoginManager



db = SQLAlchemy() # Create database
DB_name = "Users.db" # Database name

def create_app(): # Create app function
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 't3y!q@wu9sw2r+uva2pj@y$4n25mt+39fw2-9)h-9j&^bs5t(' # Secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_name}'  # Database URI
    db.init_app(app) # Initialize database

    login_manager = LoginManager() # Create login manager
    login_manager.login_view = 'auth.login' # Set login view
    login_manager.init_app(app) # Initialize login manager


    from .views import views # Import views
    from .auth import auth  # Import auth

    app.register_blueprint(views, url_prefix='/') # Register views blueprint
    app.register_blueprint(auth, url_prefix='/') # Register auth blueprint

    from .models import User # Import User class

    create_database(app) # Create database

    @login_manager.user_loader # Create user loader
    def load_user(id): # Load user function
        return User.query.get(int(id)) # Return user

    return app # Return app

def create_database(app): # Create database function
    if not path.exists('website/' + DB_name):   # Check if database exists
        with app.app_context():     # Create app context
            db.create_all() # Create database
            print('Created Database!') # Print database created
    

  

