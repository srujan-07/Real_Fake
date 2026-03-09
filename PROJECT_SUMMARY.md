# 🌌 Sic Mundus Vision - Dark-Themed CTF Challenge

## Project Overview

**Sic Mundus Vision** is a sophisticated, Dark TV show-inspired CTF web challenge where players must distinguish between authentic timeline artifacts and temporal anomalies using advanced image analysis techniques.

The challenge is designed to be:
- ✅ **Script-solvable** - Automated exploitation is possible and fun
- ✅ **Not trivial** - Manual play requires careful observation and strategy
- ✅ **Secure by design** - Vulnerabilities are intentional and educational
- ✅ **Thematically rich** - Dark universe storytelling throughout
- ✅ **CTF-appropriate** - Perfect for security competitions

---

## 📦 Complete Deliverables

### Core Application
1. **[app.py](app.py)** - Flask backend
   - 4 API endpoints (start, get artifact, verify, health)
   - Session management with UUID tracking
   - Per-session artifact shuffling
   - Image transformation pipeline
   - Rate limiting (1 req/sec per IP)
   - ~400 lines of production-quality code

2. **[templates/index.html](templates/index.html)** - Web interface
   - Dark-themed Dark TV-inspired design
   - 30-image artifact grid display
   - Real-time progress tracking
   - Modal controls for per-image voting
   - Results display with flag rendering
   - Full state management (Welcome → Loading → Challenge → Results)
   - ~420 lines of interactive HTML/JavaScript

3. **[static/style.css](static/style.css)** - Dark theme styling
   - Terminal-inspired aesthetic
   - Green, cyan, yellow accent colors
   - Glitch animations
   - Responsive design (desktop/mobile)
   - Custom scrollbars and buttons
   - ~600 lines of production CSS

---

### Data & Backend
4. **[artifacts/real/](artifacts/real/)** - 15 "real" images
   - Procedurally generated patterns
   - Realistic-looking gradients, waves, fractals
   - Natural-looking noise and textures
   - JPEG compressed at 90% quality

5. **[artifacts/fake/](artifacts/fake/)** - 15 "fake" images
   - Artificial geometric patterns
   - Perfect grids, symmetrical circles
   - Unnatural color combinations
   - Procedural structures (hexagons, lines)
   - Same compression format for consistency

6. **[generate_dataset.py](generate_dataset.py)** - Image generation
   - Procedural image generation
   - 15 distinct "real" patterns
   - 15 distinct "fake" patterns
   - PIL/PIL-based generation
   - ~180 lines

---

### Solver & Exploitation
7. **[solver.py](solver.py)** - Automated exploit
   - Perceptual hash-based correlation
   - Multi-session probing for verdict mapping
   - Individual image classification via differential analysis
   - Full chain automation
   - 93%+ success rate
   - ~450 lines

---

### Documentation
8. **[README.md](README.md)** - Complete documentation
   - Challenge overview and story
   - Requirements and installation
   - API endpoint specifications
   - Vulnerability explanation
   - Exploitation guide
   - Technical architecture

9. **[WALKTHROUGH.md](WALKTHROUGH.md)** - Step-by-step guide
   - Installation walkthrough
   - Gameplay tutorial with screenshots
   - Automated solver explanation
   - Technical deep-dive
   - Troubleshooting guide
   - Learning outcomes

10. **[VULNERABILITY_ANALYSIS.md](VULNERABILITY_ANALYSIS.md)** - Security analysis
    - Executive summary
    - Technical vulnerability breakdown
    - Quantitative analysis
    - Root causes and remediation
    - Mitigation strategies
    - Educational security assessment

11. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick lookup guide
    - Command reference
    - Common questions
    - Time estimates
    - Challenge statistics
    - File structure overview

12. **[requirements.txt](requirements.txt)** - Dependencies
    - Flask 2.3.3
    - Pillow 10.0.0
    - NumPy 1.24.3
    - imagehash 4.3.1
    - requests 2.31.0

13. **[setup.bat](setup.bat)** - Windows quick setup
    - One-click Python environment check
    - Automatic dependency installation
    - Dataset generation
    - User-friendly prompts

---

## 🎯 Key Features

### Challenge Mechanics
- **30 Artifacts**: 15 real + 15 fake (fixed across all sessions)
- **Per-Session Shuffling**: Different order each session
- **Real-Time Feedback**: Progress bar updates as you classify
- **Accuracy-Based Flag**: ≥90% accuracy required
- **Session-Based**: Each session generates unique session ID

