from app import app, db, User
from werkzeug.security import generate_password_hash
import sys
import os

try:
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        
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
            print("✓ Default admin created - Username: admin, Password: admin123")
        else:
            print("✓ Admin user already exists")
        
        print("\nDatabase initialization completed successfully!")
        print(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')}")
        
except Exception as e:
    print(f"✗ Error initializing database: {str(e)}")
    import traceback
    traceback.print_exc()
    # Don't exit with error in production - let the app handle it
    if not os.environ.get('RENDER'):
        sys.exit(1)
