# 📖 Project Overview - How Everything Works Together

This document explains how all the pieces of the Movie Ticket Booking Platform fit together.

## 🔄 Application Flow

### 1. **User Registration & Login Flow**

```
User visits website
    ↓
Clicks "Register"
    ↓
Fills registration form (username, email, password)
    ↓
routes.py → register() function processes form
    ↓
Password is hashed (encrypted) using Werkzeug
    ↓
User record saved to database (users table)
    ↓
User redirected to login page
    ↓
User logs in with credentials
    ↓
routes.py → login() function verifies password
    ↓
Flask-Login creates session (user is now "logged in")
    ↓
User redirected to home page
```

### 2. **Movie Booking Flow**

```
User browses movies on home page
    ↓
Clicks "View Shows" on a movie
    ↓
routes.py → movie_detail() shows movie info and available shows
    ↓
User selects a show time
    ↓
routes.py → show_seats() displays seat layout
    ↓
JavaScript handles seat selection (show_seats.html)
    ↓
User clicks "Book Tickets"
    ↓
JavaScript sends AJAX request to /book endpoint
    ↓
routes.py → book_tickets() function:
    - Creates Booking record
    - Assigns selected seats to booking
    - Updates seat availability
    ↓
Booking confirmation
    ↓
User redirected to "My Bookings" page
```

### 3. **Database Relationships**

```
User (1) ──────< (Many) Bookings
                          │
                          │
                    Show (1) ──────< (Many) Seats
                          │
                          │
                    Movie (1) ──────< (Many) Shows
```

**Explanation:**
- One user can have many bookings
- One booking has many seats
- One show has many seats
- One movie can have many shows

## 📁 File Responsibilities

### **app.py** - The Heart of the Application
- Creates Flask application instance
- Configures database connection
- Sets up Flask-Login
- Imports all routes and models
- Starts the web server

**Key Concepts:**
- `app = Flask(__name__)` - Creates the Flask app
- `db = SQLAlchemy(app)` - Connects to database
- `@login_manager.user_loader` - Tells Flask-Login how to find users

### **models.py** - Database Structure
- Defines all database tables as Python classes
- Each class = one database table
- Relationships between tables (one-to-many)

**Key Concepts:**
- `db.Model` - Base class for all database models
- `db.Column()` - Defines a column in the table
- `db.relationship()` - Links tables together
- `primary_key=True` - Unique identifier for each row
- `ForeignKey()` - Links to another table

### **routes.py** - All Web Pages and Actions
- Each function = one URL endpoint
- Handles GET (display page) and POST (process form) requests
- Uses `@app.route()` decorator to define URLs

**Key Concepts:**
- `@app.route('/url')` - Defines a URL
- `render_template()` - Shows HTML page
- `request.form` - Gets data from forms
- `@login_required` - Protects pages (requires login)
- `current_user` - Access to logged-in user

### **templates/** - HTML Pages
- `base.html` - Base template with navigation (all pages extend this)
- Other HTML files - Individual pages
- Uses Jinja2 templating (Flask's template engine)

**Key Concepts:**
- `{% extends "base.html" %}` - Inherits from base template
- `{{ variable }}` - Displays Python variable
- `{% for item in items %}` - Loops through data
- `{% if condition %}` - Conditional display

### **static/css/style.css** - Styling
- All visual styling for the website
- Colors, layouts, animations
- Responsive design (works on mobile)

### **static/js/main.js** - JavaScript
- Client-side interactivity
- Seat selection logic
- Form validation
- AJAX requests

## 🔐 Security Features

### Password Hashing
```python
# When registering:
user.set_password(password)  # Hashes password

# When logging in:
user.check_password(password)  # Verifies password
```
**Why?** Passwords are never stored in plain text. They're encrypted using Werkzeug's hashing.

### Session Management
- Flask-Login manages user sessions
- Session stored in browser cookie (encrypted)
- `@login_required` protects pages

### SQL Injection Prevention
- SQLAlchemy ORM automatically escapes SQL queries
- Never write raw SQL with user input

## 🗄️ Database Operations

### Creating Records
```python
user = User(username="john", email="john@example.com")
user.set_password("password123")
db.session.add(user)
db.session.commit()  # Saves to database
```

### Reading Records
```python
# Get all users
users = User.query.all()

# Get user by ID
user = User.query.get(1)

# Filter users
user = User.query.filter_by(username="john").first()
```

### Updating Records
```python
user = User.query.get(1)
user.email = "newemail@example.com"
db.session.commit()
```

### Deleting Records
```python
user = User.query.get(1)
db.session.delete(user)
db.session.commit()
```

## 🎨 Frontend-Backend Communication

### 1. **Form Submission (Traditional)**
```html
<!-- HTML Form -->
<form method="POST" action="/register">
    <input name="username">
    <button type="submit">Submit</button>
</form>
```
```python
# Backend receives data
username = request.form.get('username')
```

### 2. **AJAX Request (Modern)**
```javascript
// JavaScript sends data
fetch('/book', {
    method: 'POST',
    body: JSON.stringify({seat_ids: [1, 2, 3]})
})
```
```python
# Backend receives JSON
data = request.get_json()
seat_ids = data.get('seat_ids')
```

## 🚀 How Flask Works

1. **User visits URL** (e.g., `http://localhost:5000/login`)
2. **Flask matches URL** to route in `routes.py`
3. **Route function executes** (e.g., `login()`)
4. **Function processes request** (gets form data, queries database)
5. **Function returns response** (HTML page or JSON data)
6. **Browser displays response**

## 📊 Request-Response Cycle

```
Browser Request
    ↓
Flask receives request
    ↓
Routes.py finds matching function
    ↓
Function executes (queries database, processes data)
    ↓
Function returns HTML template or JSON
    ↓
Flask sends response to browser
    ↓
Browser renders page
```

## 🎯 Key Learning Points

1. **MVC Pattern** (Model-View-Controller)
   - **Model** = `models.py` (database)
   - **View** = `templates/` (HTML)
   - **Controller** = `routes.py` (logic)

2. **Separation of Concerns**
   - Each file has a specific purpose
   - Database logic in models
   - Page logic in routes
   - Styling in CSS
   - Interactivity in JavaScript

3. **Database Relationships**
   - Foreign keys link tables
   - Relationships enable complex queries
   - One-to-many is most common

4. **Template Inheritance**
   - Base template defines common structure
   - Child templates extend base
   - Reduces code duplication

## 🔍 Debugging Tips

1. **Print statements** - Add `print(variable)` to see values
2. **Browser console** - Press F12, check Console tab for JavaScript errors
3. **Flask debug mode** - Shows detailed error pages
4. **Database inspection** - Use SQLite browser to view database
5. **Check terminal** - Flask shows errors in terminal

## 📝 Common Patterns

### Pattern 1: Display List
```python
# Route
movies = Movie.query.all()
return render_template('index.html', movies=movies)

# Template
{% for movie in movies %}
    <h3>{{ movie.title }}</h3>
{% endfor %}
```

### Pattern 2: Form Processing
```python
if request.method == 'POST':
    # Process form
    data = request.form.get('field')
    # Save to database
    return redirect(url_for('success'))
else:
    # Show form
    return render_template('form.html')
```

### Pattern 3: Protected Route
```python
@app.route('/protected')
@login_required
def protected_page():
    return render_template('protected.html')
```

---

**Understanding these concepts will help you modify and extend the application!**

