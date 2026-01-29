# Render Deployment Guide for College Notice Board

## Prerequisites
1. Create a [Render account](https://render.com/) (free tier available)
2. Push your code to a GitHub repository

## Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. **Create New Blueprint in Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and create:
     - A PostgreSQL database
     - A web service running your Flask app

3. **Wait for deployment:**
   - Build process will run `build.sh` automatically
   - Database will be initialized with the admin user
   - Your app will be live at `https://your-app-name.onrender.com`

### Option 2: Manual Setup

1. **Create PostgreSQL Database:**
   - Go to Render Dashboard
   - Click "New +" → "PostgreSQL"
   - Name: `college-notices-db`
   - Choose Free tier
   - Click "Create Database"
   - Copy the "Internal Database URL"

2. **Create Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** college-notice-board
     - **Runtime:** Python
     - **Build Command:** `./build.sh`
     - **Start Command:** `gunicorn app:app`
     - **Environment Variables:**
       - `SECRET_KEY`: (generate a random string)
       - `DATABASE_URL`: (paste the database URL from step 1)
   - Click "Create Web Service"

## Default Admin Credentials
- **Username:** admin
- **Password:** admin123

⚠️ **IMPORTANT:** Change the admin password immediately after first login!

## Post-Deployment

1. Visit your app URL: `https://your-app-name.onrender.com`
2. Login with admin credentials
3. Change the admin password in the user settings
4. Create additional users as needed

## Troubleshooting

### "Not Found" Error
If you see a blank page with "Not Found":

1. **Check Build Logs:**
   - Go to Render Dashboard → Your Service → Logs
   - Look for any errors during build or deployment
   - Ensure all packages installed successfully

2. **Verify Environment Variables:**
   - Check that `DATABASE_URL` is set correctly
   - Check that `SECRET_KEY` is generated
   - Go to Environment tab and verify all variables

3. **Manual Database Setup:**
   If database initialization failed, manually run:
   - Go to Shell tab in your web service
   - Run: `python init_db.py`

4. **Check Service Status:**
   - Ensure the service is "Live" (green dot)
   - Check if it's still deploying (yellow)
   - Review deployment logs for errors

5. **Common Issues:**
   - PostgreSQL database not connected → Check DATABASE_URL
   - Build command failed → Check requirements.txt
   - Port binding issue → Ensure using `$PORT` environment variable

- **Database not initializing:** Check the build logs in Render dashboard
- **App not starting:** Verify environment variables are set correctly
- **Connection errors:** Ensure DATABASE_URL is properly configured

## Free Tier Limitations
- App will spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- Database has 1GB storage limit
