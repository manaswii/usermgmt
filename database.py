import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create USERS table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS USERS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            address TEXT NOT NULL
        )
    ''')

    # Create admins table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            username TEXT NOT NULL UNIQUE,
            hash TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM USERS WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def verify_admin(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT hash FROM admins WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()

    if result and check_password_hash(result[0], password):
        return True
    return False


def insert_user(first_name, last_name, phone_number, email, address):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO USERS (first_name, last_name, phone_number, email, address)
        VALUES (?, ?, ?, ?, ?)
    ''', (first_name, last_name, phone_number, email, address))
    conn.commit()
    conn.close()


def insert_into_admin(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Hash the password
    hashed_password = generate_password_hash(password)

    try:
        # Insert into admins table
        cursor.execute('''
            INSERT INTO admins (username, hash) VALUES (?, ?)
        ''', (username, hashed_password))

        conn.commit()
        print("Successfully added new admin user")
    except sqlite3.IntegrityError:
        print(f"Error: The username '{username}' already exists.")
    finally:
        conn.close()

def get_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM USERS')
    users = cursor.fetchall()
    conn.close()
    print(users)
    return users

def delete_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM USERS WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

def update_user(user_id, first_name, last_name, phone_number, email, address):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE USERS
        SET first_name = ?, last_name = ?, phone_number = ?, email = ?, address = ?
        WHERE id = ?
    ''', (first_name, last_name, phone_number, email, address, user_id))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
