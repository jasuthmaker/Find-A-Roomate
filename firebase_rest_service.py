"""
Firebase REST API Service - Temporary workaround for JWT signature issues
"""

import requests
import json
from datetime import datetime

class FirebaseRestService:
    def __init__(self):
        self.database_url = "https://dromie-58a40-default-rtdb.firebaseio.com"
        self.base_url = f"{self.database_url}/.json"
    
    def is_connected(self):
        """Check if Firebase is accessible"""
        try:
            response = requests.get(self.base_url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_user_by_username(self, username):
        """Get user by username using REST API"""
        try:
            response = requests.get(f"{self.database_url}/users.json")
            if response.status_code == 200:
                users = response.json()
                if users:
                    for user_id, user_data in users.items():
                        if user_data and user_data.get('username') == username:
                            return user_id, user_data
            return None, None
        except Exception as e:
            print(f"Error getting user by username: {e}")
            return None, None
    
    def create_user(self, user_data):
        """Create a new user using REST API"""
        try:
            response = requests.post(f"{self.database_url}/users.json", json=user_data)
            if response.status_code == 200:
                result = response.json()
                return result.get('name')  # Firebase returns the key in 'name' field
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_profile(self, user_id):
        """Get user profile using REST API"""
        try:
            response = requests.get(f"{self.database_url}/profiles/{user_id}.json")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error getting profile: {e}")
            return None
    
    def create_profile(self, user_id, profile_data):
        """Create user profile using REST API"""
        try:
            profile_data['created_at'] = datetime.now().isoformat()
            response = requests.put(f"{self.database_url}/profiles/{user_id}.json", json=profile_data)
            return response.status_code == 200
        except Exception as e:
            print(f"Error creating profile: {e}")
            return False
    
    def get_all_profiles(self, exclude_user_id=None):
        """Get all profiles using REST API"""
        try:
            response = requests.get(f"{self.database_url}/profiles.json")
            if response.status_code == 200:
                profiles = response.json()
                if not profiles:
                    return []
                
                profile_list = []
                exclude_user_id_str = str(exclude_user_id) if exclude_user_id else None
                for user_id, profile_data in profiles.items():
                    if profile_data and (exclude_user_id_str is None or user_id != exclude_user_id_str):
                        profile_data['user_id'] = user_id
                        profile_list.append(profile_data)
                
                return profile_list
            return []
        except Exception as e:
            print(f"Error getting all profiles: {e}")
            return []
    
    def get_swiped_users(self, user_id):
        """Get list of user IDs that the user has swiped on"""
        try:
            response = requests.get(f"{self.database_url}/swipes.json")
            if response.status_code == 200:
                swipes = response.json()
                if not swipes:
                    return []
                
                swiped_ids = []
                user_id_str = str(user_id)
                for swipe_id, swipe_data in swipes.items():
                    if swipe_data and swipe_data.get('swiper_id') == user_id_str:
                        swiped_ids.append(swipe_data.get('swiped_id'))
                
                return swiped_ids
            return []
        except Exception as e:
            print(f"Error getting swiped users: {e}")
            return []
    
    def create_swipe(self, swiper_id, swiped_id, action):
        """Create a swipe record using REST API"""
        try:
            swipe_data = {
                'swiper_id': str(swiper_id),
                'swiped_id': str(swiped_id),
                'action': action,
                'created_at': datetime.now().isoformat()
            }
            response = requests.post(f"{self.database_url}/swipes.json", json=swipe_data)
            return response.status_code == 200
        except Exception as e:
            print(f"Error creating swipe: {e}")
            return False
    
    def check_mutual_like(self, user1_id, user2_id):
        """Check if two users have liked each other"""
        try:
            response = requests.get(f"{self.database_url}/swipes.json")
            if response.status_code == 200:
                swipes = response.json()
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
            return False
        except Exception as e:
            print(f"Error checking mutual like: {e}")
            return False
    
    def create_match(self, user1_id, user2_id):
        """Create a match between two users"""
        try:
            match_data = {
                'user1_id': str(user1_id),
                'user2_id': str(user2_id),
                'created_at': datetime.now().isoformat()
            }
            response = requests.post(f"{self.database_url}/matches.json", json=match_data)
            return response.status_code == 200
        except Exception as e:
            print(f"Error creating match: {e}")
            return False
    
    def get_user_matches(self, user_id):
        """Get all matches for a user"""
        try:
            response = requests.get(f"{self.database_url}/matches.json")
            if response.status_code == 200:
                matches = response.json()
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
            return []
        except Exception as e:
            print(f"Error getting user matches: {e}")
            return []
    
    def get_user_swipes(self, user_id):
        """Get all swipes made by a user"""
        try:
            response = requests.get(f"{self.database_url}/swipes.json")
            if response.status_code == 200:
                swipes = response.json()
                if not swipes:
                    return []
                
                user_swipes = []
                user_id_str = str(user_id)
                for swipe_id, swipe_data in swipes.items():
                    if swipe_data and swipe_data.get('swiper_id') == user_id_str:
                        user_swipes.append(swipe_data)
                
                return user_swipes
            return []
        except Exception as e:
            print(f"Error getting user swipes: {e}")
            return []

# Create instance
firebase_rest_service = FirebaseRestService()
