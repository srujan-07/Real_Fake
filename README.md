# Sic Mundus Vision - Dark Themed CTF Challenge

A sophisticated CTF web challenge inspired by the TV show **Dark**, where players must distinguish between *real timeline artifacts* and *temporal anomalies* using perceptual hashing.

```
╔════════════════════════════════════════════════════════════╗
║     ⟳ SIC MUNDUS VISION ⟳                               ║
║     TIMELINE ARTIFACT ANALYSIS SYSTEM                    ║
║                                                          ║
║  A secret organization analyzes images recovered from   ║
║  different timelines. Some are real artifacts from      ║
║  the original timeline. Others are paradoxes—temporal   ║
║  anomalies created by fractures in spacetime.          ║
║                                                          ║
║  Your task: Determine which artifacts are genuine.     ║
╚════════════════════════════════════════════════════════════╝
```

## 🎯 Challenge Overview

### Story
Sic Mundus, a secret organization, has recovered 30 artifacts from multiple timelines:
- **15 "Real Timeline" artifacts**: Authentic relics from the original timeline
- **15 "Temporal Anomalies"**: Paradoxes created by fractures in spacetime

Players must analyze these artifacts and determine which are authentic and which are paradoxes.

### Features
- **30 artifacts displayed** in a grid interface
- **Dark-themed UI** inspired by bunker computer interfaces
- **Per-image classification**: Mark each as "Real" or "Anomaly"
- **Accuracy-based flag**: Achieve ≥90% accuracy to unlock the flag
- **Rate limiting**: 1 request per second to prevent brute force

### Intended Vulnerability
The challenge intentionally leaks enough information to be **script-solvable using perceptual hashing**:

1. **Binary changes but visual appearance stays similar**
   - Each image request applies random transformations
   - MD5 hash changes on each request
   - But **perceptual hash remains similar**

2. **Fixed dataset across sessions**
   - 30 images: 15 real, 15 fake
   - Images repeat between sessions
   - Artifact IDs change every session

3. **Exploitable by correlating hashes**
   - Solvers can download images from multiple sessions
   - Compute perceptual hashes (aHash, pHash, dHash)
   - Build a hash → verdict mapping
   - Use mapping to solve new sessions with near-perfect accuracy

## 📋 Requirements

- Python 3.8+
- Flask 2.3.3
- Pillow 10.0.0
- NumPy 1.24.3
- imagehash 4.3.1
- requests 2.31.0

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd challenge
pip install -r requirements.txt
```

### 2. Generate Dataset

```bash
python generate_dataset.py
```

This creates 15 "real" images and 15 "fake" images in:
- `artifacts/real/` - Realistic-looking patterns
- `artifacts/fake/` - Artificial/AI-like patterns

### 3. Run the Challenge Server

```bash
python app.py
```

The server will start at `http://127.0.0.1:5000`

### 4. Access the Web Interface

Open your browser to: `http://127.0.0.1:5000`

Click **"BEGIN TIMELINE ANALYSIS"** and classify the 30 artifacts.

Submit your verdict to see your accuracy and (if ≥90%) receive the flag.

## 🎮 How to Play

1. **Start Analysis**: Click "BEGIN TIMELINE ANALYSIS"
2. **Analyze Artifacts**: 30 images appear in a grid
3. **Classify Each**: Mark each image as:
   - ✓ **REAL TIMELINE** - Authentic artifact
   - ✗ **TEMPORAL ANOMALY** - Paradox/Fake
4. **Submit Verdict**: When all classified, submit your analysis
5. **View Results**: See your stability score and accuracy
6. **Unlock Flag**: Achieve ≥90% accuracy to view the flag

## 💾 API Endpoints

### Start Challenge
```http
POST /api/timeline/start
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "artifacts": [
    {
      "artifact_id": "uuid-123",
      "url": "/api/artifact/uuid-123"
    }
  ],
  "total": 30
}
```

### Retrieve Artifact
```http
GET /api/artifact/<artifact_id>
```

**Returns:** JPEG image with random transformations applied

**Transformations:**
- Random JPEG quality (75-95)
- Random brightness shift (-15 to +15)
- Random color shift (-5 to +5)
- Gaussian noise (σ=2)
- Random metadata insertion

### Verify Timeline
```http
POST /api/timeline/verify

{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "timeline": [1, 0, 1, 1, 0, ...]
}
```

**Response:**
```json
{
  "stability": 0.93,
  "correct": 28,
  "total": 30,
  "flag": "CrackOn{Pr3petu4l_hash3s_l00k_c00l}"
}
```

*(Flag only appears if accuracy ≥ 90%)*

