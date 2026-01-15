# 🎬 Movie Ticket Booking Platform

A complete web application for booking movie tickets, built with **Python Flask** and **SQLite Database**. This project is designed for beginners to learn web development, database management, and Python programming.

## 📚 What You'll Learn

- **Flask Framework**: Building web applications with Python
- **Database Management**: Using SQLite and SQLAlchemy ORM
- **User Authentication**: Login, registration, and session management
- **Frontend Development**: HTML, CSS, and JavaScript
- **RESTful Routes**: Creating and handling different URL endpoints
- **Database Relationships**: One-to-many relationships between tables

## 🎯 Features

- ✅ User Registration and Login
- ✅ Browse Movies
- ✅ View Movie Details and Show Times
- ✅ Interactive Seat Selection
- ✅ Ticket Booking System
- ✅ View Booking History
- ✅ Admin Panel (Add Movies and Shows)
- ✅ Responsive Design

## 📋 Prerequisites

Before you start, make sure you have the following installed:

1. **Python 3.7 or higher**
   - Check if installed: Open terminal/command prompt and type `python --version`
   - Download from: https://www.python.org/downloads/

2. **pip** (Python package installer)
   - Usually comes with Python
   - Check if installed: `pip --version`

3. **A code editor** (optional but recommended)
   - VS Code: https://code.visualstudio.com/
   - PyCharm: https://www.jetbrains.com/pycharm/

## 🚀 Installation & Setup

### Step 1: Navigate to Project Directory

Open your terminal/command prompt and navigate to the project folder:

```bash
cd "D:\Movie Ticket booking Platform"
```

### Step 2: Create a Virtual Environment (Recommended)

A virtual environment keeps your project dependencies separate from other Python projects.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt.

### Step 3: Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (Web framework)
- Flask-SQLAlchemy (Database ORM)
- Flask-Login (User session management)
- Werkzeug (Password hashing utilities)

### Step 4: Run the Application

Start the Flask development server:

```bash
python app.py
```

You should see output like:
```
Database tables created successfully!
 * Running on http://127.0.0.1:5000
```

### Step 5: Open in Browser

Open your web browser and go to:
```
http://localhost:5000
```

or

```
http://127.0.0.1:5000
```

## 📁 Project Structure Explained

```
Movie Ticket booking Platform/
│
├── app.py                 # Main application file - starts Flask server
├── models.py              # Database models (tables structure)
├── routes.py              # All URL routes and page handlers
├── requirements.txt       # Python packages needed
├── movie_booking.db       # SQLite database (created automatically)
│
├── templates/             # HTML templates (web pages)
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Home page (movie listings)
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── movie_detail.html  # Movie details and shows
│   ├── show_seats.html    # Seat selection page
│   ├── my_bookings.html   # User's booking history
│   ├── booking_detail.html # Individual booking details
│   └── admin/             # Admin panel templates
│       ├── dashboard.html
│       ├── add_movie.html
│       └── add_show.html
│
└── static/                # Static files (CSS, JavaScript, images)
    ├── css/
    │   └── style.css      # All styling
    └── js/
        └── main.js        # JavaScript functions
```

## 🗄️ Database Structure

The application uses **5 main tables**:

1. **users** - Stores user account information
   - id, username, email, password_hash, created_at

2. **movies** - Stores movie information
   - id, title, description, duration, genre, rating, poster_url

3. **shows** - Stores show timings for movies
   - id, movie_id, show_time, screen_number, total_seats, price

4. **seats** - Stores individual seat information
   - id, show_id, seat_number, row, column, booking_id

5. **bookings** - Stores booking information
   - id, user_id, show_id, booking_date, total_amount, status

## 🎮 How to Use the Application

### For Regular Users:

1. **Register an Account**
   - Click "Register" in the navigation
   - Fill in username, email, and password
   - Click "Register"

2. **Login**
   - Click "Login" in the navigation
   - Enter your username and password

3. **Browse Movies**
   - Home page shows all available movies
   - Click "View Shows" on any movie

4. **Book Tickets**
   - Select a show time
   - Click "Select Seats"
   - Choose your seats (click on available seats)
   - Click "Book Tickets"
   - View your booking in "My Bookings"

### For Admin:

