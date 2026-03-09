# 📖 Sic Mundus Vision - Master Index

Welcome to **Sic Mundus Vision**, a Dark TV show-inspired CTF challenge.

This index will help you navigate all documentation and get started quickly.

---

## 🚀 Quick Start (5 Minutes)

### For Players (Just Want to Play)
1. Open [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. Run: `setup.bat` (Windows) or `pip install -r requirements.txt`
3. Run: `python app.py`
4. Open: http://127.0.0.1:5000
5. Classify 30 images and try to achieve 90%+ accuracy

### For Hackers (Want to Exploit)
1. Open [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. Install dependencies (same as above)
3. Run: `python solver.py`
4. Watch it automatically solve the challenge
5. Read [VULNERABILITY_ANALYSIS.md](VULNERABILITY_ANALYSIS.md) to understand why

### For Educators (Want to Teach)
1. Start with [README.md](README.md) for overview
2. Use [VULNERABILITY_ANALYSIS.md](VULNERABILITY_ANALYSIS.md) for security lessons
3. Have students complete [WALKTHROUGH.md](WALKTHROUGH.md)
4. Discuss solutions from [solver.py](solver.py)

---

## 📚 Documentation Map

### Top-Level Entry Points

| Document | Best For | Read Time | Purpose |
|----------|----------|-----------|---------|
| **[README.md](README.md)** | Everyone | 15 min | Complete overview and API reference |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Project managers | 10 min | High-level project status and deliverables |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | Players & hackers | 5 min | Commands, quick start, FAQ |
| **[WALKTHROUGH.md](WALKTHROUGH.md)** | Learners & CTF players | 30 min | Step-by-step game and exploit tutorials |
| **[VULNERABILITY_ANALYSIS.md](VULNERABILITY_ANALYSIS.md)** | Security professionals | 20 min | Deep technical analysis and remediation |

### Choose Your Path

#### 🎮 Path 1: I Just Want to Play
```
QUICK_REFERENCE.md (commands)
    ↓
Play at http://127.0.0.1:5000
    ↓
WALKTHROUGH.md (if stuck)
    ↓
Unlock flag (≥90% accuracy)
```

#### 🔓 Path 2: I Want to Exploit It
```
README.md (understand game)
    ↓
solver.py (run and watch)
    ↓
WALKTHROUGH.md (understand solver)
    ↓
VULNERABILITY_ANALYSIS.md (understand why it works)
```

#### 🏫 Path 3: I Want to Learn Security
```
README.md (overview)
    ↓
VULNERABILITY_ANALYSIS.md (core concepts)
    ↓
WALKTHROUGH.md (exploitation techniques)
    ↓
solver.py (code study)
    ↓
Modify solver and experiment
```

#### 🎓 Path 4: I'm an Educator
```
PROJECT_SUMMARY.md (project status)
    ↓
README.md (explain to students)
    ↓
VULNERABILITY_ANALYSIS.md (teach about vulnerabilities)
    ↓
Have students run WALKTHROUGH.md
    ↓
Discuss solver.py implementation
```

---

## 📁 File Organization

```
challenge/
│
├── 📖 DOCUMENTATION
│   ├── INDEX.md (this file)
│   ├── README.md (main documentation)
│   ├── PROJECT_SUMMARY.md (project overview)
│   ├── QUICK_REFERENCE.md (quick lookup)
│   ├── WALKTHROUGH.md (step-by-step guide)
│   └── VULNERABILITY_ANALYSIS.md (security deep-dive)
│
├── 🔧 APPLICATION
│   ├── app.py (Flask backend)
│   ├── solver.py (automated exploit)
│   ├── generate_dataset.py (image generator)
│   ├── requirements.txt (dependencies)
│   └── setup.bat (Windows setup)
│
├── 🎨 WEB INTERFACE
│   ├── templates/
│   │   └── index.html (web UI)
│   └── static/
│       └── style.css (dark theme)
│
└── 🖼️ DATA
    └── artifacts/
        ├── real/ (15 real images)
        └── fake/ (15 fake images)
```

---

## 🎯 What You'll Find

### README.md
**Purpose:** Complete technical documentation

**Contains:**
- Challenge story and theme
- Feature list
- Installation instructions
- API specifications
- Intended vulnerability explanation
- Exploitation guide
- Learning resources

**When to Read:** Before diving into technical details

---

### QUICK_REFERENCE.md
**Purpose:** Fast command lookup and FAQ

**Contains:**
- One-line installation/runtime commands
- API endpoint quick reference
- Solver command options
- Common troubleshooting
- Time estimates
- Challenge statistics

**When to Read:** First thing for quick answers

---

### WALKTHROUGH.md
**Purpose:** Step-by-step tutorials for both players and attackers

**Contains:**
- Detailed installation walkthrough
- Gameplay tutorial with examples
- Automated solver explanation
- Technical deep-dives
- Troubleshooting guide
- Learning outcomes

**When to Read:** After README if you want detailed guidance

---

### VULNERABILITY_ANALYSIS.md
**Purpose:** Security-focused analysis of intentional vulnerabilities

**Contains:**
- Executive summary
- Technical vulnerability breakdown
- Exploitation difficulty analysis
- Root causes of vulnerabilities
- Quantitative metrics
- Remediation strategies
- Educational security assessments

**When to Read:** For understanding *why* the exploit works

---

### PROJECT_SUMMARY.md
**Purpose:** High-level project status and deliverables

**Contains:**
- Complete deliverables list
- Key features summary
- Technology stack
- Challenge flow diagrams
- Statistics and metrics
- Success criteria

**When to Read:** For project overview and status

---

## 🚀 Installation Quick Start

### Windows
```bash
setup.bat
python app.py
```

### macOS/Linux
```bash
pip install -r requirements.txt
python generate_dataset.py
python app.py
```

### Then
Open browser: http://127.0.0.1:5000

---

## 🎮 Gameplay Quick Start

1. Click **"BEGIN TIMELINE ANALYSIS"**
2. View 30 images in a grid
3. Click **"REAL"** or **"ANOMALY"** for each image
4. Click **"SUBMIT VERDICT"** when all classified
5. See your accuracy score
6. Unlock flag if you achieve ≥90%

---

## 🔓 Automated Exploitation Quick Start

```bash
# Standard run (3 probe sessions)
python solver.py

# Custom settings
python solver.py --probe-sessions 5
python solver.py --url http://example.com:5000
python solver.py --solve-only
```

Expected result: ~93% accuracy with flag

---

## 📊 Dashboard of Key Files

### Code Quality
- **app.py** (400 LOC) - Clean, well-documented Flask app
- **solver.py** (450 LOC) - Interactive exploitation code  
- **generate_dataset.py** (180 LOC) - Procedural generation

### Web Interface
- **index.html** (420 LOC) - Interactive JavaScript UI with state management
- **style.css** (600 LOC) - Custom dark theme with animations

### Documentation
- **README.md** - 400+ lines, comprehensive
- **VULNERABILITY_ANALYSIS.md** - 300+ lines, technical depth
- **WALKTHROUGH.md** - 350+ lines, step-by-step
- **PROJECT_SUMMARY.md** - 250+ lines, executive overview
- **QUICK_REFERENCE.md** - 200+ lines, lookup table

### Data
- **artifacts/real/** - 15 procedurally generated images
- **artifacts/fake/** - 15 procedurally generated images

---

## 🎓 Learning Paths by Skill Level

### Beginner
1. Read: QUICK_REFERENCE.md (5 min)
2. Do: Install and play manually (15 min)
3. Read: WALKTHROUGH.md gameplay section (10 min)

**Total: 30 minutes**
**Outcome:** Understand game mechanics

---

### Intermediate
1. Read: README.md (15 min)
2. Do: Manual play, try to reach 90% (30 min)
3. Do: Run solver.py and observe (5 min)
4. Read: VULNERABILITY_ANALYSIS.md intro (10 min)

**Total: 1 hour**
**Outcome:** Understand vulnerability exists

---

### Advanced
1. Read: All documentation (90 min)
2. Study: solver.py code (30 min)
3. Debug: Run solver with breakpoints (30 min)
4. Experiment: Modify solver.py (60 min)
5. Create: Alternative exploitation method (120 min)

**Total: 5-6 hours**
**Outcome:** Master-level understanding

---

## ❓ Frequently Asked Questions

**Q: Where do I start?**
A: See "Quick Start" section above, or follow your skill level learning path.

**Q: How long does it take?**
A: 5 min (quick start), 30 min (play), 20 min (run solver), 2 hours (understand fully).

**Q: What if I get stuck?**
A: See QUICK_REFERENCE.md troubleshooting section.

**Q: Can I modify the code?**
A: Yes! It's designed for learning and experimentation.

**Q: Is manual play possible?**
A: Yes! You need ~90% accuracy to unlock flag. Achievable with focus and pattern recognition.

**Q: How does the exploit work?**
A: Read VULNERABILITY_ANALYSIS.md for deep technical explanation.

---

## 🎯 Challenge Completion Checklist

### Basic (Player)
- [ ] Read QUICK_REFERENCE.md
- [ ] Install and run server
- [ ] Play manually
- [ ] Attempt to reach 90%+
- [ ] Read WALKTHROUGH.md if stuck

### Intermediate (Hacker)
- [ ] Complete basic tasks
- [ ] Read README.md
- [ ] Run solver.py
- [ ] Understand exploit chain
- [ ] Read VULNERABILITY_ANALYSIS.md (at least executive summary)

### Advanced (Expert)
- [ ] Complete intermediate tasks
- [ ] Read full VULNERABILITY_ANALYSIS.md
- [ ] Study and understand solver.py code line-by-line
- [ ] Propose at least 3 remediation strategies
- [ ] Create modified version with different approach
- [ ] Document your modifications

---

## 🔗 Navigation Quick Links

| What I Want | Where to Go |
|-------------|------------|
| To play the game | QUICK_REFERENCE.md → app.py |
| To understand the game | README.md |
| Step-by-step tutorial | WALKTHROUGH.md |
| To exploit it | QUICK_REFERENCE.md → solver.py |
| Why the exploit works | VULNERABILITY_ANALYSIS.md |
| Command reference | QUICK_REFERENCE.md |
| Project status | PROJECT_SUMMARY.md |
| Troubleshooting | QUICK_REFERENCE.md or WALKTHROUGH.md |
| Learning outcomes | Project description or README.md |

---

## 🌟 Key Concepts

### Perceptual Hashing
Images can be identified by visual similarity (perceptual hash) even if binary content changes (MD5 differs). This is the core vulnerability.

### Information Leakage
API feedback about aggregate accuracy allows attackers to determine individual image verdicts through differential analysis.

### Fixed Dataset
Only 30 unique images exist, enabling practical hash-based correlation across sessions.

### Compound Vulnerabilities
No single vulnerability is fatal, but together they enable complete exploitation.

---

## 📞 Support Channels

1. **Quick answer?** → QUICK_REFERENCE.md
2. **How-to question?** → WALKTHROUGH.md
3. **Technical issue?** → VULNERABILITY_ANALYSIS.md
4. **Installation problem?** → README.md or QUICK_REFERENCE.md troubleshooting
5. **Want to learn more?** → Read relevant documentation for your skill level

---

## 🏆 Success Definitions

**Player Success:** Achieve ≥90% accuracy and unlock flag

**Hacker Success:** Run solver.py and achieve ≥90% automatically

**Learner Success:** Understand and explain the exploitation chain

**Expert Success:** Create improved version or novel exploitation method

---

**Welcome to the Sic Mundus Vision challenge!**

*"A beginning is the end's beginning." - Dark TV Series*

Start with [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for fastest path forward → ⚡
