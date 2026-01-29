# Quick Fix for "Not Found" Error

If you're seeing "Not Found" on your deployed app, follow these steps:

## Manual Deployment (Alternative to render.yaml)

1. **Create PostgreSQL Database First:**
   - Go to Render Dashboard
   - Click "New +" → "PostgreSQL"
   - Name: `college-notices-db`
   - Region: Choose closest to you
   - Click "Create Database"
   - Wait for it to be ready
   - Copy the **Internal Database URL**

2. **Create Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `college_notice_board` repository
   
3. **Configure the Service:**
   - **Name:** `college-notice-board` (or your choice)
   - **Region:** Same as database
   - **Branch:** `main`
   - **Root Directory:** Leave blank
   - **Runtime:** Python 3
   - **Build Command:** 
     ```
     pip install -r requirements.txt && python init_db.py
     ```
   - **Start Command:** 
     ```
     gunicorn app:app
     ```

4. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable"
   
   - Variable 1:
     - Key: `DATABASE_URL`
     - Value: [Paste the Internal Database URL from step 1]
   
   - Variable 2:
     - Key: `SECRET_KEY`
     - Value: [Generate a random string, e.g., use https://randomkeygen.com/]
   
   - Variable 3:
     - Key: `PYTHON_VERSION`
     - Value: `3.11.0`

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Check the logs for any errors

6. **If Still "Not Found":**
   - Go to the Shell tab in your web service
   - Run: `python init_db.py`
   - Restart the service

## Verify Database Connection

In the Shell tab of your web service, run:
```python
python -c "from app import db, app; app.app_context().push(); db.create_all(); print('Database tables created!')"
```

This should create all necessary tables.
