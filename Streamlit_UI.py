import streamlit as st

def main():
    st.set_page_config(page_title="Inventory Management System", layout="wide")
    
    if 'page' not in st.session_state:
        st.session_state.page = 'home'  # Default page
    
    # Apply custom CSS
    apply_custom_css()
    
    # Main content based on the current page
    if st.session_state.page == 'home':
        show_home()
    elif st.session_state.page == 'item_identifier':
        item_identifier()
    elif st.session_state.page == 'list_checker':
        list_checker()
    elif st.session_state.page == 'add_new_item':
        add_new_item()

def apply_custom_css():
    st.markdown("""
    <style>
    .type--A{
      --line_color: #78909C;
      --back_color: #ECEFF1;
    }
    .type--B{
      --line_color: #5D4037;
      --back_color: #EFEBE9;
    }
    .type--C{
      --line_color: #455A64;
      --back_color: #ECEFF1;
    }
    .button{
        position: relative;
        z-index: 0;
        width: 240px;
        height: 56px;
        text-decoration: none;
        font-size: 14px; 
        font-weight: bold;
        color: var(--line_color);
        letter-spacing: 2px;
        transition: all .3s ease;
    }
    .button__text{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
    }
    .button::before,
    .button::after,
    .button__text::before,
    .button__text::after{
        content: '';
        position: absolute;
        height: 3px;
        border-radius: 2px;
        background: var(--line_color);
        transition: all .5s ease;
    }
    .button::before{
        top: 0;
        left: 54px;
        width: calc( 100% - 56px * 2 - 16px );
    }
    .button::after{
        top: 0;
        right: 54px;
        width: 8px;
    }
    .button__text::before{
        bottom: 0;
        right: 54px;
        width: calc( 100% - 56px * 2 - 16px );
    }
    .button__text::after{
        bottom: 0;
        left: 54px;
        width: 8px;
    }
    .button__line{
        position: absolute;
        top: 0;
        width: 56px;
        height: 100%;
        overflow: hidden;
    }
    .button__line::before{
        content: '';
        position: absolute;
        top: 0;
        width: 150%;
        height: 100%;
        box-sizing: border-box;
        border-radius: 300px;
        border: solid 3px var(--line_color);
    }
    .button__line:nth-child(1),
    .button__line:nth-child(1)::before{
        left: 0;
    }
    .button__line:nth-child(2),
    .button__line:nth-child(2)::before{
        right: 0;
    }
    .button:hover{
        letter-spacing: 6px;
    }
    .button:hover::before,
    .button:hover .button__text::before{
        width: 8px;
    }
    .button:hover::after,
    .button:hover .button__text::after{
        width: calc( 100% - 56px * 2 - 16px );
    }
    .button__drow1,
    .button__drow2{
        position: absolute;
        z-index: -1;
        border-radius: 16px;
        transform-origin: 16px 16px;
    }
    .button__drow1{
        top: -16px;
        left: 40px;
        width: 32px;
        height: 0;
        transform: rotate( 30deg );
    }
    .button__drow2{
        top: 44px;
        left: 77px;
        width: 32px;
        height: 0;
        transform: rotate(-127deg );
    }
    .button__drow1::before,
    .button__drow1::after,
    .button__drow2::before,
    .button__drow2::after{
        content: '';
        position: absolute;
    }
    .button__drow1::before{
        bottom: 0;
        left: 0;
        width: 0;
        height: 32px;
        border-radius: 16px;
        transform-origin: 16px 16px;
        transform: rotate( -60deg );
    }
    .button__drow1::after{
        top: -10px;
        left: 45px;
        width: 0;
        height: 32px;
        border-radius: 16px;
        transform-origin: 16px 16px;
        transform: rotate( 69deg );
    }
    .button__drow2::before{
        bottom: 0;
        left: 0;
        width: 0;
        height: 32px;
        border-radius: 16px;
        transform-origin: 16px 16px;
        transform: rotate( -146deg );
    }
    .button__drow2::after{
        bottom: 26px;
        left: -40px;
        width: 0;
        height: 32px;
        border-radius: 16px;
        transform-origin: 16px 16px;
        transform: rotate( -262deg );
    }
    .button__drow1,
    .button__drow1::before,
    .button__drow1::after,
    .button__drow2,
    .button__drow2::before,
    .button__drow2::after{
        background: var( --back_color );
    }
    .button:hover .button__drow1{
        animation: drow1 ease-in .06s;
        animation-fill-mode: forwards;
    }
    .button:hover .button__drow1::before{
        animation: drow2 linear .08s .06s;
        animation-fill-mode: forwards;
    }
    .button:hover .button__drow1::after{
        animation: drow3 linear .03s .14s;
        animation-fill-mode: forwards;
    }
    .button:hover .button__drow2{
        animation: drow4 linear .06s .2s;
        animation-fill-mode: forwards;
    }
    .button:hover .button__drow2::before{
        animation: drow3 linear .03s .26s;
        animation-fill-mode: forwards;
    }
    .button:hover .button__drow2::after{
        animation: drow5 linear .06s .32s;
        animation-fill-mode: forwards;
    }
    @keyframes drow1{
        0%   { height: 0; }
        100% { height: 100px; }
    }
    @keyframes drow2{
        0%   { width: 0; opacity: 0;}
        10%  { opacity: 0;}
        11%  { opacity: 1;}
        100% { width: 120px; }
    }
    @keyframes drow3{
        0%   { width: 0; }
        100% { width: 80px; }
    }
    @keyframes drow4{
        0%   { height: 0; }
        100% { height: 120px; }
    }
    @keyframes drow5{
        0%   { width: 0; }
        100% { width: 124px; }
    }
    .container{
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .button:not(:last-child){
      margin-bottom: 64px;
    }
    </style>
    """, unsafe_allow_html=True)

