from flask import Flask
from database import init_db

app = Flask(__name__)

# Set the secret key to a random bytes string or a hardcoded string
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

# Initialize the database
init_db()

# Import routes
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
