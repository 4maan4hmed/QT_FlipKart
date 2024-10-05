import cv2
import sqlite3 as sq
from pyzbar.pyzbar import decode
from bar_code import barcode_number

# Load the image of the item
img = cv2.imread('C:/Users/amaan/OneDrive/Desktop/VIT/Semester 5/Flipkart Grid/OCR/Images/jarr.jpg')

# Connect to the SQLite database
conn = sq.connect("Items_list.db")  # Use .db to indicate it is a database file
cursor = conn.cursor()

# Extract barcode(s) from the image
barcodes = barcode_number(img)

if barcodes:
    for barcode in barcodes:
        print(f"Barcode found: {barcode}")

        # Query the database to find the item corresponding to the barcode
        cursor.execute("SELECT * FROM items WHERE barcode = ?", (barcode,))
        result = cursor.fetchone()  # Fetch the first matching row

        if result:
            print("Item found in database:")
            print(f"ID: {result[0]}, Name: {result[1]}, Price: {result[2]}")  # Adjust based on your table structure
        else:
            print("Item not found in database.")
else:
    print("No barcodes found in the image.")


# Close the database connection
conn.close()