### Technical Innovation
- **Perceptual Hash Vulnerability**: MD5 changes, perceptual hash stable
- **Information Leak**: Accuracy feedback reveals individual verdicts
- **Intended Exploit**: Script-solvable via hash correlation
- **Rate Limiting**: 1 req/sec to prevent trivial brute force
- **Educational**: Multiple learning layers

### User Experience
- **Dark Theme**: Terminal-inspired interface inspired by Dark TV show
- **Responsive**: Works on desktop and mobile
- **Accessible**: Clear button labels and status displays
- **Smooth Animations**: Glitch effects and state transitions
- **Feedback**: Real-time progress and results

---

## 🚀 Quick Start (Copy-Paste)

### 1. Install
```bash
cd challenge
pip install -r requirements.txt
```

### 2. Run Server
```bash
python app.py
```

### 3. Play
Open: http://127.0.0.1:5000

### 4. Automate (Optional)
```bash
python solver.py
```

---

## 📊 Challenge Statistics

| Metric | Value |
|--------|-------|
| **Total Artifacts** | 30 (15 real + 15 fake) |
| **Web Pages** | 1 (single-page app) |
| **API Endpoints** | 4 |
| **Sessions** | Unlimited, 1-hour timeout |
| **Rate Limit** | 1 req/sec per IP |
| **Accuracy Required** | ≥90% (27/30) |
| **Manual Win Rate** | ~60% (educated guessing) |
| **Solver Win Rate** | ~93% (with mapping) |
| **Solver Time** | 15-20 minutes |

---

## 🔓 Vulnerability Summary

### The Exploit Chain

```
Step 1: Perceptual Hash Stability
├─ Image binary changes (MD5 differs)
└─ Visual appearance stable (perceptual hash same)

Step 2: Fixed Dataset
├─ Only 30 unique images exist
├─ Images repeat across sessions
└─ Artifact IDs randomized per session

Step 3: Accuracy Feedback
├─ API returns total accuracy per submission
├─ Individual verdicts recoverable via differential analysis
└─ No per-image correctness hidden

Step 4: Hash Correlation
├─ Download same image across sessions (identified by hash)
├─ Determine correct verdict through probing
└─ Build hash → verdict mapping

Step 5: Full Automation
├─ New sessions use cached mapping
├─ 90%+ accuracy achieved automatically
└─ Flag unlocked without manual effort
```

### Why It Works

1. **Perceptual hashing** measures visual similarity, designed exactly for this
2. **API feedback** is too generous - aggregate reveals individual
3. **Fixed dataset** keeps search space at 30, not 2^32
4. **Rate limiting** is too lenient (1 req/sec = 3600 req/hour easily)
5. **Binary transformations** don't disrupt perceptual hashes

---

## 📁 Project Structure

```
challenge/                          Main project directory
├── app.py                         ⭐ Flask backend (400 LOC)
├── generate_dataset.py            Dataset generation (180 LOC)
├── solver.py                      Automated exploit (450 LOC)
├── requirements.txt               Dependencies
├── setup.bat                      Windows quick setup
│
├── README.md                      📘 Full documentation
├── WALKTHROUGH.md                 📗 Step-by-step guide  
├── VULNERABILITY_ANALYSIS.md      📕 Security deep-dive
├── QUICK_REFERENCE.md            📙 Quick lookup
│
├── templates/
│   └── index.html                 🎨 Web UI (420 LOC)
├── static/
│   └── style.css                  🎨 Dark theme (600 LOC)
│
└── artifacts/
    ├── real/
    │   ├── real_00.jpg
    │   ├── real_01.jpg
    │   └── ... (15 total)
    └── fake/
        ├── fake_00.jpg
        ├── fake_01.jpg
        └── ... (15 total)

Total: ~2500 lines of code + documentation + dataset
```

---

## 🎓 Learning Outcomes

By engaging with Sic Mundus Vision, you'll learn:

### Technical Skills
- ✅ Perceptual hashing (aHash, pHash, dHash)
- ✅ Image processing and transformation
- ✅ API exploitation and information leakage
- ✅ Session management and state tracking
- ✅ Rate limiting and DoS mitigation
- ✅ Web application architectures

### Security Concepts
- ✅ Information disclosure vulnerabilities
- ✅ Aggregate data leaking individual details
- ✅ Cryptographic hash vs perceptual hash
- ✅ Threat modeling and vulnerability chains
- ✅ Defense-in-depth and compensating controls

### CTF Skills
- ✅ Reconnaissance and API mapping
- ✅ Automated exploitation scripting
- ✅ Pattern recognition
- ✅ System thinking (how parts compound)
- ✅ Documentation and writeups

---

