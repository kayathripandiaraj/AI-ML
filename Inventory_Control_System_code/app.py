import streamlit as st
from db import create_tables, insert_item, get_inventory, update_item, delete_item, register_user, login_user

# Add this function at the top of your file, after the imports
def add_background_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set up Streamlit page configuration
st.set_page_config(page_title="Inventory Control System", layout="wide")

# Add background image
add_background_image("https://www.gespac.be/wp-content/uploads/logiciel-gestion-de-stock-scaled.jpg")

# Create database tables
create_tables()

# Initialize session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# LOGIN FUNCTION
def login():
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

# REGISTER FUNCTION
def register():
    st.subheader("📝 Register")
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        if password == confirm and username:
            try:
                register_user(username, password)
                st.success("Registration successful! Please log in.")
                st.rerun()
            except:
                st.error("Username already exists")
        else:
            st.warning("Passwords must match and not be empty")

# INVENTORY UI
def inventory_ui():
    st.title("📦 Inventory Control System")
    menu = ["Add Item", "View Inventory", "Update Item", "Delete Item", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Item":
        st.subheader("➕ Add New Item")
        item_name = st.text_input("Item Name")
        quantity = st.number_input("Quantity", min_value=0, step=1)
        price = st.number_input("Price", min_value=0.0, format="%.2f")
        if st.button("Add Item"):
            if item_name:
                insert_item(item_name, quantity, price)
                st.success(f"'{item_name}' added!")
            else:
                st.warning("Enter item name")

    elif choice == "View Inventory":
        st.subheader("📋 Current Inventory")
        data = get_inventory()
        if data:
            # Show item number (ID) in the first column
            st.dataframe(
                [{
                    "Item No": row[0],        # Item ID (No)
                    "Item Name": row[1],
                    "Quantity": row[2],
                    "Price": f"₹{row[3]:.2f}",
                    "Last Updated": row[4]
                } for row in data],
                use_container_width=True
            )
        else:
            st.info("No items in inventory yet.")

    elif choice == "Update Item":
        st.subheader("🔁 Update Item")
        data = get_inventory()
        if data:
            item_options = {f"Item No {row[0]}: {row[1]}": row[0] for row in data}
            selected_label = st.selectbox("Select Item", list(item_options.keys()))
            selected_id = item_options[selected_label]
            quantity = st.number_input("New Quantity", min_value=0)
            price = st.number_input("New Price", min_value=0.0)
            if st.button("Update"):
                update_item(selected_id, quantity, price)
                st.success("Item updated")
        else:
            st.warning("No items available")

    elif choice == "Delete Item":
        st.subheader("❌ Delete Item")
        data = get_inventory()
        if data:
            item_options = {f"Item No {row[0]}: {row[1]}": row[0] for row in data}
            selected_label = st.selectbox("Select Item to Delete", list(item_options.keys()))
            selected_id = item_options[selected_label]
            if st.button("Delete"):
                delete_item(selected_id)
                st.warning("Item deleted")
        else:
            st.warning("No items available")

    elif choice == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Logged out")
        st.rerun()

# MAIN FLOW
if not st.session_state.logged_in:
    st.sidebar.title("🔐 Authentication")
    auth_choice = st.sidebar.radio("Choose", ["Login", "Register"])
    if auth_choice == "Login":
        login()
    else:
        register()
else:
    inventory_ui()
