import sqlite3
import os

def remove_unwanted_profiles():
    """Remove specific profiles from the database"""
    
    if not os.path.exists('roommate_finder.db'):
        print("❌ Database not found. Please run the main app first to create the database.")
        return
    
    conn = sqlite3.connect('roommate_finder.db')
    cursor = conn.cursor()
    
    print("🔍 Current profiles in database:")
    cursor.execute('SELECT user_id, name, age, location FROM user_profiles ORDER BY user_id')
    profiles = cursor.fetchall()
    
    for profile in profiles:
        print(f"   ID {profile[0]}: {profile[1]} ({profile[2]} years old, {profile[3]})")
    
    print(f"\n📊 Total profiles: {len(profiles)}")
    
    # Profiles to remove (you can modify this list)
    profiles_to_remove = [
        # Add profile IDs or names you want to remove
        # Example: 8, 9, 10, 11, 12, 13  # Remove additional profiles
        # Or by name: 'David Chen', 'Emma Rodriguez'
    ]
    
    if not profiles_to_remove:
        print("\n✅ No profiles marked for removal.")
        conn.close()
        return
    
    print(f"\n🗑️  Removing profiles: {profiles_to_remove}")
    
    # Remove profiles by ID
    for profile_id in profiles_to_remove:
        if isinstance(profile_id, int):
            # Remove by user_id
            cursor.execute('DELETE FROM user_profiles WHERE user_id = ?', (profile_id,))
            cursor.execute('DELETE FROM users WHERE id = ?', (profile_id,))
            print(f"✅ Removed profile with ID {profile_id}")
        else:
            # Remove by name
            cursor.execute('DELETE FROM user_profiles WHERE name = ?', (profile_id,))
            print(f"✅ Removed profile: {profile_id}")
    
    conn.commit()
    
    # Show remaining profiles
    cursor.execute('SELECT COUNT(*) FROM user_profiles')
    remaining_count = cursor.fetchone()[0]
    print(f"\n📊 Remaining profiles: {remaining_count}")
    
    conn.close()
    print("✅ Profile removal completed!")

def create_minimal_profiles():
    """Create a minimal set of profiles for testing"""
    
    if not os.path.exists('roommate_finder.db'):
        print("❌ Database not found. Please run the main app first to create the database.")
        return
    
    conn = sqlite3.connect('roommate_finder.db')
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute('DELETE FROM user_profiles')
    cursor.execute('DELETE FROM users WHERE id > 1')  # Keep admin user if exists
    conn.commit()
    
    print("🗑️  Cleared existing profiles")
    
    # Insert minimal profiles
    minimal_users = [
        ('test_user1', 'test1@example.com', 'password123'),
        ('test_user2', 'test2@example.com', 'password123')
    ]
    
    minimal_profiles = [
        (2, 'Test User 1', 25, 600, 'Downtown', 'Test profile for demo purposes.', '["Music", "Movies"]', '["Flexible", "Moderately Social", "Moderately Clean", "Neutral"]'),
        (3, 'Test User 2', 26, 700, 'Midtown', 'Another test profile for demo.', '["Sports", "Fitness"]', '["Early Bird", "Quiet", "Very Clean", "No Pets"]')
    ]
    
    # Insert users
    for username, email, password in minimal_users:
        cursor.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)', 
                      (username, email, 'hashed_password'))
    
    # Insert profiles
    for profile_data in minimal_profiles:
        cursor.execute('''INSERT INTO user_profiles 
                         (user_id, name, age, budget, location, bio, interests, lifestyle_preferences)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', profile_data)
    
    conn.commit()
    conn.close()
    
    print("✅ Created minimal test profiles")

if __name__ == "__main__":
    print("🔧 RoomieMatch - Profile Management")
    print("=" * 40)
    
    print("\n1. Remove unwanted profiles")
    print("2. Create minimal test profiles")
    print("3. Show current profiles")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        remove_unwanted_profiles()
    elif choice == '2':
        create_minimal_profiles()
    elif choice == '3':
        # Show profiles
        if os.path.exists('roommate_finder.db'):
            conn = sqlite3.connect('roommate_finder.db')
            cursor = conn.cursor()
            cursor.execute('SELECT user_id, name, age, location FROM user_profiles ORDER BY user_id')
            profiles = cursor.fetchall()
            
            print("\n📋 Current profiles:")
            for profile in profiles:
                print(f"   ID {profile[0]}: {profile[1]} ({profile[2]} years old, {profile[3]})")
            
            conn.close()
        else:
            print("❌ Database not found.")
    else:
        print("❌ Invalid choice.")
