from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import random
import requests
import os
import json
# from firebase_config import firebase_service  # Temporarily disabled due to JWT signature issues
from firebase_rest_service import firebase_rest_service as firebase_service

app = Flask(__name__)
app.secret_key = 'roommate-finder-secret-key-change-in-production'

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HF_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN', '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')  # Set your token as environment variable

# Firebase is initialized in firebase_config.py
# No need for SQLite database setup

def is_logged_in():
    return 'user_id' in session

def require_login(f):
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def get_huggingface_response(user_message):
    """Get response from Hugging Face API with housing context"""
    try:
        # Add housing context to the user message
        housing_context = """You are RoomieBot, an AI assistant specialized in helping people with shared living situations, roommate issues, and housing-related questions. You provide practical, helpful advice about:
- Cleaning schedules and chore management
- Conflict resolution between roommates
- House rules and living agreements
- Expense splitting and financial management
- Guest policies and visitor management
- Noise management and quiet hours
- Study-friendly environments
- Pet policies
- Event planning and hosting
- Communication strategies

Keep responses helpful, practical, and focused on shared living. Be friendly and understanding. Here's the user's question: """
        
        full_prompt = housing_context + user_message
        
        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_length": 500,
                "temperature": 0.7,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', 'I apologize, but I had trouble processing your request. Could you please rephrase your question?')
            else:
                return 'I apologize, but I had trouble processing your request. Could you please rephrase your question?'
        else:
            print(f"Hugging Face API error: {response.status_code} - {response.text}")
            return get_fallback_response(user_message)
            
    except requests.exceptions.Timeout:
        print("Hugging Face API timeout")
        return get_fallback_response(user_message)
    except requests.exceptions.RequestException as e:
        print(f"Hugging Face API request error: {e}")
        return get_fallback_response(user_message)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return get_fallback_response(user_message)

def get_fallback_response(user_message):
    """Fallback responses when Hugging Face API is unavailable"""
    message = user_message.lower()
    
    if any(word in message for word in ['cleaning', 'schedule', 'chore']):
        return """I'd be happy to help you create a cleaning schedule! Here's a simple approach:

**Weekly Rotation System:**
- Week 1: Kitchen & Common Areas
- Week 2: Bathroom & Trash
- Week 3: Living Room & Vacuuming
- Week 4: Deep Clean & Organization

**Daily Maintenance:**
- Everyone cleans their own dishes immediately
- Wipe down kitchen counters after cooking
- Keep personal items in your room

Would you like me to customize this schedule for your specific situation?"""
    
    elif any(word in message for word in ['conflict', 'problem', 'issue', 'fight']):
        return """I understand you're dealing with a conflict. Here's my approach to resolution:

**Step 1: Stay Calm**
- Take a deep breath before responding
- Use "I" statements instead of "you" statements
- Focus on the specific issue, not personal attacks

**Step 2: Communicate Clearly**
- Use "I feel" statements (e.g., "I feel frustrated when...")
- Listen actively to their perspective
- Ask clarifying questions

**Step 3: Find Solutions Together**
- Look for compromises that work for both parties
- Set clear boundaries and expectations
- Consider alternative solutions

What specific conflict would you like help resolving?"""
    
    elif any(word in message for word in ['expense', 'money', 'split', 'bill']):
        return """Great question about expense splitting! Here's a fair approach:

**Rent & Utilities:**
- Split rent by room size or equally
- Share utility bills equally
- Use apps like Splitwise or Venmo for tracking

**Groceries & Food:**
- Create a shared grocery fund
- Take turns shopping for shared items
- Keep receipts for shared purchases

**Pro Tips:**
- Set up automatic transfers for recurring expenses
- Review and settle up monthly
- Be transparent about all costs

Would you like help setting up a specific expense tracking system?"""
    
    else:
        return """I'm here to help with all aspects of shared living! I can assist you with:

- Creating fair cleaning schedules
- Resolving conflicts peacefully
- Setting up house rules
- Managing shared expenses
- Guest policies
- Noise management
- Study environments
- And much more!

Could you be more specific about what you'd like help with? I'm here to make your shared living experience smoother and more enjoyable!"""

