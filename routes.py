"""
Routes - Define all URL endpoints and their functionality

This file contains all the routes (URLs) that users can visit.
Each function handles a specific page or action.
"""

from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, Movie, Show, Booking, Seat
from datetime import datetime, timedelta
from sqlalchemy import and_

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    """Home page - Display all movies"""
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    User Registration Page
    
    GET: Show registration form
    POST: Process registration form and create new user
    """
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required!', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)  # Hash the password
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    User Login Page
    
    GET: Show login form
    POST: Process login and create user session
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password!', 'error')
            return render_template('login.html')
        
        # Find user in database
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password is correct
        if user and user.check_password(password):
            login_user(user)  # Create session for user
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect to page user was trying to access, or home
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required  # User must be logged in to logout
def logout():
    """Logout user and end session"""
    logout_user()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('index'))


# ==================== MOVIE ROUTES ====================

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    """Display movie details and available shows"""
    movie = Movie.query.get_or_404(movie_id)
    
    # Get all shows for this movie that are in the future
    shows = Show.query.filter(
        and_(
            Show.movie_id == movie_id,
            Show.show_time > datetime.now()
        )
    ).order_by(Show.show_time).all()
    
    return render_template('movie_detail.html', movie=movie, shows=shows)


@app.route('/show/<int:show_id>')
@login_required
def show_seats(show_id):
    """
    Seat Selection Page
    
    Display available seats for a show and allow user to select seats
    """
    show = Show.query.get_or_404(show_id)
    movie = show.movie
    
    # Get all seats for this show
    seats = Seat.query.filter_by(show_id=show_id).all()
    
    # If no seats exist, create them
    if not seats:
        seats = create_seats_for_show(show)
    
    # Organize seats by row for display
    seats_by_row = {}
    for seat in seats:
        if seat.row not in seats_by_row:
            seats_by_row[seat.row] = []
        seats_by_row[seat.row].append(seat)
    
    # Get booked seat IDs
    booked_seat_ids = [seat.id for seat in seats if not seat.is_available()]
    
    return render_template('show_seats.html', 
                         show=show, 
                         movie=movie, 
                         seats_by_row=seats_by_row,
                         booked_seat_ids=booked_seat_ids)


def create_seats_for_show(show):
    """
    Helper function to create seats for a show
    
    Creates seats in a grid pattern (e.g., A1-A10, B1-B10, etc.)
    """
    seats = []
    rows = ['A', 'B', 'C', 'D', 'E']  # 5 rows
    seats_per_row = show.total_seats // len(rows)  # Distribute seats across rows
    
    for row in rows:
        for col in range(1, seats_per_row + 1):
            seat = Seat(
                show_id=show.id,
                seat_number=f"{row}{col}",
                row=row,
                column=col
            )
            seats.append(seat)
            db.session.add(seat)
    
    db.session.commit()
    return seats


@app.route('/book', methods=['POST'])
@login_required
def book_tickets():
    """
    Process ticket booking
    
    Receives selected seat IDs and creates a booking
    """
    data = request.get_json()
    show_id = data.get('show_id')
    seat_ids = data.get('seat_ids', [])
    
    if not show_id or not seat_ids:
        return jsonify({'success': False, 'message': 'Invalid booking data'}), 400
    
    show = Show.query.get_or_404(show_id)
    
    # Check if seats are available
    seats = Seat.query.filter(
        and_(
            Seat.show_id == show_id,
            Seat.id.in_(seat_ids)
        )
    ).all()
    
    # Verify all seats are available
    for seat in seats:
        if not seat.is_available():
            return jsonify({'success': False, 'message': f'Seat {seat.seat_number} is already booked!'}), 400
    
    # Calculate total amount
    total_amount = len(seat_ids) * show.price
    
    # Create booking
    booking = Booking(
        user_id=current_user.id,
        show_id=show_id,
        total_amount=total_amount,
        status='confirmed'
    )
    db.session.add(booking)
    db.session.flush()  # Get booking ID
    
    # Assign seats to booking
    for seat in seats:
        seat.booking_id = booking.id
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Booking confirmed!',
        'booking_id': booking.id
    })


@app.route('/bookings')
@login_required
def my_bookings():
    """Display all bookings for the current user"""
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(
        Booking.booking_date.desc()
    ).all()
    
    return render_template('my_bookings.html', bookings=bookings)


@app.route('/booking/<int:booking_id>')
@login_required
def booking_detail(booking_id):
    """Display details of a specific booking"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Verify booking belongs to current user
    if booking.user_id != current_user.id:
        flash('You do not have permission to view this booking!', 'error')
        return redirect(url_for('my_bookings'))
    
    return render_template('booking_detail.html', booking=booking)


# ==================== ADMIN ROUTES ====================

@app.route('/admin')
@login_required
def admin_dashboard():
    """
    Admin Dashboard
    
    Simple admin panel to manage movies and shows
    Note: In production, add proper admin role checking!
    """
    movies = Movie.query.all()
    shows = Show.query.order_by(Show.show_time.desc()).limit(10).all()
    bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                         movies=movies, 
                         shows=shows, 
                         bookings=bookings)


@app.route('/admin/movie/add', methods=['GET', 'POST'])
@login_required
def add_movie():
    """Add a new movie"""
    if request.method == 'POST':
        movie = Movie(
            title=request.form.get('title'),
            description=request.form.get('description'),
            duration=int(request.form.get('duration', 0)),
            genre=request.form.get('genre'),
            rating=request.form.get('rating'),
            poster_url=request.form.get('poster_url')
        )
        db.session.add(movie)
        db.session.commit()
        flash('Movie added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/add_movie.html')


@app.route('/admin/show/add', methods=['GET', 'POST'])
@login_required
def add_show():
    """Add a new show for a movie"""
    if request.method == 'POST':
        show = Show(
            movie_id=int(request.form.get('movie_id')),
            show_time=datetime.strptime(request.form.get('show_time'), '%Y-%m-%dT%H:%M'),
            screen_number=int(request.form.get('screen_number')),
            total_seats=int(request.form.get('total_seats', 50)),
            price=float(request.form.get('price'))
        )
        db.session.add(show)
        db.session.commit()
        flash('Show added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    movies = Movie.query.all()
    return render_template('admin/add_show.html', movies=movies)

