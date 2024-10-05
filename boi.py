import sqlite3 as sq

# Connect to the SQLite database
conn = sq.connect("Items_list.db")  # Ensure you're using the correct path and name
cursor = conn.cursor()

# Create the 'items' table if it does not exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barcode TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    price REAL NOT NULL
);
''')

# Commit changes and close the connection
conn.commit()
conn.close()
