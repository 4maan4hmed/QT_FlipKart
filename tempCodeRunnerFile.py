import streamlit as st
import time

def main():
    st.set_page_config(page_title="Inventory Management System", layout="wide")

    if 'page' not in st.session_state:
        st.session_state.page = 'home'  # Default page

    # Main content based on the current page
    if st.session_state.page == 'home':
        show_home()
    elif st.session_state.page == 'item_identifier':
        item_identifier()
    elif st.session_state.page == 'list_checker':
        list_checker()
    elif st.session_state.page == 'add_new_item':
        add_new_item()

def show_home():
    st.title("🔍 Inventory Management System")
    st.header("Choose an option:")
    
    col1, col2, col3 = st.columns(3)  # Create three columns for buttons
    with col1:
        if st.button("Item Identifier"):
            navigate_to('item_identifier')
    with col2:
        if st.button("List Checker"):
            navigate_to('list_checker')
    with col3:
        if st.button("Add New Item"):
            navigate_to('add_new_item')

def navigate_to(page):
    """ Simulate navigation with a loading effect. """
    with st.spinner("Navigating..."):
        time.sleep(0.5)  # Simulate loading time
        st.session_state.page = page  # Update the current page

def item_identifier():
    st.title("Item Identifier")
    st.write("This is the Item Identifier page.")
    
    # Simulating some input functionality
    item_text = st.text_input("Enter item text for identification:")
    if st.button("Identify Item"):
        st.success(f"Identified item: {item_text}")  # Placeholder for identification logic

    # Back button
    if st.button("Back"):
        st.session_state.page = 'home'

def list_checker():
    st.title("List Checker")
    st.write("This is the List Checker page.")
    
    items = ["Item 1", "Item 2", "Item 3"]  # Example list
    selected_item = st.selectbox("Select an item to check:", items)
    if st.button("Check Item"):
        st.success(f"You checked: {selected_item}")  # Placeholder for checking logic

    # Back button
    if st.button("Back"):
        st.session_state.page = 'home'

def add_new_item():
    st.title("Add New Item")
    st.write("This is the Add New Item page.")
    
    item_name = st.text_input("Item Name:")
    item_quantity = st.number_input("Quantity:", min_value=1)
    item_description = st.text_area("Description:")
    
    if st.button("Add Item"):
        st.success(f"Added item: {item_name}, Quantity: {item_quantity}, Description: {item_description}")  # Placeholder for adding logic

    # Back button
    if st.button("Back"):
        st.session_state.page = 'home'

if __name__ == "__main__":
    main()
    