1. **Add a Movie**
   - Login to your account
   - Go to "Admin" in navigation
   - Click "Add Movie"
   - Fill in movie details
   - Submit

2. **Add a Show**
   - Go to Admin Dashboard
   - Click "Add Show"
   - Select a movie
   - Set date, time, screen number, seats, and price
   - Submit

## 🔧 Adding Sample Data

To quickly test the application, you can add sample data:

1. **Option 1: Use Admin Panel**
   - Register and login
   - Use Admin panel to add movies and shows

2. **Option 2: Use Python Script**
   - Run `python add_sample_data.py` (if you create this script)
   - This will add sample movies and shows automatically

## 📖 Understanding the Code

### How Authentication Works:

1. **Registration** (`routes.py` - `register()` function):
   - User submits form with username, email, password
   - Password is hashed (encrypted) using `generate_password_hash()`
   - User data is saved to database
   - User is redirected to login

2. **Login** (`routes.py` - `login()` function):
   - User submits username and password
   - System finds user in database
   - Password is verified using `check_password()`
   - If correct, `login_user()` creates a session
   - User is redirected to home page

3. **Session Management**:
   - Flask-Login manages user sessions
   - `@login_required` decorator protects routes
   - `current_user` gives access to logged-in user

### How Booking Works:

1. **Seat Selection** (`show_seats.html`):
   - JavaScript handles seat clicking
   - Selected seats are stored in a Set
   - Total price is calculated dynamically

2. **Booking Creation** (`routes.py` - `book_tickets()` function):
   - Receives selected seat IDs via AJAX
   - Creates a Booking record
   - Assigns seats to the booking
   - Updates seat availability

### Database Relationships:

- **One User** → **Many Bookings** (One-to-Many)
- **One Movie** → **Many Shows** (One-to-Many)
- **One Show** → **Many Seats** (One-to-Many)
- **One Booking** → **Many Seats** (One-to-Many)

## 🐛 Troubleshooting

### Problem: "Module not found" error
**Solution:** Make sure you activated virtual environment and installed requirements:
```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Problem: "Port already in use"
**Solution:** Another application is using port 5000. Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Problem: Database errors
**Solution:** Delete `movie_booking.db` file and restart the application. It will recreate the database.

### Problem: Can't see movies
**Solution:** Add movies through Admin panel or create sample data.

## 🔒 Security Notes

⚠️ **Important for Production:**

1. **Change SECRET_KEY** in `app.py`:
   ```python
   app.config['SECRET_KEY'] = 'your-very-secret-key-here'
   ```

2. **Use Environment Variables** for sensitive data:
   ```python
   import os
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
   ```

3. **Add Admin Role Checking** - Currently any logged-in user can access admin panel. Add role-based access control.

4. **Use PostgreSQL** instead of SQLite for production.

5. **Add CSRF Protection** using Flask-WTF.

## 🎓 Learning Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **HTML/CSS Tutorial**: https://www.w3schools.com/
- **JavaScript Tutorial**: https://www.w3schools.com/js/

## 🚀 Next Steps to Enhance

1. **Payment Integration**: Add payment gateway (Stripe, PayPal)
2. **Email Notifications**: Send booking confirmation emails
3. **Search & Filter**: Add search for movies, filter by genre
4. **User Profile**: Add user profile page with edit functionality
5. **Reviews & Ratings**: Allow users to rate movies
6. **Cancel Booking**: Add booking cancellation feature
7. **Admin Authentication**: Separate admin login
8. **Image Upload**: Allow uploading movie posters

## 📝 License

This project is for educational purposes. Feel free to use and modify as needed.

## 💡 Tips for Beginners

1. **Read the code comments** - They explain what each part does
2. **Experiment** - Try changing values and see what happens
3. **Use print() statements** - Debug by printing variables
4. **Check browser console** - See JavaScript errors (F12)
5. **Read error messages** - They tell you what went wrong
6. **Start small** - Understand one feature at a time

## 🤝 Need Help?

If you encounter any issues:
1. Check the error message carefully
2. Review the code comments
3. Check if all dependencies are installed
4. Make sure database is created (run app.py once)

---

**Happy Coding! 🎉**

Remember: The best way to learn is by doing. Don't be afraid to experiment and break things - that's how you learn!

