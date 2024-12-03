import sqlite3

def export_db_to_sqlite_file(db_path: str, sql_file_path: str):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    with open(sql_file_path, 'w') as sql_file:
        # Export the schema (table creation statements)
        for line in cursor.iterdump():
            sql_file.write(f"{line}\n")

    connection.close()

# Usage
db_path = 'p01_db/sales_db.sqlite'  # Path to your SQLite database file
sql_file_path = 'sales_db_export.sql'  # Path where you want to save the SQL file
export_db_to_sqlite_file(db_path, sql_file_path)
