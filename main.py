from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'roommate-finder-secret-key-change-in-production'

# Database setup
def init_db():
    conn = sqlite3.connect('roommate_finder.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # User profiles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            budget INTEGER NOT NULL,
            location TEXT NOT NULL,
            bio TEXT,
            interests TEXT,
            lifestyle_preferences TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Swipes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS swipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            swiper_id INTEGER NOT NULL,
            swiped_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (swiper_id) REFERENCES users (id),
            FOREIGN KEY (swiped_id) REFERENCES users (id),
            UNIQUE(swiper_id, swiped_id)
        )
    ''')
    
    # Matches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user1_id INTEGER NOT NULL,
            user2_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user1_id) REFERENCES users (id),
            FOREIGN KEY (user2_id) REFERENCES users (id),
            UNIQUE(user1_id, user2_id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Helper functions
def get_db_connection():
    conn = sqlite3.connect('roommate_finder.db')
    conn.row_factory = sqlite3.Row
    return conn

def is_logged_in():
    return 'user_id' in session

def require_login(f):
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Add sample data
def add_sample_data():
    conn = get_db_connection()
    
    # Check if sample data already exists
    existing_users = conn.execute('SELECT COUNT(*) as count FROM users').fetchone()
    if existing_users['count'] > 0:
        conn.close()
        return
    
    # Sample users
    conn.execute('''
        INSERT INTO users (username, email, password_hash) VALUES 
        ('alex_smith', 'alex@example.com', ?),
        ('maya_johnson', 'maya@example.com', ?),
        ('sam_wilson', 'sam@example.com', ?),
        ('jessica_brown', 'jessica@example.com', ?),
        ('mike_davis', 'mike@example.com', ?),
        ('sarah_miller', 'sarah@example.com', ?)
    ''', (
        generate_password_hash('password123', method='pbkdf2:sha256'),
        generate_password_hash('password123', method='pbkdf2:sha256'),
        generate_password_hash('password123', method='pbkdf2:sha256'),
        generate_password_hash('password123', method='pbkdf2:sha256'),
        generate_password_hash('password123', method='pbkdf2:sha256'),
        generate_password_hash('password123', method='pbkdf2:sha256')
    ))
    
    conn.commit()
    
    # Sample profiles
    conn.execute('''
        INSERT INTO user_profiles (user_id, name, age, budget, location, bio, interests, lifestyle_preferences) VALUES 
        (2, 'Alex Smith', 22, 600, 'Downtown', 'Love music, gaming, and cooking!', '["Music", "Gaming", "Cooking", "Movies"]', '["Night Owl", "Very Social", "Moderately Clean", "Love Pets"]'),
        (3, 'Maya Johnson', 25, 750, 'Midtown', 'Fitness enthusiast and nature lover.', '["Fitness", "Nature", "Reading", "Photography"]', '["Early Bird", "Quiet", "Very Clean", "Neutral"]'),
        (4, 'Sam Wilson', 23, 650, 'Uptown', 'Artist and photographer.', '["Art", "Photography", "Travel", "Cooking"]', '["Flexible", "Moderately Social", "Moderately Clean", "Love Pets"]'),
        (5, 'Jessica Brown', 24, 700, 'Downtown', 'Tech professional who loves coding.', '["Technology", "Gaming", "Movies", "Music"]', '["Night Owl", "Moderately Social", "Moderately Clean", "Neutral"]'),
        (6, 'Mike Davis', 26, 800, 'Midtown', 'Sports fanatic and outdoor enthusiast.', '["Sports", "Fitness", "Nature", "Travel"]', '["Early Bird", "Very Social", "Very Clean", "No Pets"]'),
        (7, 'Sarah Miller', 21, 550, 'Uptown', 'Student studying art history.', '["Art", "Reading", "Movies", "Nature"]', '["Flexible", "Quiet", "Very Clean", "Neutral"]')
    ''')
    
    conn.commit()
    conn.close()

# Add sample data
add_sample_data()

# Routes
@app.route("/")
def home():
    if is_logged_in():
        return redirect(url_for('swipe'))
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        # Validate inputs
        if not username or not password:
            flash('Please fill in all fields', 'error')
            return render_template("login.html")
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('swipe'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        
        # Validate inputs
        if not username or not email or not password:
            flash('Please fill in all fields', 'error')
            return render_template("signup.html")
            
        if len(username) < 3 or len(username) > 20:
            flash('Username must be between 3 and 20 characters', 'error')
            return render_template("signup.html")
            
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template("signup.html")
            
        if '@' not in email:
            flash('Please enter a valid email address', 'error')
            return render_template("signup.html")
        
        conn = get_db_connection()
        
        # Check if user already exists
        existing_user = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email)).fetchone()
        
        if existing_user:
            flash('Username or email already exists', 'error')
            conn.close()
            return render_template("signup.html")
        
        # Create new user
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        conn.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)', (username, email, password_hash))
        conn.commit()
        
        # Get the new user's ID
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        session['user_id'] = user['id']
        session['username'] = user['username']
        conn.close()
        
        flash('Account created successfully! Please complete your profile.', 'success')
        return redirect(url_for('profile_setup'))
    
    return render_template("signup.html")

@app.route("/profile-setup", methods=["GET", "POST"])
@require_login
def profile_setup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_str = request.form.get("age", "").strip()
        budget_str = request.form.get("budget", "").strip()
        location = request.form.get("location", "").strip()
        bio = request.form.get("bio", "").strip()
        
        # Validate inputs
        if not name or not age_str or not budget_str or not location:
            flash('Please fill in all required fields', 'error')
            return render_template("profile_setup.html")
        
        try:
            age = int(age_str)
            budget = int(budget_str)
            
            if age < 18 or age > 100:
                flash('Age must be between 18 and 100', 'error')
                return render_template("profile_setup.html")
                
            if budget < 300 or budget > 5000:
                flash('Budget must be between $300 and $5000', 'error')
                return render_template("profile_setup.html")
                
        except ValueError:
            flash('Please enter valid numbers for age and budget', 'error')
            return render_template("profile_setup.html")
        
        # Get interests from form
        interests = []
        for key in request.form:
            if key.startswith('interest_'):
                interests.append(request.form.get(key))
        
        # Get lifestyle preferences
        lifestyle_prefs = []
        for key in request.form:
            if key.startswith('lifestyle_'):
                lifestyle_prefs.append(request.form.get(key))
        
        conn = get_db_connection()
        conn.execute('''INSERT INTO user_profiles 
                       (user_id, name, age, budget, location, bio, interests, lifestyle_preferences)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (session['user_id'], name, age, budget, location, bio, str(interests), str(lifestyle_prefs)))
        conn.commit()
        conn.close()
        
        flash('Profile created successfully!', 'success')
        return redirect(url_for('swipe'))
    
    return render_template("profile_setup.html")