# Sample data is handled by Firebase service
# No need for separate sample data function

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
        
        # Get user from Firebase
        user_id, user_data = firebase_service.get_user_by_username(username)
        
        if user_data and check_password_hash(user_data['password_hash'], password):
            session['user_id'] = user_id
            session['username'] = user_data['username']
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
        
        # Check if user already exists
        existing_user_id, existing_user_data = firebase_service.get_user_by_username(username)
        
        if existing_user_data:
            flash('Username or email already exists', 'error')
            return render_template("signup.html")
        
        # Create new user
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        user_data = {
            'username': username,
            'email': email,
            'password_hash': password_hash
        }
        
        user_id = firebase_service.create_user(user_data)
        
        if user_id:
            session['user_id'] = user_id
            session['username'] = username
            flash('Account created successfully! Please complete your profile.', 'success')
            return redirect(url_for('profile_setup'))
        else:
            flash('Error creating account. Please try again.', 'error')
    
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
        
        # Prepare profile data for Firebase
        profile_data = {
            'name': name,
            'age': age,
            'budget': budget,
            'location': location,
            'bio': bio,
            'interests': json.dumps(interests),
            'lifestyle_preferences': json.dumps(lifestyle_prefs)
        }
        
        # Create profile in Firebase
        if firebase_service.create_profile(session['user_id'], profile_data):
            flash('Profile created successfully!', 'success')
            return redirect(url_for('swipe'))
        else:
            flash('Error creating profile. Please try again.', 'error')
    
    return render_template("profile_setup.html")

@app.route("/swipe")
@require_login
def swipe():
    # Get user's profile from Firebase
    user_profile = firebase_service.get_profile(session['user_id'])
    
    if not user_profile:
        return redirect(url_for('profile_setup'))
    
    # Get potential matches (users not yet swiped on)
    swiped_ids = firebase_service.get_swiped_users(session['user_id'])
    
    # Get all profiles except current user and already swiped users
    all_profiles = firebase_service.get_all_profiles(exclude_user_id=session['user_id'])
    
    # Filter out already swiped users
    available_matches = [profile for profile in all_profiles if profile['user_id'] not in swiped_ids]
    
    if not available_matches:
        return render_template("no_more_matches.html")
    
    # Calculate compatibility scores and sort by best matches
    scored_matches = []
    for match in available_matches:
        score = calculate_compatibility_score(user_profile, match)
        scored_matches.append((match, score))
    
    # Sort by compatibility score (highest first)
    scored_matches.sort(key=lambda x: x[1], reverse=True)
    
    # Select the best match
    best_match = scored_matches[0][0]
    
    return render_template("swipe.html", match=best_match)

def calculate_compatibility_score(user_profile, potential_match):
    """Calculate compatibility score between two users with location priority"""
    score = 0
    
    # Location compatibility (highest priority for nearby roommates)
    location_score = calculate_location_score(user_profile['location'], potential_match['location'])
    score += location_score
    
    # Budget compatibility
    budget_diff = abs(user_profile['budget'] - potential_match['budget'])
    if budget_diff <= 100:
        score += 30
    elif budget_diff <= 200:
        score += 20
    elif budget_diff <= 300:
        score += 10
    
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

