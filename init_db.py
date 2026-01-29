from app import app, db, User
from werkzeug.security import generate_password_hash

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
        print("Default admin created - Username: admin, Password: admin123")
    else:
        print("Admin user already exists")
