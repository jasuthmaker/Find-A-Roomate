"""
Firebase Configuration and Service
Handles all Firebase Realtime Database operations
"""

import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

class FirebaseService:
    def __init__(self):
        self.app = None
        self.db = None
        self.initialize_firebase()
    
    def initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Check if Firebase is already initialized
            if firebase_admin._apps:
                self.app = firebase_admin.get_app()
            else:
                # Initialize Firebase with service account
                service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH', 'firebase-service-account.json')
                database_url = os.getenv('FIREBASE_DATABASE_URL', 'https://dromie-58a40-default-rtdb.firebaseio.com/')
                
                print(f"Using service account: {service_account_path}")
                print(f"Using database URL: {database_url}")
                
                if os.path.exists(service_account_path):
                    try:
                        cred = credentials.Certificate(service_account_path)
                        self.app = firebase_admin.initialize_app(cred, {
                            'databaseURL': database_url
                        })
                    except Exception as cred_error:
                        print(f"❌ Service account credential error: {cred_error}")
                        print("🔧 Please regenerate your Firebase service account key")
                        print("1. Go to Firebase Console → Project Settings → Service Accounts")
                        print("2. Click 'Generate new private key'")
                        print("3. Replace the firebase-service-account.json file")
                        return
                else:
                    # For development, you can use a default configuration
                    print("Warning: Firebase service account file not found. Please set up Firebase credentials.")
                    return
            
            # Get database reference
            self.db = db.reference()
            print("✅ Firebase initialized successfully")
            
        except Exception as e:
            print(f"❌ Firebase initialization failed: {e}")
            print("🔧 Please check your Firebase service account key and database URL")
            self.app = None
            self.db = None
    
    def is_connected(self):
        """Check if Firebase is connected"""
        return self.db is not None
    
    # User Management
    def create_user(self, user_data):
        """Create a new user in Firebase"""
        if not self.is_connected():
            return None
        
        try:
            user_id = self.db.child('users').push(user_data)
            return user_id.key
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user(self, user_id):
        """Get user by ID"""
        if not self.is_connected():
            return None
        
        try:
            return self.db.child('users').child(user_id).get()
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_user_by_username(self, username):
        """Get user by username"""
        if not self.is_connected():
            return None
        
        try:
            users = self.db.child('users').get()
            if users:
                for user_id, user_data in users.items():
                    if user_data and user_data.get('username') == username:
                        return user_id, user_data
            return None, None
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None, None
    
    def update_user(self, user_id, user_data):
        """Update user data"""
        if not self.is_connected():
            return False
        
        try:
            self.db.child('users').child(user_id).update(user_data)
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    # Profile Management
    def create_profile(self, user_id, profile_data):
        """Create user profile"""
        if not self.is_connected():
            return False
        
        try:
            # Ensure user_id is a string
            user_id_str = str(user_id)
            profile_data['created_at'] = datetime.now().isoformat()
            self.db.child('profiles').child(user_id_str).set(profile_data)
            return True
        except Exception as e:
            print(f"Error creating profile: {e}")
            return False
    
    def get_profile(self, user_id):
        """Get user profile"""
        if not self.is_connected():
            return None
        
        try:
            user_id_str = str(user_id)
            return self.db.child('profiles').child(user_id_str).get()
        except Exception as e:
            print(f"Error getting profile: {e}")
            return None
    
    def get_all_profiles(self, exclude_user_id=None):
        """Get all profiles except the specified user"""
        if not self.is_connected():
            return []
        
        try:
            profiles = self.db.child('profiles').get()
            if not profiles:
                return []
            
            profile_list = []
            exclude_user_id_str = str(exclude_user_id) if exclude_user_id else None
            for user_id, profile_data in profiles.items():
                if profile_data and (exclude_user_id_str is None or user_id != exclude_user_id_str):
                    profile_data['user_id'] = user_id
                    profile_list.append(profile_data)
            
            return profile_list
        except Exception as e:
            print(f"Error getting all profiles: {e}")
            return []
    
    def update_profile(self, user_id, profile_data):
        """Update user profile"""
        if not self.is_connected():
            return False
        
        try:
            user_id_str = str(user_id)
            self.db.child('profiles').child(user_id_str).update(profile_data)
            return True
        except Exception as e:
            print(f"Error updating profile: {e}")
            return False
    
    # Swipes Management
    def create_swipe(self, swiper_id, swiped_id, action):
        """Create a swipe record"""
        if not self.is_connected():
            return False
        
        try:
            swipe_data = {
                'swiper_id': str(swiper_id),
                'swiped_id': str(swiped_id),
                'action': action,
                'created_at': datetime.now().isoformat()
            }
            self.db.child('swipes').push(swipe_data)
            return True
        except Exception as e:
            print(f"Error creating swipe: {e}")
            return False
    
    def get_user_swipes(self, user_id):
        """Get all swipes made by a user"""
        if not self.is_connected():
            return []
        
        try:
            swipes = self.db.child('swipes').get()
            if not swipes:
                return []
            
            user_swipes = []
            user_id_str = str(user_id)
            for swipe_id, swipe_data in swipes.items():
                if swipe_data and swipe_data.get('swiper_id') == user_id_str:
                    user_swipes.append(swipe_data)
            
            return user_swipes
        except Exception as e:
            print(f"Error getting user swipes: {e}")
            return []
    
    def get_swiped_users(self, user_id):
        """Get list of user IDs that the user has swiped on"""
        if not self.is_connected():
            return []
        
        try:
            swipes = self.db.child('swipes').get()
            if not swipes:
                return []
            
            swiped_ids = []
            user_id_str = str(user_id)
            for swipe_id, swipe_data in swipes.items():
                if swipe_data and swipe_data.get('swiper_id') == user_id_str:
                    swiped_ids.append(swipe_data.get('swiped_id'))
            
            return swiped_ids
        except Exception as e:
            print(f"Error getting swiped users: {e}")
            return []
    
    def check_mutual_like(self, user1_id, user2_id):
        """Check if two users have liked each other"""
        if not self.is_connected():
            return False
        
        try:
            swipes = self.db.child('swipes').get()
            if not swipes:
                return False
            
            user1_liked_user2 = False
            user2_liked_user1 = False
            user1_id_str = str(user1_id)
            user2_id_str = str(user2_id)
            
            for swipe_id, swipe_data in swipes.items():
                if swipe_data:
                    swiper_id = swipe_data.get('swiper_id')
                    swiped_id = swipe_data.get('swiped_id')
                    action = swipe_data.get('action')
                    
                    if swiper_id == user1_id_str and swiped_id == user2_id_str and action == 'like':
                        user1_liked_user2 = True
                    elif swiper_id == user2_id_str and swiped_id == user1_id_str and action == 'like':
                        user2_liked_user1 = True
            
            return user1_liked_user2 and user2_liked_user1
        except Exception as e:
            print(f"Error checking mutual like: {e}")
            return False
    
    # Matches Management
    def create_match(self, user1_id, user2_id):
        """Create a match between two users"""
        if not self.is_connected():
            return False
        
        try:
            match_data = {
                'user1_id': str(user1_id),
                'user2_id': str(user2_id),
                'created_at': datetime.now().isoformat()
            }
            self.db.child('matches').push(match_data)
            return True
        except Exception as e:
            print(f"Error creating match: {e}")
            return False
    
    def get_user_matches(self, user_id):
        """Get all matches for a user"""
        if not self.is_connected():
            return []
        
        try:
            matches = self.db.child('matches').get()
            if not matches:
                return []
            
            user_matches = []
            user_id_str = str(user_id)
            for match_id, match_data in matches.items():
                if match_data:
                    if match_data.get('user1_id') == user_id_str or match_data.get('user2_id') == user_id_str:
                        # Get profile data for both users
                        user1_profile = self.get_profile(match_data.get('user1_id'))
                        user2_profile = self.get_profile(match_data.get('user2_id'))
                        
                        if user1_profile and user2_profile:
                            match_info = {
                                'match_id': match_id,
                                'user1_id': match_data.get('user1_id'),
                                'user2_id': match_data.get('user2_id'),
                                'user1_name': user1_profile.get('name'),
                                'user1_bio': user1_profile.get('bio'),
                                'user1_location': user1_profile.get('location'),
                                'user2_name': user2_profile.get('name'),
                                'user2_bio': user2_profile.get('bio'),
                                'user2_location': user2_profile.get('location'),
                                'created_at': match_data.get('created_at')
                            }
                            user_matches.append(match_info)
            
            return user_matches
        except Exception as e:
            print(f"Error getting user matches: {e}")
            return []
    
    # Sample Data
    def add_sample_data(self):
        """Add sample data to Firebase"""
        if not self.is_connected():
            return False
        
        try:
            # Sample users
            sample_users = [
                {
                    'username': 'alex_smith',
                    'email': 'alex@example.com',
                    'password_hash': 'pbkdf2:sha256:260000$...',  # You'll need to generate real hashes
                    'created_at': datetime.now().isoformat()
                },
                {
                    'username': 'maya_johnson',
                    'email': 'maya@example.com',
                    'password_hash': 'pbkdf2:sha256:260000$...',
                    'created_at': datetime.now().isoformat()
                },
                {
                    'username': 'sam_wilson',
                    'email': 'sam@example.com',
                    'password_hash': 'pbkdf2:sha256:260000$...',
                    'created_at': datetime.now().isoformat()
                },
                {
                    'username': 'jessica_brown',
                    'email': 'jessica@example.com',
                    'password_hash': 'pbkdf2:sha256:260000$...',
                    'created_at': datetime.now().isoformat()
                },
                {
                    'username': 'mike_davis',
                    'email': 'mike@example.com',
                    'password_hash': 'pbkdf2:sha256:260000$...',
                    'created_at': datetime.now().isoformat()
                },
                {
                    'username': 'sarah_miller',
                    'email': 'sarah@example.com',
                    'password_hash': 'pbkdf2:sha256:260000$...',
                    'created_at': datetime.now().isoformat()
                }
            ]
            
            # Add users
            for user_data in sample_users:
                user_id = self.create_user(user_data)
                if user_id:
                    print(f"Created user: {user_data['username']} with ID: {user_id}")
            
            # Sample profiles
            sample_profiles = [
                {
                    'user_id': 'alex_smith',
                    'name': 'Alex Smith',
                    'age': 22,
                    'budget': 600,
                    'location': 'Downtown',
                    'bio': 'Love music, gaming, and cooking!',
                    'interests': '["Music", "Gaming", "Cooking", "Movies"]',
                    'lifestyle_preferences': '["Night Owl", "Very Social", "Moderately Clean", "Love Pets"]',
                    'created_at': datetime.now().isoformat()
                },
                {
                    'user_id': 'maya_johnson',
                    'name': 'Maya Johnson',
                    'age': 25,
                    'budget': 750,
                    'location': 'Midtown',
                    'bio': 'Fitness enthusiast and nature lover.',
                    'interests': '["Fitness", "Nature", "Reading", "Photography"]',
                    'lifestyle_preferences': '["Early Bird", "Quiet", "Very Clean", "Neutral"]',
                    'created_at': datetime.now().isoformat()
                },
                {
                    'user_id': 'sam_wilson',
                    'name': 'Sam Wilson',
                    'age': 23,
                    'budget': 650,
                    'location': 'Uptown',
                    'bio': 'Artist and photographer.',
                    'interests': '["Art", "Photography", "Travel", "Cooking"]',
                    'lifestyle_preferences': '["Flexible", "Moderately Social", "Moderately Clean", "Love Pets"]',
                    'created_at': datetime.now().isoformat()
                },
                {
                    'user_id': 'jessica_brown',
                    'name': 'Jessica Brown',
                    'age': 24,
                    'budget': 700,
                    'location': 'Downtown',
                    'bio': 'Tech professional who loves coding.',
                    'interests': '["Technology", "Gaming", "Movies", "Music"]',
                    'lifestyle_preferences': '["Night Owl", "Moderately Social", "Moderately Clean", "Neutral"]',
                    'created_at': datetime.now().isoformat()
                },
                {
                    'user_id': 'mike_davis',
                    'name': 'Mike Davis',
                    'age': 26,
                    'budget': 800,
                    'location': 'Midtown',
                    'bio': 'Sports fanatic and outdoor enthusiast.',
                    'interests': '["Sports", "Fitness", "Nature", "Travel"]',
                    'lifestyle_preferences': '["Early Bird", "Very Social", "Very Clean", "No Pets"]',
                    'created_at': datetime.now().isoformat()
                },
                {
                    'user_id': 'sarah_miller',
                    'name': 'Sarah Miller',
                    'age': 21,
                    'budget': 550,
                    'location': 'Uptown',
                    'bio': 'Student studying art history.',
                    'interests': '["Art", "Reading", "Movies", "Nature"]',
                    'lifestyle_preferences': '["Flexible", "Quiet", "Very Clean", "Neutral"]',
                    'created_at': datetime.now().isoformat()
                }
            ]
            
            # Add profiles
            for profile_data in sample_profiles:
                if self.create_profile(profile_data['user_id'], profile_data):
                    print(f"Created profile for: {profile_data['name']}")
            
            print("✅ Sample data added to Firebase successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error adding sample data: {e}")
            return False

# Global Firebase service instance
firebase_service = FirebaseService()
