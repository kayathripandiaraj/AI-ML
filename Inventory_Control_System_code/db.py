import sqlite3
from datetime import datetime

# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect("inventory.db")

# Function to create tables if they don't exist
def create_tables():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            quantity INTEGER,
            price REAL,
            last_updated TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to register a new user
def register_user(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Function to authenticate a user during login
def login_user(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = cur.fetchone()
    conn.close()
    return result is not None

# Function to insert a new item into the inventory
def insert_item(name, quantity, price):
    conn = connect_db()
    cur = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("INSERT INTO inventory (name, quantity, price, last_updated) VALUES (?, ?, ?, ?)", (name, quantity, price, now))
    conn.commit()
    conn.close()

# Function to get the current inventory
def get_inventory():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory")
    data = cur.fetchall()
    conn.close()
    return data

# Function to update an existing item's quantity and price
def update_item(item_id, quantity, price):
    conn = connect_db()
    cur = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("UPDATE inventory SET quantity=?, price=?, last_updated=? WHERE id=?", (quantity, price, now, item_id))
    conn.commit()
    conn.close()

# Function to delete an item from the inventory
def delete_item(item_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM inventory WHERE id=?", (item_id,))
    conn.commit()
    conn.close()
