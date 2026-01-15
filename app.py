"""
Movie Ticket Booking Platform - Main Application File

This is the entry point of our application. It initializes Flask,
sets up the database, and registers all routes.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialize Flask application
app = Flask(__name__)

# Configuration
# SECRET_KEY is used for session management and security
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# Database configuration
# SQLite database file will be created in the project directory
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'movie_booking.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize Flask-Login for user session management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if not authenticated
login_manager.login_message = 'Please log in to access this page.'

# Import models (must be after db initialization)
from models import User, Movie, Show, Booking, Seat

# Import routes (must be after app initialization)
from routes import *

# User loader function for Flask-Login
# This tells Flask-Login how to find a user by their ID
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login session management"""
    return User.query.get(int(user_id))

# Create database tables
# This creates all tables defined in models.py
def create_tables():
    """Create all database tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    # Create tables when running the app
    create_tables()
    
    # Run the Flask development server
    # debug=True enables auto-reload on code changes (only for development!)
    app.run(debug=True, host='0.0.0.0', port=5000)