def custom_button(text, button_type, key):
    button_html = f"""
    <div class="container">
        <a href="#" class="button {button_type}" onclick="buttonClicked('{key}'); return false;">
            <div class="button__line"></div>
            <div class="button__line"></div>
            <span class="button__text">{text}</span>
            <div class="button__drow1"></div>
            <div class="button__drow2"></div>
        </a>
    </div>
    """
    st.markdown(button_html, unsafe_allow_html=True)
    
    # JavaScript to handle button clicks
    st.markdown("""
    <script>
    function buttonClicked(key) {
        window.parent.postMessage({
            type: "streamlit:setComponentValue",
            key: key,
            value: true
        }, "*");
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Return True if the button was clicked
    return st.session_state.get(key, False)

def show_home():
    st.title("🔍 Inventory Management System")
    st.header("Choose an option:")
    
    if custom_button("ITEM IDENTIFIER", "type--A", "item_identifier_btn"):
        st.session_state.page = 'item_identifier'
        st.experimental_rerun()
    
    if custom_button("LIST CHECKER", "type--B", "list_checker_btn"):
        st.session_state.page = 'list_checker'
        st.experimental_rerun()
    
    if custom_button("ADD NEW ITEM", "type--C", "add_new_item_btn"):
        st.session_state.page = 'add_new_item'
        st.experimental_rerun()

def item_identifier():
    st.title("Item Identifier")
    st.write("This is the Item Identifier page.")
    
    item_text = st.text_input("Enter item text for identification:")
    if st.button("Identify Item", key="identify_item_btn"):
        st.success(f"Identified item: {item_text}")  # Placeholder for identification logic
    
    if custom_button("BACK TO HOME", "type--A", "back_home_btn"):
        st.session_state.page = 'home'
        st.experimental_rerun()

def list_checker():
    st.title("List Checker")
    st.write("This is the List Checker page.")
    
    items = ["Item 1", "Item 2", "Item 3"]  # Example list
    selected_item = st.selectbox("Select an item to check:", items)
    if st.button("Check Item", key="check_item_btn"):
        st.success(f"You checked: {selected_item}")  # Placeholder for checking logic
    
    if custom_button("BACK TO HOME", "type--B", "back_home_btn"):
        st.session_state.page = 'home'
        st.experimental_rerun()

def add_new_item():
    st.title("Add New Item")
    st.write("This is the Add New Item page.")
    
    item_name = st.text_input("Item Name:")
    item_quantity = st.number_input("Quantity:", min_value=1)
    item_description = st.text_area("Description:")
    
    if st.button("Add Item", key="add_item_btn"):
        st.success(f"Added item: {item_name}, Quantity: {item_quantity}, Description: {item_description}")  # Placeholder for adding logic
    
    if custom_button("BACK TO HOME", "type--C", "back_home_btn"):
        st.session_state.page = 'home'
        st.experimental_rerun()

if __name__ == "__main__":
    main()