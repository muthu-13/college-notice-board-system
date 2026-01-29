# College Notice Board System

A comprehensive web-based notice board system built with Flask for managing college notices and announcements.

## Features

### User Roles
- **Admin**: Full system access, user management, and notice management
- **Teacher**: Can create, edit, and delete their own notices
- **Student**: Can view notices relevant to their department

### Key Functionalities
- ✅ User Authentication (Login/Register/Logout)
- ✅ Role-based Access Control
- ✅ Create, Read, Update, Delete (CRUD) Notices
- ✅ Department-wise Notice Filtering
- ✅ Priority-based Notices (High, Medium, Normal)
- ✅ Category-based Organization (Academic, Event, Exam, Holiday, Sports, General)
- ✅ User Management Dashboard (Admin Only)
- ✅ Responsive Design
- ✅ Modern UI with Beautiful Gradient Effects

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Icons**: Font Awesome 6
- **Security**: Werkzeug Password Hashing

## Project Structure

```
college_notice_board/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── static/
│   └── css/
│       └── style.css              # Custom CSS styles
│
├── templates/
│   ├── base.html                  # Base template
│   ├── index.html                 # Landing page
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── home.html                  # Dashboard/Notice board
│   ├── create_notice.html         # Create notice form
│   ├── edit_notice.html           # Edit notice form
│   ├── view_notice.html           # View notice details
│   ├── my_notices.html            # User's notices
│   └── users.html                 # User management (Admin)
│
└── instance/
    └── college_notices.db         # SQLite database (auto-created)
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd d:\Flask\venv\Scripts\college_notice_board
```

### Step 2: Create Virtual Environment (if not already in one)
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run the Application
```bash
python app.py
```

The application will:
- Create the database automatically
- Create a default admin account
- Start the development server at `http://127.0.0.1:5000`

### Step 6: Access the Application
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## Default Login Credentials

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`

**Note**: Change the admin password after first login in a production environment!

## Usage Guide

### For Students:
1. Register with your college email and select "Student" role
2. Choose your department
3. Login and view notices relevant to your department
4. View detailed information about each notice

### For Teachers:
1. Register with "Teacher" role
2. Login and access the notice board
3. Click "Create New Notice" to post announcements
4. Select category, priority, and target department
5. Manage your own notices (Edit/Delete)

### For Admins:
1. Login with admin credentials
2. Access all system features
3. View and manage all notices
4. Access "Manage Users" to see all registered users
5. View user statistics and system overview

## Database Models

### User Model
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password`: Hashed password
- `role`: User role (admin/teacher/student)
- `department`: Department name
- `created_at`: Registration timestamp

### Notice Model
- `id`: Primary key
- `title`: Notice title
- `content`: Notice content
- `category`: Notice category
- `department`: Target department
- `priority`: Notice priority level
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `user_id`: Foreign key to User
- `is_active`: Active status

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control
- CSRF protection (built-in Flask)
- SQL injection prevention (SQLAlchemy ORM)

## Customization

### Adding New Departments
Edit the department options in:
- `templates/register.html`
- `templates/create_notice.html`
- `templates/edit_notice.html`

### Changing Colors/Theme
Modify CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #64748b;
    --success-color: #10b981;
    --danger-color: #ef4444;
    --warning-color: #f59e0b;
}
```

### Adding New Notice Categories
Update the category options in:
- `templates/create_notice.html`
- `templates/edit_notice.html`

## Production Deployment

### Important Security Changes:
1. Change the secret key in `app.py`:
```python
app.config['SECRET_KEY'] = 'your-secure-random-secret-key'
```

2. Disable debug mode:
```python
app.run(debug=False)
```

3. Use a production database (PostgreSQL/MySQL) instead of SQLite

4. Set up environment variables for sensitive data

5. Use a production WSGI server (Gunicorn, uWSGI)

6. Enable HTTPS/SSL

## Troubleshooting

### Database Issues
If you encounter database errors:
```bash
# Delete the database file
rm instance/college_notices.db

# Restart the application (database will be recreated)
python app.py
```

### Port Already in Use
If port 5000 is already in use:
```python
# In app.py, change the port:
app.run(debug=True, port=5001)
```

### Import Errors
Make sure you're in the virtual environment:
```bash
pip install -r requirements.txt
```

## Future Enhancements

- [ ] Email notifications for new notices
- [ ] File attachments for notices
- [ ] Notice expiry dates
- [ ] Search and filter functionality
- [ ] Notice read/unread status
- [ ] Mobile app integration
- [ ] API endpoints for external integration
- [ ] Comments/feedback on notices
- [ ] Notice templates
- [ ] Multi-language support

## License

This project is created for educational purposes.

## Support

For issues or questions:
- Check the troubleshooting section
- Review the code comments in `app.py`
- Ensure all dependencies are installed correctly

## Author

Created as a College Notice Board Management System

---

**Note**: This is a development version. Please implement additional security measures and testing before deploying to production.