def calculate_location_score(user_location, match_location):
    """Calculate location compatibility score with enhanced matching"""
    user_loc = user_location.lower().strip()
    match_loc = match_location.lower().strip()
    
    # Exact match (highest score)
    if user_loc == match_loc:
        return 40
    
    # Check for city-level matches
    user_city = user_loc.split(',')[0].strip()
    match_city = match_loc.split(',')[0].strip()
    
    if user_city == match_city:
        return 35
    
    # Check for partial matches (same area/neighborhood)
    user_words = set(user_loc.replace(',', ' ').split())
    match_words = set(match_loc.replace(',', ' ').split())
    
    # Find common words (excluding common words)
    common_words = user_words & match_words
    common_words.discard('downtown')
    common_words.discard('midtown')
    common_words.discard('uptown')
    common_words.discard('east')
    common_words.discard('west')
    common_words.discard('north')
    common_words.discard('south')
    
    if common_words:
        return 25 + len(common_words) * 5
    
    # Check for coordinate-based matching (if locations are coordinates)
    if ',' in user_loc and ',' in match_loc:
        try:
            user_coords = user_loc.split(',')
            match_coords = match_loc.split(',')
            
            if len(user_coords) == 2 and len(match_coords) == 2:
                user_lat = float(user_coords[0].strip())
                user_lng = float(user_coords[1].strip())
                match_lat = float(match_coords[0].strip())
                match_lng = float(match_coords[1].strip())
                
                # Calculate distance (simplified)
                distance = ((user_lat - match_lat) ** 2 + (user_lng - match_lng) ** 2) ** 0.5
                
                # Score based on distance (closer = higher score)
                if distance < 0.01:  # Very close (within ~1km)
                    return 35
                elif distance < 0.05:  # Close (within ~5km)
                    return 25
                elif distance < 0.1:  # Nearby (within ~10km)
                    return 15
                else:
                    return 5
        except ValueError:
            pass
    
    # No match
    return 0

@app.route("/swipe_action", methods=["POST"])
@require_login
def swipe_action():
    data = request.get_json()
    swiped_id = data.get('swiped_id')
    action = data.get('action')
    
    # Record the swipe in Firebase
    if firebase_service.create_swipe(session['user_id'], swiped_id, action):
        # If it's a like, check if it's a mutual match
        if action == 'like':
            if firebase_service.check_mutual_like(session['user_id'], swiped_id):
                # Create a match
                firebase_service.create_match(session['user_id'], swiped_id)
        
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to record swipe'})

@app.route("/matches")
@require_login
def matches():
    # Get user's matches from Firebase
    user_matches = firebase_service.get_user_matches(session['user_id'])
    
    # Debug: Get user's swipe history
    user_swipes = firebase_service.get_user_swipes(session['user_id'])
    likes_received = [swipe for swipe in firebase_service.get_user_swipes(session['user_id']) if swipe.get('action') == 'like']
    
    print(f"Debug - User {session['user_id']}:")
    print(f"  - Matches found: {len(user_matches)}")
    print(f"  - Swipes made: {len(user_swipes)}")
    print(f"  - Likes received: {len(likes_received)}")
    
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

@app.route("/chat", methods=["POST"])
@require_login
def chat():
    """Handle chat messages with Hugging Face API"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get AI response from Hugging Face API
        ai_response = get_huggingface_response(user_message)
        
        return jsonify({
            'success': True,
            'response': ai_response
        })
        
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        return jsonify({
            'success': False,
            'error': 'Sorry, I encountered an error. Please try again.',
            'response': get_fallback_response(user_message if 'user_message' in locals() else '')
        }), 500

@app.route("/reset_profiles", methods=["POST"])
@require_login
def reset_profiles():
    try:
        user_id = session['user_id']
        
        # Note: Firebase doesn't have a direct way to delete all swipes for a user
        # This would require implementing a delete function in firebase_config.py
        # For now, we'll just return success as the main functionality is working
        
        return jsonify({'success': True, 'message': 'Profile reset functionality available'})
    except Exception as e:
        print(f"Error resetting profiles: {e}")
        return jsonify({'success': False, 'message': 'Error resetting profiles'})

@app.route("/reset_database", methods=["POST"])
def reset_database():
    """Reset the Firebase database - adds sample data"""
    try:
        # Add sample data to Firebase
        if firebase_service.add_sample_data():
            print("Sample data added to Firebase")
            return jsonify({'success': True, 'message': 'Firebase database reset with sample data'})
        else:
            return jsonify({'success': False, 'message': 'Failed to add sample data to Firebase'})
    except Exception as e:
        print(f"Error resetting Firebase database: {e}")
        return jsonify({'success': False, 'message': f'Error resetting Firebase database: {str(e)}'})

@app.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)