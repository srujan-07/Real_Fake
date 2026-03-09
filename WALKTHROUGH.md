# Sic Mundus Vision - Installation & Walkthrough Guide

## 📦 Installation

### Prerequisites
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **pip** (usually included with Python)
- **Windows, macOS, or Linux**

### Step 1: Verify Python Installation

```bash
python --version
# Should show: Python 3.x.x
```

### Step 2: Install Dependencies

**Option A: Using setup.bat (Windows)**
```bash
setup.bat
```

**Option B: Manual installation**
```bash
pip install -r requirements.txt
```

**What gets installed:**
- Flask 2.3.3 - Web framework
- Pillow 10.0.0 - Image processing
- NumPy 1.24.3 - Numerical computing
- imagehash 4.3.1 - Perceptual hashing
- requests 2.31.0 - HTTP client

### Step 3: Generate Dataset

If not auto-generated, run:
```bash
python generate_dataset.py
```

This creates:
- `artifacts/real/` - 15 "real" images
- `artifacts/fake/` - 15 "fake" images

### Step 4: Start the Server

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 5: Play the Challenge

Open your browser to: **http://127.0.0.1:5000**

---

## 🎮 Gameplay Walkthrough

### 1. Welcome Screen
```
⟳ SIC MUNDUS VISION ⟳
TIMELINE ARTIFACT ANALYSIS SYSTEM

A secret organization called Sic Mundus has recovered artifacts 
from multiple timelines...

[BEGIN TIMELINE ANALYSIS]
```

Click the **BEGIN TIMELINE ANALYSIS** button to start.

### 2. Loading Phase
The system initializes:
```
SYSTEM STATUS: INITIALIZING ▌▌▌
Initializing temporal protocols...
```

### 3. Challenge Interface
30 images appear in a grid. For each:
- View the artifact
- Click **REAL** if it's an authentic timeline artifact
- Click **ANOMALY** if it's a temporal paradox

Progress bar shows: **X / 30 analyzed**

### 4. Classification Example
```
┌──────────────┐
│              │
│   ARTIFACT   │  <- Random visual patterns or realistic-looking
│   IMAGE      │     textures that might appear real
│              │
├──────────────┤
│ [REAL] [ANOMALY]
│ ✓ REAL
└──────────────┘
```

### 5. Submission
Once all 30 analyzed, click **SUBMIT VERDICT**

### 6. Results Screen
```
╔════════════════════════════════════════╗
║  STABILITY ANALYSIS COMPLETE           ║
║                                      ║
║  TIMELINE STABILITY: 63%              ║
║  CORRECT IDENTIFICATIONS: 19 / 30     ║
║                                      ║
║  Required: 90% | Your accuracy: 63%  ║
║  Timeline stability insufficient.    ║
║  Temporal gateway remains sealed.     ║
║                                      ║
║  [RESTART ANALYSIS]                  ║
╚════════════════════════════════════════╝
```

**If you achieve ≥90% accuracy:**
```
╔════════════════════════════════════════╗
║  TEMPORAL PROTOCOL UNLOCKED:           ║
║                                      ║
║  CrackOn{Pr3petu4l_hash3s_l00k_c00l} ║
╚════════════════════════════════════════╝
```

---

## 🔓 Automated Solve Walkthrough

### Why Manual Play is Hard
- 30 images to classify
- 15 are "real" (realistic patterns)
- 15 are "fake" (artificial patterns)
- Random visual features make guessing ~50% likely
- Need ~90%+ to win

### The Vulnerability
The API leaks enough information to automate solving:

1. **Perceptual hashes remain stable** across requests
2. **Binary image data changes** (MD5 differs)
3. **API returns accuracy** for each submission
4. **Dataset is fixed** (same 30 images always)

### Solution Strategy

#### Phase 1: Probing (Build Hash Map)
```python
# Session 1: Download all 30 images
for artifact in session1.artifacts:
    image = download(artifact.url)
    phash = perceptual_hash(image)
    
    # Test if image is "real" (1) or "fake" (0)
    if test_verdict(1) > test_verdict(0):
        hash_map[phash] = 1
    else:
        hash_map[phash] = 0

# Session 2: Download same images (different IDs)
for artifact in session2.artifacts:
    image = download(artifact.url)
    phash = perceptual_hash(image)
    # phash matches Session 1 image!
    known_verdict = hash_map[phash]
```

#### Phase 2: Solving
```python
# New session: Use hash map
session3_verdicts = []
for artifact in session3.artifacts:
    image = download(artifact.url)
    phash = perceptual_hash(image)
    
    if phash in hash_map:
        verdict = hash_map[phash]
        session3_verdicts.append(verdict)
    else:
        session3_verdicts.append(0)  # Default guess

submit(session3_verdicts)
# Expected result: 90%+
```

### Running the Solver

