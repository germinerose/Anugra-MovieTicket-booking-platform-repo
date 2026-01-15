"""
Sample Data Script - Add sample movies and shows to the database

Run this script after setting up the application to add sample data:
    python add_sample_data.py

This will help you test the application without manually adding data.
"""

from app import app, db
from models import Movie, Show, Seat
from datetime import datetime, timedelta

def add_sample_data():
    """Add sample movies and shows to the database"""
    
    with app.app_context():
        # Clear existing data (optional - comment out if you want to keep existing data)
        # db.drop_all()
        # db.create_all()
        
        # Check if movies already exist
        if Movie.query.first():
            print("Sample data already exists! Skipping...")
            return
        
        print("Adding sample movies...")
        
        # Sample Movies
        movies_data = [
            {
                'title': 'The Dark Knight',
                'description': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'duration': 152,
                'genre': 'Action, Crime, Drama',
                'rating': 'PG-13',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg'
            },
            {
                'title': 'Inception',
                'description': 'A skilled thief is given a chance at redemption if he can pull off an impossible task: Inception, the implantation of another person\'s idea into a target\'s subconscious.',
                'duration': 148,
                'genre': 'Action, Sci-Fi, Thriller',
                'rating': 'PG-13',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg'
            },
            {
                'title': 'The Matrix',
                'description': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
                'duration': 136,
                'genre': 'Action, Sci-Fi',
                'rating': 'R',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg'
            },
            {
                'title': 'Interstellar',
                'description': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
                'duration': 169,
                'genre': 'Adventure, Drama, Sci-Fi',
                'rating': 'PG-13',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg'
            },
            {
                'title': 'Pulp Fiction',
                'description': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
                'duration': 154,
                'genre': 'Crime, Drama',
                'rating': 'R',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3Yz5NTljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg'
            }
        ]
        
        movies = []
        for movie_data in movies_data:
            movie = Movie(**movie_data)
            db.session.add(movie)
            movies.append(movie)
        
        db.session.commit()
        print(f"✓ Added {len(movies)} movies")
        
        print("Adding sample shows...")
        
        # Add shows for each movie
        show_times = []
        base_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        
        # If current time is past 10 AM, start from tomorrow
        if base_time < datetime.now():
            base_time += timedelta(days=1)
        
        for movie in movies:
            # Add 3 shows per movie on different days
            for day_offset in range(3):
                for screen in [1, 2]:
                    show_time = base_time + timedelta(days=day_offset, hours=screen * 3)
                    
                    show = Show(
                        movie_id=movie.id,
                        show_time=show_time,
                        screen_number=screen,
                        total_seats=50,
                        price=250.00 + (screen * 50)  # Screen 1: ₹250, Screen 2: ₹300
                    )
                    db.session.add(show)
                    show_times.append(show)
        
        db.session.commit()
        print(f"✓ Added {len(show_times)} shows")
        
        print("\n" + "="*50)
        print("Sample data added successfully!")
        print("="*50)
        print("\nYou can now:")
        print("1. Register a new account")
        print("2. Login and browse movies")
        print("3. Book tickets for any show")
        print("\nRun the application with: python app.py")

if __name__ == '__main__':
    add_sample_data()

