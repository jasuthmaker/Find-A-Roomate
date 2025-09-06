import sqlite3
import os
from werkzeug.security import generate_password_hash

def direct_sql_execution():
    """Demonstrate direct SQL execution for loading sample data"""
    
    print("=== Direct SQL Execution Demo ===\n")
    
    # Check if database exists
    if not os.path.exists('roommate_finder.db'):
        print("❌ Database not found. Please run the main app first to create the database.")
        return
    
    # Connect to database
    conn = sqlite3.connect('roommate_finder.db')
    cursor = conn.cursor()
    
    print("✅ Connected to roommate_finder.db")
    
    # Check current data
    cursor.execute('SELECT COUNT(*) as count FROM users')
    user_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) as count FROM user_profiles')
    profile_count = cursor.fetchone()[0]
    
    print(f"📊 Current data: {user_count} users, {profile_count} profiles")
    
    if user_count > 0:
        print("⚠️  Database already contains data. Skipping insertion.")
        conn.close()
        return
    
    print("\n🚀 Executing SQL INSERT statements...")
    
    # Method 1: Direct SQL execution with individual statements
    print("\n--- Method 1: Individual INSERT statements ---")
    
    # Insert users one by one
    users_sql = [
        "INSERT INTO users (username, email, password_hash) VALUES ('alex_smith', 'alex@example.com', ?)",
        "INSERT INTO users (username, email, password_hash) VALUES ('maya_johnson', 'maya@example.com', ?)",
        "INSERT INTO users (username, email, password_hash) VALUES ('sam_wilson', 'sam@example.com', ?)",
        "INSERT INTO users (username, email, password_hash) VALUES ('jessica_brown', 'jessica@example.com', ?)",
        "INSERT INTO users (username, email, password_hash) VALUES ('mike_davis', 'mike@example.com', ?)",
        "INSERT INTO users (username, email, password_hash) VALUES ('sarah_miller', 'sarah@example.com', ?)"
    ]
    
    password_hash = generate_password_hash('password123')
    
    for sql in users_sql:
        cursor.execute(sql, (password_hash,))
        print(f"✅ Executed: {sql[:50]}...")
    
    # Insert profiles
    profiles_sql = [
        """INSERT INTO user_profiles (user_id, name, age, budget, location, bio, interests, lifestyle_preferences) 
           VALUES (2, 'Alex Smith', 22, 600, 'Downtown', 'Love music, gaming, and cooking!', '["Music", "Gaming", "Cooking", "Movies"]', '["Night Owl", "Very Social", "Moderately Clean", "Love Pets"]')""",
        
        """INSERT INTO user_profiles (user_id, name, age, budget, location, bio, interests, lifestyle_preferences) 
           VALUES (3, 'Maya Johnson', 25, 750, 'Midtown', 'Fitness enthusiast and nature lover.', '["Fitness", "Nature", "Reading", "Photography"]', '["Early Bird", "Quiet", "Very Clean", "Neutral"]')""",
        
        """INSERT INTO user_profiles (user_id, name, age, budget, location, bio, interests, lifestyle_preferences) 
           VALUES (4, 'Sam Wilson', 23, 650, 'Uptown', 'Artist and photographer.', '["Art", "Photography", "Travel", "Cooking"]', '["Flexible", "Moderately Social", "Moderately Clean", "Love Pets"]')""",
        
        """INSERT INTO user_profiles (user_id, name, age, budget, location, bio, interests, lifestyle_preferences) 
           VALUES (5, 'Jessica Brown', 24, 700, 'Downtown', 'Tech professional who loves coding.', '["Technology", "Gaming", "Movies", "Music"]', '["Night Owl", "Moderately Social", "Moderately Clean", "Neutral"]')""",
        
        """INSERT INTO user_profiles (user_id, name, age, budget, location, bio, interests, lifestyle_preferences) 
           VALUES (6, 'Mike Davis', 26, 800, 'Midtown', 'Sports fanatic and outdoor enthusiast.', '["Sports", "Fitness", "Nature", "Travel"]', '["Early Bird", "Very Social", "Very Clean", "No Pets"]')""",
        
        """INSERT INTO user_profiles (user_id, name, age, budget, location, bio, interests, lifestyle_preferences) 
           VALUES (7, 'Sarah Miller', 21, 550, 'Uptown', 'Student studying art history.', '["Art", "Reading", "Movies", "Nature"]', '["Flexible", "Quiet", "Very Clean", "Neutral"]')"""
    ]
    
    for sql in profiles_sql:
        cursor.execute(sql)
        print(f"✅ Executed: Profile INSERT...")
    
    # Commit all changes
    conn.commit()
    print("\n💾 All changes committed to database")
    
    # Verify data
    cursor.execute('SELECT COUNT(*) as count FROM users')
    new_user_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) as count FROM user_profiles')
    new_profile_count = cursor.fetchone()[0]
    
    print(f"\n📊 Final data: {new_user_count} users, {new_profile_count} profiles")
    
    # Show sample data
    print("\n👥 Sample users:")
    cursor.execute('SELECT username, email FROM users LIMIT 3')
    for row in cursor.fetchall():
        print(f"   - {row[0]} ({row[1]})")
    
    print("\n👤 Sample profiles:")
    cursor.execute('SELECT name, age, location FROM user_profiles LIMIT 3')
    for row in cursor.fetchall():
        print(f"   - {row[0]}, {row[1]} years old, {row[2]}")
    
    conn.close()
    print("\n✅ Direct SQL execution completed successfully!")

def execute_sql_file():
    """Execute SQL statements from a file"""
    
    print("\n=== Executing SQL from File ===\n")
    
    if not os.path.exists('sample_data.sql'):
        print("❌ sample_data.sql file not found")
        return
    
    conn = sqlite3.connect('roommate_finder.db')
    cursor = conn.cursor()
    
    try:
        with open('sample_data.sql', 'r') as file:
            sql_content = file.read()
        
        print("📄 Reading sample_data.sql...")
        
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
        
        print(f"🔍 Found {len(statements)} SQL statements")
        
        for i, statement in enumerate(statements, 1):
            if statement.startswith('INSERT'):
                cursor.execute(statement)
                print(f"✅ Executed statement {i}: {statement[:50]}...")
        
        conn.commit()
        print("\n💾 All SQL statements executed and committed!")
        
    except Exception as e:
        print(f"❌ Error executing SQL file: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔧 RoomieMatch - Direct SQL Execution Demo")
    print("=" * 50)
    
    # Method 1: Direct SQL execution
    direct_sql_execution()
    
    # Method 2: Execute from SQL file
    execute_sql_file()
    
    print("\n🎉 Demo completed! You can now use these methods to load data directly via SQL.")
