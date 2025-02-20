import sqlite3 as sq

# Connect to the SQLite database (create it if it doesn't exist)
conn = sq.connect("Items_list.db")
cursor = conn.cursor()

# Create the 'items' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barcode TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    price REAL NOT NULL
);
''')
items = [
    ('5032722302075', 'Item 1', 10.99),
    ('1234567890123', 'Item 2', 15.49),
    ('9876543210987', 'Item 3', 20.00)
]

# Insert data
cursor.executemany("INSERT OR IGNORE INTO items (barcode, name, price) VALUES (?, ?, ?)", items)


# Commit changes and close the connection
conn.commit()
conn.close()
