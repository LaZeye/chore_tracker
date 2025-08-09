from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from pymongo import MongoClient
from bson.objectid import ObjectId
import os


################################################################# Flask Init
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with secrets.token_hex(16)


################################################################# Mongo-DB
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://192.168.0.247:27017/chore_tracker')
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client['chore_tracker']


################################################################# Authentication
class User(UserMixin):
    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in.', 'error')
                return redirect(url_for('login'))
            if current_user.role not in roles:
                flash('Unauthorized access.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@login_manager.user_loader
def load_user(user_id):
    try:
        user = db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            return User(str(user['_id']), user['name'], user['role'])
    except:
        return None
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']
        user = db.users.find_one({'name': {'$regex': '^' + username + '$', '$options': 'i'}})
        if user and check_password_hash(user['password'], password):
            login_user(User(str(user['_id']), user['name'], user['role']))
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        if new_password:
            db.users.update_one(
                {'_id': ObjectId(current_user.id)},
                {'$set': {'password': generate_password_hash(new_password)}}
            )
            flash('Password changed successfully.', 'success')
            return redirect(url_for('dashboard'))
        flash('Please enter a new password.', 'error')
    return render_template('change_password.html')


################################################################# Routes 
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/wallet')
@login_required
def wallet():
    return render_template('wallet.html', user=current_user)

@app.route('/post_chore', methods=['POST'])
@login_required
@roles_required('Parent')
def post_chore():
    flash('Chore posting not implemented yet.', 'error')
    return redirect(url_for('dashboard'))


################################################################# Server
if __name__ == '__main__':
    try:
        client.server_info()
        print("Connected to MongoDB")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
    app.run(debug=True, host='0.0.0.0', port=5000)