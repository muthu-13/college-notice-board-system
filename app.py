from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-12345')

# Database configuration - use PostgreSQL in production, SQLite in development
database_url = os.environ.get('DATABASE_URL')
if database_url:
    # Render uses postgres:// but SQLAlchemy needs postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print(f"Using PostgreSQL database")
else:
    # Use SQLite for local development
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "college_notices.db")}'
    print(f"Using SQLite database")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

db = SQLAlchemy(app)

# Initialize database tables
def init_database():
    """Initialize database and create default admin user"""
    try:
        with app.app_context():
            db.create_all()
            # Create default admin if doesn't exist
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@college.edu',
                    password=generate_password_hash('admin123'),
                    role='admin',
                    department='Administration'
                )
                db.session.add(admin)
                db.session.commit()
                print("✓ Default admin created")
    except Exception as e:
        print(f"Database initialization error: {e}")

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'teacher', 'student'
    department = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notices = db.relationship('Notice', backref='author', lazy=True, cascade='all, delete-orphan')

class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # 'Academic', 'Event', 'Exam', 'General'
    department = db.Column(db.String(50))
    priority = db.Column(db.String(20), default='Normal')  # 'High', 'Medium', 'Normal'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

# Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# Initialize database on first request
@app.before_request
def before_first_request():
    if not hasattr(app, 'db_initialized'):
        try:
            db.create_all()
            app.db_initialized = True
        except Exception as e:
            print(f"Database error: {e}")

# Routes
@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error: {e}")
        return f"<h1>Welcome to College Notice Board</h1><p><a href='/login'>Login</a> | <a href='/register'>Register</a></p>", 200

@app.route('/home')
@login_required
def home():
    user = User.query.get(session['user_id'])
    
    # Filter notices based on user's department or show all if admin
    if user.role == 'admin':
        notices = Notice.query.filter_by(is_active=True).order_by(Notice.created_at.desc()).all()
    elif user.department:
        notices = Notice.query.filter_by(is_active=True).filter(
            (Notice.department == user.department) | (Notice.department == 'All')
        ).order_by(Notice.created_at.desc()).all()
    else:
        notices = Notice.query.filter_by(is_active=True, department='All').order_by(Notice.created_at.desc()).all()
    
    return render_template('home.html', notices=notices, user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'student')
        department = request.form.get('department')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=role,
            department=department
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/notice/create', methods=['GET', 'POST'])
@login_required
def create_notice():
    user = User.query.get(session['user_id'])
    
    # Only admin and teachers can create notices
    if user.role not in ['admin', 'teacher']:
        flash('Only teachers and admins can create notices.', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        department = request.form.get('department')
        priority = request.form.get('priority', 'Normal')
        
        if not title or not content:
            flash('Title and content are required.', 'danger')
            return redirect(url_for('create_notice'))
        
        notice = Notice(
            title=title,
            content=content,
            category=category,
            department=department,
            priority=priority,
            user_id=user.id
        )
        
        db.session.add(notice)
        db.session.commit()
        
        flash('Notice created successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('create_notice.html', user=user)

@app.route('/notice/<int:notice_id>')
@login_required
def view_notice(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    user = User.query.get(session['user_id'])
    return render_template('view_notice.html', notice=notice, user=user)

@app.route('/notice/edit/<int:notice_id>', methods=['GET', 'POST'])
@login_required
def edit_notice(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    user = User.query.get(session['user_id'])
    
    # Only the author or admin can edit
    if notice.user_id != user.id and user.role != 'admin':
        flash('You do not have permission to edit this notice.', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        notice.title = request.form.get('title')
        notice.content = request.form.get('content')
        notice.category = request.form.get('category')
        notice.department = request.form.get('department')
        notice.priority = request.form.get('priority')
        notice.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Notice updated successfully!', 'success')
        return redirect(url_for('view_notice', notice_id=notice.id))
    
    return render_template('edit_notice.html', notice=notice, user=user)

@app.route('/notice/delete/<int:notice_id>')
@login_required
def delete_notice(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    user = User.query.get(session['user_id'])
    
    # Only the author or admin can delete
    if notice.user_id != user.id and user.role != 'admin':
        flash('You do not have permission to delete this notice.', 'danger')
        return redirect(url_for('home'))
    
    db.session.delete(notice)
    db.session.commit()
    flash('Notice deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/my-notices')
@login_required
def my_notices():
    user = User.query.get(session['user_id'])
    notices = Notice.query.filter_by(user_id=user.id).order_by(Notice.created_at.desc()).all()
    return render_template('my_notices.html', notices=notices, user=user)

@app.route('/users')
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/public-notices')
def public_notices():
    notices = Notice.query.filter_by(is_active=True).order_by(Notice.created_at.desc()).all()
    return render_template('public_notices.html', notices=notices)

@app.route('/public-notice/<int:notice_id>')
def view_public_notice(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    return render_template('view_public_notice.html', notice=notice)

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default admin if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@college.edu',
                password=generate_password_hash('admin123'),
                role='admin',
                department='Administration'
            )
            db.session.add(admin)
            db.session.commit()
            print("Default admin created - Username: admin, Password: admin123")

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
