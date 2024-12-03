import sqlite3
from pathlib import Path

def test_connection():
    # Define the database path
    db_path = Path(__file__).parent.parent / 'p01_db' / 'sales_db.sqlite'

    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute a simple query
        cursor.execute("SELECT * FROM Region")
        rows = cursor.fetchall()

        # Print the results
        for row in rows:
            print(row)
        
        conn.close()
    except sqlite3.Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()