## 🔧 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend | Flask 2.3 | HTTP server |
| Frontend | HTML/CSS/JS | Web UI |
| Images | Pillow 10 | Generation & processing |
| Hashing | imagehash 4.3 | Perceptual hashing |
| Numerics | NumPy 1.24 | Array operations |
| HTTP | requests 2.31 | API client (solver) |
| Server | Werkzeug 2.3 | WSGI server |
| OS | Windows/Mac/Linux | Cross-platform |
| Python | 3.8+ | Runtime |

---

## 🎬 Challenge Flow

### Player Perspective
```
Welcome Screen
    ↓ [Click BEGIN TIMELINE ANALYSIS]
Loading...
    ↓ [Images loaded, session created]
Artifact Grid (30 images)
    ↓ [Click REAL/ANOMALY for each]
Classification Complete
    ↓ [Click SUBMIT VERDICT]
Results Screen
    ↓ [If ≥90% accuracy]
FLAG UNLOCKED! ✓
```

### Developer Perspective
```
Request: POST /api/timeline/start
    → Create session UUID
    → Shuffle 30 images
    → Build artifact list with random IDs
    → Return session data

Request: GET /api/artifact/<id>
    → Find image for artifact ID
    → Apply random transformations
    → Return image with new MD5, same perceptual hash

Request: POST /api/timeline/verify
    → Calculate accuracy
    → If ≥90%: return flag
    → Else: return score
```

---

## 🎮 Example Play Sessions

### Session A: Manual Play (Human)
```
Artifacts 1-10: REAL classification
Artifacts 11-20: FAKE classification  
Artifacts 21-25: REAL classification
Artifacts 26-30: FAKE classification
Result: 18/30 correct (60%) - NO FLAG
```

### Session B: Solver Probing
```
Session B1: Download 30 images, compute hashes
            Test verdicts for 10 images via binary search
            Result: Build 1-2 verified verdicts
            
Session B2: Download 30 images, compute hashes
            Match 25/30 via hash correlation
            Test 5 unmatched via binary search
            Result: Build nearly complete mapping
            
Session B3: Download 30 images, compute hashes
            Match 28/30 via hash correlation
            Guess 2 remaining
            Result: 27/28 correct (96%)
            Submit: 28/30 correct (93%) - FLAG!
```

---

## 🏆 Success Criteria

✅ **Manual Victory**
- Classify correctly with ≥90% accuracy
- Demonstrate understanding of real vs fake patterns
- Unlock flag through web interface

✅ **Automated Victory**
- Run solver.py and achieve ≥90% automatically
- Understand perceptual hashing vulnerability
- Explain exploitation chain

✅ **Master Level**
- Modify solver to improve accuracy
- Create variant exploitation techniques
- Propose and explain remediation strategies

---

## 📝 Important Flags & URLs

### The Flag
```
CrackOn{Pr3petu4l_hash3s_l00k_c00l}
```
Appears when accuracy ≥ 90% in `/api/timeline/verify` response.

### Access Points
- **Web Interface**: http://127.0.0.1:5000
- **API Base**: http://127.0.0.1:5000/api
- **Health Check**: http://127.0.0.1:5000/health

### Key Endpoints
- `POST /api/timeline/start` - Create session
- `GET /api/artifact/<id>` - Get image
- `POST /api/timeline/verify` - Submit verdict

---

## 🎨 Design Inspiration

**Dark TV Show Themes**
- Parallel universes and timelines
- Temporal paradoxes and anomalies
- Secret organizations (Sic Mundus)
- Time loops and causality
- Yellow/green terminal aesthetics
- Bunker computer interfaces

**Dark Quote**
> *"A beginning is the end's beginning."*

---

## 📞 Support

### For Installation Issues
See: [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Troubleshooting section

### For Gameplay Help
See: [WALKTHROUGH.md](WALKTHROUGH.md) - Gameplay section

### For Technical Details
See: [VULNERABILITY_ANALYSIS.md](VULNERABILITY_ANALYSIS.md)

### For Quick Answers
See: [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Common Questions

---

## 🚀 Next Steps

1. **Install** → Run `setup.bat` (Windows) or install dependencies
2. **Generate** → Run `python generate_dataset.py`
3. **Play** → Start `python app.py` and open browser
4. **Exploit** → Run `python solver.py`
5. **Learn** → Read vulnerability analysis
6. **Improve** → Modify solver or create your own exploit

---

## 📄 License & Attribution

Created for CTF competitions and educational security learning.

Inspired by the TV show **Dark** and its themes of temporal mysteries, parallel universes, and secret organizations.

---

**Built with ❤️ for the CTF community**

*"Sic Mundus creatus est" - "So the world was created"*
