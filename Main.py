# All imports required
import cv2
import sqlite3 as sq
from pyzbar.pyzbar import decode
from bar_code import barcode_number
import streamlit as st
from PIL import Image
import numpy as np

# Connect to SQLite database
conn = sq.connect("Items_list.db")
cursor = conn.cursor()

# Ensure the table exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        price REAL NOT NULL
    );
''')
conn.commit()

def add_item_form(barcode):
    """Display a form to add item details when the barcode is not found"""
    with st.form("item_form", clear_on_submit=False):  # This ensures form stays visible after submission
        name = st.text_input("Enter Item Name")
        price = st.number_input("Enter Item Price", min_value=0.0, step=0.01)
        submit_button = st.form_submit_button("Add Item")

    # Insert the data into the database when the form is submitted
    if submit_button:
        if name and price > 0:
            try:
                # Insert the new item into the database
                cursor.execute("INSERT INTO items (barcode, name, price) VALUES (?, ?, ?)", (barcode, name, price))
                conn.commit()
                st.success(f"Item '{name}' with barcode {barcode} added successfully!")
            except sq.IntegrityError:
                st.error("This barcode already exists. Please use a unique barcode.")
        else:
            st.error("Please fill in all fields and ensure the price is greater than 0.")

def run():
    """Main function to handle barcode detection and database query"""
    barcodes = barcode_number(img)

    if barcodes:
        for barcode in barcodes:
            st.write(f"Barcode found: {barcode}")

            # Query the database to find the item corresponding to the barcode
            cursor.execute("SELECT * FROM items WHERE barcode = ?", (barcode,))
            result = cursor.fetchone()

            if result:
                st.write(f"Item found: ID {result[0]}, Name {result[2]}, Price {result[3]}")
            else:
                st.write("Item not found in the database.")
                add_item_form(barcode)  # Show form to add the missing item

    else:
        st.write("No barcodes found in the image.")

# Load the image of the item
st.title('OCR with Barcode Detection')
input_method = st.radio("Choose input method", ('Capture Image', 'Upload Image'))
uploaded_file = None

if input_method == 'Capture Image':
    uploaded_file = st.camera_input("Capture an image")
else:
    uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    img = np.array(image)
    run()

conn.close()