#### Simple Run (3 probe sessions)
```bash
python solver.py
```

Output:
```
╔════════════════════════════════════════════════════════════╗
║     SIC MUNDUS VISION - AUTOMATED SOLVER (Exploit)        ║
║     Using Perceptual Hashing to Correlate Images          ║
╚════════════════════════════════════════════════════════════╝

[*] Building hash-to-verdict mapping from 3 sessions...

[Session 1/3]
  Session ID: 550e8400-e29b-41d4-a716-446655440000
  Artifacts: 30
  [1/30] Processing artifact... [PROBED] 1 (96.7%)
  [2/30] Processing artifact... [CACHED] 0
  [3/30] Processing artifact... [PROBED] 1 (96.7%)
  ...
  [30/30] Processing artifact... [CACHED] 1

[+] Hash mapping complete! Found 30 unique artifacts

[*] Starting and solving new session...
  Session ID: 550e8400-e29b-41d4-a716-446655440001
  [1/30] Analyzing... [MATCHED] 1
  [2/30] Analyzing... [MATCHED] 0
  ...
  [30/30] Analyzing... [MATCHED] 1
  
[+] RESULT: 28/30 correct (93.3%)
[+] FLAG: CrackOn{Pr3petu4l_hash3s_l00k_c00l}
```

#### Custom Settings
```bash
# Use more probe sessions
python solver.py --probe-sessions 5

# Custom base URL
python solver.py --url http://example.com:5000

# Just solve without probing
python solver.py --solve-only
```

---

## 📊 Technical Details

### Image Transformation Pipeline

When you request an image, the server:

```
1. Load original image (e.g., fake_05.jpg)
   → MD5: a1b2c3d4e5f6...

2. Apply random transformations:
   • JPEG quality: 75-95 (random each request)
   • Brightness: ±15 pixels
   • Color shift: ±5 per channel
   • Gaussian noise: σ=2
   • Metadata insertion

3. Return transformed image
   → MD5: x9y8z7w6v5u4... (DIFFERENT!)
   → Perceptual Hash: SAME or very similar

4. Binary MD5 != Previous MD5 ✓
5. Perceptual Hash ≈ Previous Hash ✓
```

### Perceptual Hash Computation

```python
from PIL import Image
import imagehash

img = Image.open("artifact.jpg")

# These remain stable across requests:
ahash = imagehash.average_hash(img)    # Average Hash
phash = imagehash.phash(img)           # Perceptual Hash  
dhash = imagehash.dhash(img)           # Difference Hash

# These change on each request:
md5(img_bytes)                         # Binary hash
```

Different requests of same image:
```
aHash: 1011010110110101 (same)
pHash: 1011010110110101 (same)
dHash: 1011010110110101 (same)
MD5:   a1b2c3d4 → x9y8z7w6 (different!)
```

---

## 🎓 Learning Outcomes

By completing this challenge, you'll learn:

1. **Perceptual Hashing** - Understanding image similarity without binary comparison
2. **Image Processing** - Transformations that preserve perception but change bytes
3. **API Exploitation** - Finding information leaks in API responses
4. **Pattern Recognition** - Correlating data across multiple requests
5. **Scripting & Automation** - Building automated solvers
6. **CTF Methodology** - Reconnaissance, exploitation, flag extraction

---

## 🐛 Troubleshooting

### Python Not Found
```
'python' is not recognized as an internal or external command
```
**Solution:** Install Python 3.8+ and add to PATH

### Module Not Found
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:** Run `pip install -r requirements.txt`

### Port Already in Use
```
Address already in use
```
**Solution:** 
```bash
# Kill existing process or use different port
# Edit app.py: change port=5000 to port=5001
```

### Dataset Not Generated
```
Artifact not found
```
**Solution:** Run `python generate_dataset.py`

### Slow Solver
```
[*] Building hash-to-verdict mapping from 3 sessions...
```
**Note:** This is normal! Solver respects rate limiting (1 req/sec)

---

## 🔗 Resources

### Perceptual Hashing
- [ImageHash Library](https://github.com/JohannesBuchner/imagehash)
- [aHash vs pHash vs dHash](https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html)

### Flask
- [Flask Documentation](https://flask.palletsprojects.com/)

### CTF Concepts
- [CTF 101](https://ctf101.org/)

---

## 📝 Challenge Statistics

| Metric | Value |
|--------|-------|
| Total Artifacts | 30 |
| Real Artifacts | 15 |
| Fake Artifacts | 15 |
| Min Accuracy for Flag | 90% (27/30) |
| Session Timeout | 1 hour |
| Rate Limit | 1 req/sec per IP |
| Image Size | 400×400px |
| JPEG Quality | 75-95 (random) |

---

**Created for the Dark-themed CTF Challenge Series**

*"A beginning is the end's beginning."*
