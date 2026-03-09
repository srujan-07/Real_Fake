# Render Deployment - Troubleshooting Guide

## 🔍 Quick Diagnostic

If images aren't loading on your Render deployment, follow these steps:

### 1. Check Image Availability

Visit this URL on your deployed site:
```
https://your-app.onrender.com/api/debug/images
```

**Expected response:**
```json
{
  "real_count": 15,
  "fake_count": 15,
  "total": 30,
  "real_dir_exists": true,
  "fake_dir_exists": true,
  ...
}
```

**If you see `"total": 0` or directories don't exist:**
- Your artifact images weren't pushed to GitHub
- Follow "Fix Missing Artifacts" section below

### 2. Check Render Logs

1. Go to https://dashboard.render.com
2. Click on your service
3. Click **"Logs"** tab
4. Look for these error messages:
   - `No images found in artifacts directories!`
   - `Image file not found: /opt/render/project/src/artifacts/...`
   - `Failed to load image: ...`

### 3. Test Image Loading

Start a session and try to load an image:
```bash
# Start session
curl -X POST https://your-app.onrender.com/api/timeline/start

# Copy one artifact URL from response
curl https://your-app.onrender.com/api/artifact/ARTIFACT_ID_HERE
```

**Expected:** Binary image data (JPEG)  
**If error:** Check logs for specific error message

---

## 🔧 Common Issues & Fixes

### Issue 1: "No images found in artifacts directories!"

**Cause:** Artifact images weren't committed to git

**Fix:**
```bash
# Check if artifacts are in git
git ls-files artifacts/

# If empty, add them:
git add artifacts/
git status  # Should show 30 files
git commit -m "Add artifact images"
git push
```

After push, Render will auto-deploy. Wait 2-3 minutes.

### Issue 2: "Image file not found"

**Cause:** File paths are incorrect or files are missing

**Fix:**
```bash
# Verify all 30 images exist locally
ls artifacts/real/*.jpg | wc -l   # Should be 15
ls artifacts/fake/*.jpg | wc -l   # Should be 15

# Check git has them
git ls-files artifacts/ | wc -l   # Should be 30

# If correct, recommit and push
git add artifacts/
git commit -m "Ensure all artifacts are included"
git push
```

### Issue 3: "Failed to load artifact" (500 error)

**Causes:**
1. Image file corrupted
2. PIL can't open the image
3. Memory issue on free tier

**Fix:**
```bash
# Test all images locally
python -c "
from PIL import Image
from pathlib import Path

for img in Path('artifacts/real').glob('*.jpg'):
    try:
        Image.open(img).verify()
        print(f'✓ {img.name}')
    except Exception as e:
        print(f'✗ {img.name}: {e}')
"
```

If all images work locally but fail on Render, try:
- Upgrade from free tier (more memory)
- Reduce image sizes: `python generate_dataset.py` with smaller dimensions

### Issue 4: Images load intermittently

**Cause:** Rate limiting or multiple workers causing session issues

**Fix in render.yaml:**
```yaml
startCommand: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

Change `--workers 2` to `--workers 1` to avoid session sharing issues.

### Issue 5: Blank images or "Artifact not found"

**Cause:** Session expired or wasn't created properly

**Fix:** Check browser console for JavaScript errors:
1. Press F12 in browser
2. Go to Console tab
3. Look for errors when clicking "Start Analysis"
4. Check Network tab for failed requests

---

## ✅ Verification Checklist

Before deploying to Render, verify:

- [ ] Git repository initialized: `git status`
- [ ] 30 artifact files committed: `git ls-files artifacts/ | wc -l`
- [ ] Images load locally: Test at http://127.0.0.1:5000
- [ ] Debug endpoint works locally: http://127.0.0.1:5000/api/debug/images
- [ ] All files pushed: `git push`
- [ ] Render.yaml exists in root directory
- [ ] requirements.txt includes all dependencies

---

## 🚀 Deployment Commands

### Initial Deployment
```bash
# 1. Ensure everything is committed
git add .
git commit -m "Ready for deployment"
git push

# 2. Watch Render logs during deployment
# Go to dashboard.render.com → Your Service → Logs
```

### After Code Changes
```bash
# Any push triggers auto-deploy
git add .
git commit -m "Fix image loading"
git push

# Wait 2-3 minutes for Render to rebuild
```

### Force Rebuild
If auto-deploy doesn't work:
1. Go to dashboard.render.com
2. Click your service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 📊 Testing Your Live Deployment

Once deployed to `https://your-app.onrender.com`:

```bash
# 1. Health check
curl https://your-app.onrender.com/health

# 2. Debug images (IMPORTANT - check this first!)
curl https://your-app.onrender.com/api/debug/images

# 3. Start session
curl -X POST https://your-app.onrender.com/api/timeline/start

# 4. Load sample image (use artifact_id from step 3)
curl https://your-app.onrender.com/api/artifact/ARTIFACT_ID > test.jpg
open test.jpg  # On Mac
# Or: start test.jpg  # On Windows
```

---

## 🆘 Still Having Issues?

### Enable Debug Logging

Add to render.yaml:
```yaml
envVars:
  - key: FLASK_ENV
    value: production
  - key: LOG_LEVEL
    value: DEBUG
```

### Check Render Build Logs

1. Dashboard → Your Service → **Events** tab
2. Look for build failures or warnings
3. Check "Build" section for file copying issues

### Worst Case: Start Fresh

```bash
# Delete and recreate
rm -rf .git
git init
git add .
git commit -m "Fresh start"
git remote add origin YOUR_GITHUB_URL
git push -u origin main --force

# Redeploy on Render (may need to reconnect GitHub)
```

---

## 📞 Getting Help

Include this info when asking for help:

1. Output of: `curl https://your-app.onrender.com/api/debug/images`
2. Render logs (last 50 lines)
3. Browser console errors (F12 → Console)
4. Local test result: `git ls-files artifacts/ | wc -l`

---

## 🎯 Expected Working State

When everything works:

- `/health` returns `{"status": "ok", ...}`
- `/api/debug/images` shows `"total": 30`
- `/` loads the web interface
- Images display when clicking "Start Analysis"
- Solver achieves 90%+ accuracy
- Flag is revealed at 90%+ accuracy
