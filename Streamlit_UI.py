import streamlit as st

#--------------------------------------------------------------------------------------------------------------------------------------------------

def add_new_item():
    st.title("Add New Item")
    st.write("This is the Add New Item page.")

    item_name = st.text_input("Item Name:")
    item_quantity = st.number_input("Quantity:", min_value=1)
    item_description = st.text_area("Description:")

    if st.button("Add Item", key="add_item_btn"):
        st.success(f"Added item: {item_name}, Quantity: {item_quantity}, Description: {item_description}")
        # Placeholder for adding logic

    if st.button("BACK TO HOME", key="back_home_btn"):
        st.session_state.page = 'home'

#--------------------------------------------------------------------------------------------------------------------------------------------------

def item_identifier():
    st.title("Item Identifier")
    st.write("This is the Item Identifier page.")

    item_text = st.text_input("Enter item text for identification:")
    if st.button("Identify Item", key="identify_item_btn"):
        st.success(f"Identified item: {item_text}")
        # Placeholder for identification logic

    if st.button("BACK TO HOME", key="back_home_btn"):
        st.session_state.page = 'home'

#--------------------------------------------------------------------------------------------------------------------------------------------------

def list_checker():
    st.title("List Checker")
    st.write("This is the List Checker page.")

    items = ["Item 1", "Item 2", "Item 3"]  # Example list
    selected_item = st.selectbox("Select an item to check:", items)
    if st.button("Check Item", key="check_item_btn"):
        st.success(f"You checked: {selected_item}")
        # Placeholder for checking logic

    if st.button("BACK TO HOME", key="back_home_btn"):
        st.session_state.page = 'home'

#--------------------------------------------------------------------------------------------------------------------------------------------------

def show_home():
    st.title("🔍 Inventory Management System")
    st.header("Welcome to the Inventory Management System")
    st.write("Use the sidebar to navigate between different functions.")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Item Identifier"):
            st.session_state.page = 'item_identifier'

    with col2:
        if st.button("List Checker"):
            st.session_state.page = 'list_checker'

    with col3:
        if st.button("Add New Item"):
            st.session_state.page = 'add_new_item'

#--------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="Inventory Management System", layout="wide")

    # Initialize session state if not already set
    if 'page' not in st.session_state:
        st.session_state.page = 'home'  # Default page

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ['Home', 'Item Identifier', 'List Checker', 'Add New Item'])

    # Update session state based on sidebar selection
    st.session_state.page = page.lower().replace(' ', '_')

    # Main content based on the current page
    if st.session_state.page == 'home':
        show_home()
    elif st.session_state.page == 'item_identifier':
        item_identifier()
    elif st.session_state.page == 'list_checker':
        list_checker()
    elif st.session_state.page == 'add_new_item':
        add_new_item()

if __name__ == "__main__":
    main()
