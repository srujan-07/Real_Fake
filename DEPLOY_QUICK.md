# Quick Deployment Checklist

## ✅ Files Created for Render Deployment

- [x] `requirements.txt` - Updated with gunicorn
- [x] `render.yaml` - Blueprint configuration for Render
- [x] `Procfile` - Alternative deployment config
- [x] `.gitignore` - Ensures artifacts are included
- [x] `DEPLOYMENT.md` - Full deployment guide
- [x] `app.py` - Updated for production (gunicorn) compatibility

## 🚀 Quick Start

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Ready for Render deployment"
git remote add origin https://github.com/YOUR_USERNAME/real-fake-ctf.git
git push -u origin main
```

### 2. Deploy on Render

**Option A - Blueprint (Easiest):**
1. Go to https://render.com
2. Click "New +" → "Blueprint"
3. Connect your GitHub repo
4. Click "Apply"
5. Done! 🎉

**Option B - Manual:**
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
5. Click "Create Web Service"
6. Done! 🎉

### 3. Access Your CTF

Your app will be at: `https://real-fake-ctf.onrender.com`

Test it:
- Main page: `/`
- Health check: `/health`
- API: `/api/timeline/start` (POST)

## ⚙️ Configuration

All set with sensible defaults:
- ✅ 2 workers (good for free tier)
- ✅ 120s timeout (handles slow image processing)
- ✅ Rate limiting (50ms between requests)
- ✅ Session management
- ✅ Health check endpoint

## 📊 What's Included

- Flask web server
- 30 artifact images (15 real + 15 fake)
- Perceptual hashing challenge
- Auto-scoring system
- Flag: `CrackOn{Pr3petu4l_hash3s_l00k_c00l}`

## 🎯 CTF Challenge Details

- Players get 30 images to classify
- Must achieve 90% accuracy (27/30 correct)
- Images are transformed per-request (different MD5)
- Solution: Perceptual hashing with fuzzy matching
- Difficulty: Easy-Medium

## 🐛 Troubleshooting

**Service won't start:**
- Check Render logs in dashboard
- Verify all artifact images are committed to git
- Make sure `artifacts/real/` and `artifacts/fake/` directories are not empty

**Slow first load:**
- Free tier spins down after 15min inactivity
- First request takes ~30-60s to wake up
- Upgrade to paid tier for always-on service

**Images not loading:**
- Ensure `.gitignore` doesn't exclude `artifacts/`
- Check file paths in logs
- Verify images were pushed to GitHub

## 💻 Local Development

**Windows users:** Gunicorn doesn't work on Windows. For local testing, use:
```bash
python app.py
```

**Linux/Mac users:** You can test gunicorn locally:
```bash
gunicorn app:app --bind 127.0.0.1:8000 --workers 2
```

Both methods work fine - Render will use gunicorn automatically on its Linux servers.

## 💰 Cost

- **Free**: $0/month (with cold starts)
- **Starter**: $7/month (always-on)
- **Standard**: $25/month (production-ready)

## 📝 Notes

- Free tier has 750 hours/month
- Auto-deploys on git push
- SSL certificate included
- Custom domain support available

## 🔗 Useful Links

- Render Dashboard: https://dashboard.render.com
- Documentation: https://render.com/docs
- Your repo: Update after creating on GitHub

---

**Ready to deploy!** Follow the steps above and your CTF challenge will be live in minutes.
