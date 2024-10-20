import Streamlit_UI as SUI
import streamlit as st

"""--------------------------------------------------------------------------------------------------------------------------------------------------"""

def add_new_item():
    st.title("Add New Item")
    st.write("This is the Add New Item page.")
    
    item_name = st.text_input("Item Name:")
    item_quantity = st.number_input("Quantity:", min_value=1)
    item_description = st.text_area("Description:")
    
    if st.button("Add Item", key="add_item_btn"):
        st.success(f"Added item: {item_name}, Quantity: {item_quantity}, Description: {item_description}")  # Placeholder for adding logic
    
    if SUI.custom_button("BACK TO HOME", "type--C", "back_home_btn"):
        st.session_state.page = 'home'
        st.experimental_rerun()


"""--------------------------------------------------------------------------------------------------------------------------------------------------"""

def item_identifier():
    st.title("Item Identifier")
    st.write("This is the Item Identifier page.")
    
    item_text = st.text_input("Enter item text for identification:")
    if st.button("Identify Item", key="identify_item_btn"):
        st.success(f"Identified item: {item_text}")  # Placeholder for identification logic
    
    if SUI.custom_button("BACK TO HOME", "type--A", "back_home_btn"):
        st.session_state.page = 'home'
        st.experimental_rerun()

"""--------------------------------------------------------------------------------------------------------------------------------------------------"""



def list_checker():
    st.title("List Checker")
    st.write("This is the List Checker page.")
    
    items = ["Item 1", "Item 2", "Item 3"]  # Example list
    selected_item = st.selectbox("Select an item to check:", items)
    if st.button("Check Item", key="check_item_btn"):
        st.success(f"You checked: {selected_item}")  # Placeholder for checking logic
    
    if SUI.custom_button("BACK TO HOME", "type--B", "back_home_btn"):
        st.session_state.page = 'home'
        st.experimental_rerun()




"""--------------------------------------------------------------------------------------------------------------------------------------------------"""