@app.route("/swipe")
@require_login
def swipe():
    conn = get_db_connection()
    
    # Get user's profile
    user_profile = conn.execute('SELECT * FROM user_profiles WHERE user_id = ?', (session['user_id'],)).fetchone()
    
    if not user_profile:
        conn.close()
        return redirect(url_for('profile_setup'))
    
    # Get potential matches (users not yet swiped on)
    swiped_users = conn.execute('SELECT swiped_id FROM swipes WHERE swiper_id = ?', (session['user_id'],)).fetchall()
    swiped_ids = [row['swiped_id'] for row in swiped_users]
    
    # Get other users' profiles
    query = '''SELECT up.*, u.username FROM user_profiles up 
               JOIN users u ON up.user_id = u.id 
               WHERE up.user_id != ?'''
    
    params = [session['user_id']]
    
    if swiped_ids:
        query += ' AND up.user_id NOT IN ({})'.format(','.join('?' * len(swiped_ids)))
        params.extend(swiped_ids)
    
    # Get all potential matches
    all_matches = conn.execute(query, params).fetchall()
    
    if not all_matches:
        conn.close()
        return render_template("no_more_matches.html")
    
    # Calculate compatibility scores and sort by best matches
    scored_matches = []
    for match in all_matches:
        score = calculate_compatibility_score(user_profile, match)
        scored_matches.append((match, score))
    
    # Sort by compatibility score (highest first)
    scored_matches.sort(key=lambda x: x[1], reverse=True)
    
    # Select the best match
    best_match = scored_matches[0][0]
    
    conn.close()
    
    return render_template("swipe.html", match=best_match)

