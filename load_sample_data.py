import sqlite3
import os

def load_sql_data():
    """Load sample data from SQL file into the database"""
    
    # Check if database exists
    if not os.path.exists('roommate_finder.db'):
        print("Database not found. Please run the main app first to create the database.")
        return
    
    # Connect to database
    conn = sqlite3.connect('roommate_finder.db')
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute('SELECT COUNT(*) as count FROM users')
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"Database already contains {count} users. Skipping data insertion.")
        conn.close()
        return
    
    # Read and execute SQL file
    try:
        with open('sample_data.sql', 'r') as file:
            sql_script = file.read()
        
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement.startswith('INSERT'):
                cursor.execute(statement)
        
        conn.commit()
        print("Sample data loaded successfully!")
        
    except FileNotFoundError:
        print("sample_data.sql file not found.")
    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    load_sql_data()