## 🔓 Exploitation (Intended Solve)

### Vulnerability Chain

1. **Perceptual Hash Invariance**
   - Binary image hashes change on each request
   - But visual appearance (perceived content) stays similar
   - Perceptual hashes (aHash, pHash, dHash) remain stable

2. **Fixed Dataset**
   - Only 30 images exist (15 real, 15 fake)
   - They repeat across all sessions
   - Solvers can identify same image across sessions via hash

3. **Public Accuracy Feedback**
   - API returns score accuracy
   - Players can determine correctness for individual images by testing

### Exploit Strategy (solver.py)

```python
# 1. Download images from multiple sessions
# 2. Compute perceptual hashes for each
# 3. Probe individual images to determine verdicts
# 4. Build hash -> verdict mapping
# 5. Use mapping to solve new sessions
```

### Running the Solver

```bash
# Probe 3 sessions and solve new session
python solver.py --probe-sessions 3

# Solve with existing mapping
python solver.py --solve-only

# Custom base URL
python solver.py --url http://example.com:5000
```

### Expected Solver Output

```
[Session 1/3]
  Session ID: 550e8400-e29b-41d4-a716-446655440000
  Artifacts: 30
  [1/30] Processing artifact... [PROBED] 1 (96.7%)
  [2/30] Processing artifact... [PROBED] 0 (96.7%)
  ...

[+] Hash mapping complete! Found 30 unique artifacts

[*] Starting and solving new session...
  [1/30] Analyzing... [MATCHED] 1
  [2/30] Analyzing... [MATCHED] 0
  ...
  
[+] RESULT: 28/30 correct (93.3%)
[+] FLAG: CrackOn{Pr3petu4l_hash3s_l00k_c00l}
```

## 📁 Project Structure

```
challenge/
├── app.py                      # Flask backend
├── generate_dataset.py         # Image generation script
├── solver.py                   # Automated solver (exploit)
├── requirements.txt            # Python dependencies
├── artifacts/
│   ├── real/                  # 15 "real" images
│   └── fake/                  # 15 "fake" images
├── templates/
│   └── index.html             # Web interface
└── static/
    └── style.css              # Dark theme styles
```

## 🎨 Frontend Features

- **Dark Terminal Interface**: Black background with green/cyan text
- **Glitch Animations**: Terminal-style effects
- **Real-time Progress**: Visual progress bar
- **Artifact Grid**: 30-image display with classification buttons
- **Responsive Design**: Works on mobile and desktop
- **State Management**: Welcome → Loading → Challenge → Results

### Dark Theme Colors

| Element | Color | Hex |
|---------|-------|-----|
| Primary | Bright Green | #00FF41 |
| Secondary | Yellow | #FFFF00 |
| Tertiary | Cyan | #00FFFF |
| Background | Very Dark Navy | #0A0E27 |
| Text | Light Gray | #E0E0E0 |
| Danger | Red | #FF3333 |

## 🔧 Backend Features

### Session Management
- UUID-based session creation
- Automatic session expiration (1 hour)
- Per-session artifact shuffling
- Rate limiting (1 req/sec per IP)

### Image Transformation
- Random JPEG quality degradation
- Random brightness adjustment
- Random noise injection
- Perceptual hash stability maintained

### Security
- No answer labels exposed
- No dataset filenames revealed in API responses
- Only aggregate accuracy returned
- Metadata hidden from API responses

## 🎓 Learning Resources

### Perceptual Hashing
- **aHash** (Average Hash): Uses average pixel value
- **pHash** (Perceptual Hash): Uses DCT coefficients
- **dHash** (Difference Hash): Uses pixel gradient differences

### Implementation
```python
import imagehash
from PIL import Image

img = Image.open("artifact.jpg")
phash = imagehash.phash(img)        # Perceptual hash
ahash = imagehash.average_hash(img) # Average hash
dhash = imagehash.dhash(img)        # Difference hash
```

## 🚨 Important Notes

- The challenge is **intentionally vulnerable** to perceptual hash correlation
- Binary image changes prevent trivial MD5-based solving
- Rate limiting prevents rapid brute force
- The exploit requires understanding **image processing** and **API patterns**
- **Manual play is also possible** - no automation needed for casual players

## 🏆 Flag

**For ≥90% Accuracy:**
```
CrackOn{Pr3petu4l_hash3s_l00k_c00l}
```

## 📝 License

This challenge is provided for educational purposes in CTF competitions.

---

**Inspired by:** The TV show *Dark* and its themes of parallel timelines, paradoxes, and temporal mysteries.

**Theme Quote:** *"A beginning is the end's beginning."*
