"""
Database Models - Define the structure of our database tables

Each class represents a table in the database.
SQLAlchemy ORM (Object-Relational Mapping) converts these Python classes
to SQL tables automatically.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Import db from app (will be initialized in app.py)
# This import happens after db is created, so it's safe
from app import db

# UserMixin provides default implementations for Flask-Login
class User(UserMixin, db.Model):
    """
    User Model - Stores user account information
    
    Attributes:
        id: Primary key (auto-generated)
        username: Unique username
        email: Unique email address
        password_hash: Encrypted password (never store plain passwords!)
        bookings: Relationship to bookings (one user can have many bookings)
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship: One user can have many bookings
    bookings = db.relationship('Booking', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and store password securely"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against stored hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Movie(db.Model):
    """
    Movie Model - Stores movie information
    
    Attributes:
        id: Primary key
        title: Movie title
        description: Movie description
        duration: Movie duration in minutes
        genre: Movie genre
        rating: Movie rating (e.g., PG, PG-13, R)
        poster_url: URL to movie poster image
        shows: Relationship to shows (one movie can have many shows)
    """
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)  # Duration in minutes
    genre = db.Column(db.String(100))
    rating = db.Column(db.String(10))
    poster_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship: One movie can have many shows
    shows = db.relationship('Show', backref='movie', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Movie {self.title}>'


class Show(db.Model):
    """
    Show Model - Stores show timings for movies
    
    Attributes:
        id: Primary key
        movie_id: Foreign key to Movie
        show_time: Date and time of the show
        screen_number: Screen/auditorium number
        total_seats: Total number of seats
        price: Ticket price
        bookings: Relationship to bookings
        seats: Relationship to seats
    """
    __tablename__ = 'shows'
    
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    show_time = db.Column(db.DateTime, nullable=False)
    screen_number = db.Column(db.Integer, nullable=False)
    total_seats = db.Column(db.Integer, default=50)  # Default 50 seats
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='show', lazy=True)
    seats = db.relationship('Seat', backref='show', lazy=True, cascade='all, delete-orphan')
    
    def get_available_seats(self):
        """Get count of available seats for this show"""
        booked_seats = db.session.query(Seat).join(Booking).filter(
            Seat.show_id == self.id,
            Booking.status == 'confirmed'
        ).count()
        return self.total_seats - booked_seats
    
    def __repr__(self):
        return f'<Show {self.id} - {self.show_time}>'


class Seat(db.Model):
    """
    Seat Model - Stores individual seat information
    
    Attributes:
        id: Primary key
        show_id: Foreign key to Show
        seat_number: Seat identifier (e.g., "A1", "B5")
        row: Row letter/number
        column: Column number
        booking_id: Foreign key to Booking (if booked)
    """
    __tablename__ = 'seats'
    
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)  # e.g., "A1", "B5"
    row = db.Column(db.String(5), nullable=False)  # Row letter
    column = db.Column(db.Integer, nullable=False)  # Column number
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=True)
    
    def is_available(self):
        """Check if seat is available"""
        return self.booking_id is None
    
    def __repr__(self):
        return f'<Seat {self.seat_number}>'


class Booking(db.Model):
    """
    Booking Model - Stores booking information
    
    Attributes:
        id: Primary key
        user_id: Foreign key to User
        show_id: Foreign key to Show
        booking_date: When the booking was made
        total_amount: Total price of the booking
        status: Booking status (pending, confirmed, cancelled)
        seats: Relationship to seats
    """
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='confirmed')  # pending, confirmed, cancelled
    
    # Relationship: One booking can have many seats
    seats = db.relationship('Seat', backref='booking', lazy=True)
    
    def __repr__(self):
        return f'<Booking {self.id} - {self.status}>'

