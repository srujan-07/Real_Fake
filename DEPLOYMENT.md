# Deploying Real_Fake CTF Challenge to Render

## Prerequisites
- GitHub account
- Render account (sign up at https://render.com)
- Git installed locally

## Step-by-Step Deployment Guide

### 1. Prepare Your Repository

First, ensure your code is in a Git repository and pushed to GitHub:

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for Render deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/real-fake-ctf.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Render

#### Option A: Using render.yaml (Recommended)

1. Go to https://render.com and sign in
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Click **"Apply"** to deploy

#### Option B: Manual Setup

1. Go to https://render.com and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `real-fake-ctf` (or your choice)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave blank
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Plan**: Free (or paid for better performance)

5. Add Environment Variables (if needed):
   - `PYTHON_VERSION`: `3.11.0`

6. Click **"Create Web Service"**

### 3. Verify Deployment

Once deployed, Render will provide a URL like: `https://real-fake-ctf.onrender.com`

Test the endpoints:
- Health check: `https://your-app.onrender.com/health`
- Main page: `https://your-app.onrender.com/`

### 4. Important Notes

#### Free Tier Limitations
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30-60 seconds to wake up
- 750 hours/month of free usage

#### Performance Optimization
- Consider upgrading to a paid plan for consistent uptime
- Adjust worker count in start command based on your plan
- Monitor response times and adjust `REQUEST_DELAY` if needed

#### Security Considerations
- The FLAG is hardcoded in `app.py` - this is intentional for the CTF
- For production, consider using environment variables
- Rate limiting is already implemented

### 5. Updating Your Deployment

Render auto-deploys on every push to your connected branch:

```bash
# Make changes to your code
git add .
git commit -m "Update challenge"
git push
```

Render will automatically rebuild and redeploy.

### 6. Monitoring

- View logs in the Render dashboard
- Set up alerts for service downtime
- Monitor the `/health` endpoint

### 7. Custom Domain (Optional)

In Render dashboard:
1. Go to your service
2. Click **"Settings"** → **"Custom Domain"**
3. Add your domain and configure DNS

## Troubleshooting

### Service Won't Start
- Check logs in Render dashboard
- Verify all dependencies in `requirements.txt`
- Ensure `artifacts/real/` and `artifacts/fake/` directories exist with images

### Images Not Loading
- Verify artifact directories are committed to git
- Check file paths are relative (not absolute)
- Ensure image files are not in `.gitignore`

### Slow Performance
- Upgrade from free tier
- Increase worker count in start command
- Reduce `REQUEST_DELAY` in app.py (currently 0.05s)

## Cost Estimate

- **Free Tier**: $0/month (with limitations)
- **Starter**: $7/month (always-on, better performance)
- **Standard**: $25/month (production-ready)

## Support

For Render-specific issues, check:
- Render documentation: https://render.com/docs
- Render community: https://community.render.com