def calculate_compatibility_score(user_profile, potential_match):
    """Calculate compatibility score between two users"""
    score = 0
    
    # Budget compatibility
    budget_diff = abs(user_profile['budget'] - potential_match['budget'])
    if budget_diff <= 100:
        score += 30
    elif budget_diff <= 200:
        score += 20
    elif budget_diff <= 300:
        score += 10
    
    # Location compatibility
    if user_profile['location'].lower() == potential_match['location'].lower():
        score += 25
    
    # Age compatibility
    age_diff = abs(user_profile['age'] - potential_match['age'])
    if age_diff <= 2:
        score += 20
    elif age_diff <= 5:
        score += 15
    elif age_diff <= 10:
        score += 10
    
    # Interests compatibility
    user_interests = eval(user_profile['interests']) if user_profile['interests'] else []
    match_interests = eval(potential_match['interests']) if potential_match['interests'] else []
    
    if user_interests and match_interests:
        common_interests = set(user_interests) & set(match_interests)
        interest_score = (len(common_interests) / max(len(user_interests), len(match_interests))) * 25
        score += interest_score
    
    # Lifestyle preferences compatibility
    user_lifestyle = eval(user_profile['lifestyle_preferences']) if user_profile['lifestyle_preferences'] else []
    match_lifestyle = eval(potential_match['lifestyle_preferences']) if potential_match['lifestyle_preferences'] else []
    
    if user_lifestyle and match_lifestyle:
        common_lifestyle = set(user_lifestyle) & set(match_lifestyle)
        lifestyle_score = (len(common_lifestyle) / max(len(user_lifestyle), len(match_lifestyle))) * 20
        score += lifestyle_score
    
    # Add some randomness
    score += random.uniform(0, 5)
    
    return score

@app.route("/swipe_action", methods=["POST"])
@require_login
def swipe_action():
    data = request.get_json()
    swiped_id = data.get('swiped_id')
    action = data.get('action')
    
    conn = get_db_connection()
    
    # Record the swipe
    conn.execute('INSERT INTO swipes (swiper_id, swiped_id, action) VALUES (?, ?, ?)', (session['user_id'], swiped_id, action))
    
    # If it's a like, check if it's a mutual match
    if action == 'like':
        mutual_like = conn.execute('SELECT * FROM swipes WHERE swiper_id = ? AND swiped_id = ? AND action = "like"', (swiped_id, session['user_id'])).fetchone()
        
        if mutual_like:
            # Create a match
            conn.execute('INSERT INTO matches (user1_id, user2_id) VALUES (?, ?)', (min(session['user_id'], swiped_id), max(session['user_id'], swiped_id)))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route("/matches")
@require_login
def matches():
    conn = get_db_connection()
    
    # Get user's matches
    user_matches = conn.execute('''SELECT m.*, up1.name as user1_name, up1.bio as user1_bio, up1.location as user1_location,
                                  up2.name as user2_name, up2.bio as user2_bio, up2.location as user2_location
                                  FROM matches m
                                  JOIN user_profiles up1 ON m.user1_id = up1.user_id
                                  JOIN user_profiles up2 ON m.user2_id = up2.user_id
                                  WHERE m.user1_id = ? OR m.user2_id = ?''', (session['user_id'], session['user_id'])).fetchall()
    
    conn.close()
    
    return render_template("matches.html", matches=user_matches)

@app.route("/rent-splitter")
@require_login
def rent_splitter():
    return render_template("rent_splitter.html")

@app.route("/chat-assistant")
@require_login
def chat_assistant():
    return render_template("chat_assistant.html")

@app.route("/success-predictor")
@require_login
def success_predictor():
    return render_template("success_predictor.html")

@app.route("/reset_profiles", methods=["POST"])
@require_login
def reset_profiles():
    try:
        user_id = session['user_id']
        
        # Delete all swipes for this user to reset their swipe history
        conn = sqlite3.connect('roommate_finder.db')
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM swipes WHERE swiper_id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Profiles reset successfully'})
    except Exception as e:
        print(f"Error resetting profiles: {e}")
        return jsonify({'success': False, 'message': 'Error resetting profiles'})

@app.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)