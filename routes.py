from flask import render_template, request, redirect, url_for, flash, session
from app import app
from database import get_users, delete_user, update_user, insert_user, get_user_by_id, verify_admin
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You need to log in first.', 'warning')
            return redirect(url_for('login'))  # Redirect to login if not logged in
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verify admin credentials (you should implement this function)
        if verify_admin(username, password):
            session['username'] = username  # Create a session
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to home after login
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('login.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.pop('username', None)  # Remove the session
    flash('You have been logged out.', 'success')  # Flash message only on logout
    return redirect(url_for('login'))  # Redirect to login page




@app.route('/')
@login_required
def home():
    users = get_users()  # Fetch all users from the database
    return render_template('home.html', users=users)  # Pass users to the template


@app.route('/manage-users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if request.method == 'POST':
        if 'delete' in request.form:
            user_id = request.form['user_id']
            delete_user(user_id)
            flash('User deleted successfully!', 'success')
        elif 'edit' in request.form:
            # You can handle editing here if you wish to use a modal or another route.
            pass

    users = get_users()
    return render_template('manage_users.html', users=users)

@app.route('/add-user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        address = request.form.get('address')

        # Server-side validation
        errors = []
        if not first_name:
            errors.append("First name is required.")
        if not last_name:
            errors.append("Last name is required.")
        if not phone_number:
            errors.append("Phone number is required.")
        if not email:
            errors.append("Email is required.")
        if not address:
            errors.append("Address is required.")

        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('add_user'))
        
        insert_user(first_name, last_name, phone_number, email, address)  # Insert new user
        flash('User added successfully!', 'success')  # Flash message on success
        return redirect(url_for('manage_users'))  # Redirect to manage users page

    return render_template('add_user.html')  # Render the add user form

@app.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = get_user_by_id(user_id)  # Fetch user details for the given user_id

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        address = request.form['address']
        errors = []
        
        if not first_name:
            errors.append("First name is required.")
        if not last_name:
            errors.append("Last name is required.")
        if not phone_number:
            errors.append("Phone number is required.")
        if not email:
            errors.append("Email is required.")
        if not address:
            errors.append("Address is required.")

        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('edit_user', user_id=user_id))  # Redirect back to edit user page if there are errors
        
        update_user(user_id, first_name, last_name, phone_number, email, address)  # Update user
        flash('User updated successfully!', 'success')  # Flash message on success
        return redirect(url_for('manage_users'))  # Redirect to manage users page

    return render_template('edit_user.html', user=user)  # Render edit user form
