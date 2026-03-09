# Sic Mundus Vision - Quick Reference Guide

## 🚀 START HERE

### 1. Install & Setup (First Time Only)

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
pip install -r requirements.txt
python generate_dataset.py
```

### 2. Start the Server

```bash
python app.py
```

Server runs at: **http://127.0.0.1:5000**

### 3. Play the Challenge

Open browser → http://127.0.0.1:5000 → Click "BEGIN TIMELINE ANALYSIS"

---

## 📊 Automated Solving

### Run Full Exploit (Recommended)
```bash
python solver.py
```

**What it does:**
1. Probes 3 sessions to build hash mapping
2. Solves a new session using the mapping
3. Expected result: 90%+ accuracy with flag

**Time:** ~15-20 minutes

### Customize Solver

```bash
# Use more/fewer probe sessions
python solver.py --probe-sessions 5

# Custom server URL
python solver.py --url http://192.168.1.100:5000

# Only solve, don't probe (needs existing mapping)
python solver.py --solve-only
```

---

## 🎲 Manual Play

### Objective
- View 30 randomly shown images
- Mark each as **REAL TIMELINE** or **TEMPORAL ANOMALY**
- Achieve ≥90% accuracy to unlock flag

### Steps
1. Click **BEGIN TIMELINE ANALYSIS**
2. Scroll through and classify each image
3. Click **REAL** or **ANOMALY** for each
4. Click **SUBMIT VERDICT** when all 30 classified
5. View your accuracy and flag (if earned)

---

## 📁 File Structure

```
challenge/
├── app.py                           Main Flask server
├── generate_dataset.py              Creates test images
├── solver.py                        Automated exploit
├── requirements.txt                 Python dependencies
├── setup.bat                        Windows quick setup
│
├── README.md                        Full documentation
├── WALKTHROUGH.md                   Detailed guide
├── VULNERABILITY_ANALYSIS.md        Security details
├── QUICK_REFERENCE.md              This file!
│
├── templates/
│   └── index.html                  Web interface
├── static/
│   └── style.css                   Dark theme styling
├── artifacts/
│   ├── real/                       15 real images
│   └── fake/                       15 fake images
```

---

## 🔧 Commands Reference

| Task | Command |
|------|---------|
| Install deps | `pip install -r requirements.txt` |
| Generate images | `python generate_dataset.py` |
| Start server | `python app.py` |
| Run solver | `python solver.py` |
| Solve with 5 probes | `python solver.py --probe-sessions 5` |
| Custom URL | `python solver.py --url http://localhost:8000` |

---

## 🌐 API Overview

### Start Session
```
POST /api/timeline/start

Response:
{
  "session_id": "uuid",
  "artifacts": [...],
  "total": 30
}
```

### Get Image
```
GET /api/artifact/<artifact_id>

Response: JPEG image with random transformations
```

### Submit Verdicts
```
POST /api/timeline/verify

Body: { "session_id": "uuid", "timeline": [1,0,1,...] }

Response:
{
  "stability": 0.93,
  "correct": 28,
  "total": 30,
  "flag": "CrackOn{...}" (if ≥90%)
}
```

---

## 💡 Tips & Tricks

### For Manual Players
- Look for **realistic patterns** (real) vs **artificial geometric patterns** (fake)
- Real images: gradients, natural lighting, organic randomness
- Fake images: perfect symmetry, uniform grids, unnatural colors

### For Solver Users
- Run with 3-5 probe sessions for best results
- Each session takes ~2-3 minutes (rate limited at 1 req/sec)
- Probing finds ~85-95% of correct answers
- Matching on new session gets remaining ~5-15%

### Troubleshooting
```
Error: Port already in use
→ Kill existing server or change port in app.py

Error: Module not found
→ pip install -r requirements.txt

Error: Artifacts not found
→ python generate_dataset.py

Error: Slow solver
→ Normal! It respects rate limiting (1 req/sec)
```

---

## 🎓 Learning Path

**Beginner:** Play challenge manually (10 minutes)
→ *Understand game mechanics*

**Intermediate:** Read README.md and solve manually (30 minutes)
→ *Understand real vs fake patterns*

**Advanced:** Read VULNERABILITY_ANALYSIS.md and study solver.py (1-2 hours)
→ *Understand perceptual hashing exploitation*

**Expert:** Modify solver.py or create improvements (varies)
→ *Implement countermeasures or optimizations*

---

## 🏆 Success Criteria

- **Manual Victory:** Classify correctly with ≥90% accuracy
- **Automated Victory:** Get 90%+ with solver script
- **Ultimate Victory:** Understand AND explain why the exploit works

---

## 📝 Flag Format

```
CrackOn{Pr3petu4l_hash3s_l00k_c00l}
```

Appears when you achieve ≥90% accuracy in `/api/timeline/verify` response.

---

## 🔗 Important Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | Complete documentation |
| [WALKTHROUGH.md](WALKTHROUGH.md) | Step-by-step guide |
| [VULNERABILITY_ANALYSIS.md](VULNERABILITY_ANALYSIS.md) | Security details |
| [app.py](app.py) | Backend implementation |
| [solver.py](solver.py) | Automated exploit |
| [templates/index.html](templates/index.html) | Frontend UI |
| [static/style.css](static/style.css) | Dark theme styling |

---

## ⏱️ Time Estimates

| Activity | Time |
|----------|------|
| Installation | 5 min |
| Dataset generation | 2 min |
| Manual play | 30 min |
| Full solver exploit | 20 min |
| Reading vulnerability analysis | 15 min |
| Creating own exploit variant | 1-2 hours |

---

## 🎯 Challenge Stats

| Stat | Value |
|------|-------|
| Total Images | 30 |
| Real Images | 15 |
| Fake Images | 15 |
| Min Accuracy for Flag | 90% (27/30) |
| Session Timeout | 1 hour |
| Rate Limit | 1 req/sec per IP |
| Hash Match Accuracy | 93%+ |

---

## 📞 Common Questions

**Q: My solver is stuck?**
A: Check if app.py is running. If rate limited, wait. Check terminal for errors.

**Q: How long does solver take?**
A: ~15-20 min (respects 1 req/sec rate limit)

**Q: Can I modify the solver?**
A: Yes! It's a learning tool. Experiment with different hash methods.

**Q: What if I just guess?**
A: ~50% accuracy (15/30). Need 27/30 for flag.

**Q: Can I run multiple solver sessions?**
A: Yes! Each learns from previous sessions using hash map.

---

## 🚀 Next Steps

1. **Run:** `python app.py`
2. **Play:** Open http://127.0.0.1:5000
3. **Exploit:** `python solver.py`
4. **Learn:** Read VULNERABILITY_ANALYSIS.md
5. **Master:** Create improved version

---

**Created for the Dark-inspired CTF Challenge Series**

*"The error of man is to forget that he is a child created by God."*
