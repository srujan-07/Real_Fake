"""
Sic Mundus Vision - Dark Themed CTF Challenge
Inspired by the TV show "Dark"

A challenge where players must distinguish between real timeline artifacts
and temporal anomalies created by paradoxes.
"""

import os
import uuid
import json
import time
import hashlib
import threading
import logging
from datetime import datetime, timedelta
from pathlib import Path
from io import BytesIO

import numpy as np
import imagehash
from PIL import Image, ImageDraw, ImageFont

from flask import Flask, jsonify, send_file, request, render_template, Response
from functools import wraps

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Configure logging for production
if not app.debug:
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

ARTIFACT_REAL_DIR = Path(__file__).parent / "artifacts" / "real"
ARTIFACT_FAKE_DIR = Path(__file__).parent / "artifacts" / "fake"
FLAG = "CrackOn{Pr3petu4l_hash3s_l00k_c00l}"
CORRECT_LABELS = {}  # Built dynamically from artifact labels
SESSION_TIMEOUT = 3600  # 1 hour
REQUEST_DELAY = 0.05  # Rate limiting: 50ms between requests

# ============================================================================
# SESSION & MEMORY MANAGEMENT
# ============================================================================

class Session:
    """Represents a player's challenge session"""
    def __init__(self, session_id, artifacts_data):
        self.session_id = session_id
        self.artifacts = artifacts_data
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()
    
    def is_expired(self):
        return datetime.now() - self.created_at > timedelta(seconds=SESSION_TIMEOUT)
    
    def update_access_time(self):
        self.last_accessed = datetime.now()

# Global session storage
sessions = {}
session_lock = threading.Lock()

# Rate limiting per IP
last_request_time = {}
rate_limit_lock = threading.Lock()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def cleanup_expired_sessions():
    """Remove expired sessions"""
    global sessions
    with session_lock:
        expired = [sid for sid, session in sessions.items() if session.is_expired()]
        for sid in expired:
            del sessions[sid]

def rate_limit(func):
    """Decorator to enforce rate limiting"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        ip = request.remote_addr
        current_time = time.time()
        
        with rate_limit_lock:
            last_time = last_request_time.get(ip, 0)
            elapsed = current_time - last_time
            
            if elapsed < REQUEST_DELAY:
                time.sleep(REQUEST_DELAY - elapsed)
            
            last_request_time[ip] = time.time()
        
        return func(*args, **kwargs)
    return wrapper

def get_image_files():
    """Get all image files from real and fake directories"""
    real_images = sorted([f.name for f in ARTIFACT_REAL_DIR.glob("*") 
                         if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
    fake_images = sorted([f.name for f in ARTIFACT_FAKE_DIR.glob("*") 
                         if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
    return real_images, fake_images

def load_image(filepath):
    """Load image from filepath"""
    try:
        img = Image.open(filepath)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        return img
    except Exception as e:
        app.logger.error(f"Failed to load image {filepath}: {e}")
        return None

def compute_perceptual_hash(image):
    """Compute perceptual hash of an image"""
    try:
        # Use average hash as primary perceptual hash
        phash = imagehash.average_hash(image)
        return str(phash)
    except Exception as e:
        app.logger.error(f"Failed to compute hash: {e}")
        return None

def apply_random_transformations(image):
    """
    Apply random transformations to the image to:
    1. Change binary MD5 hash
    2. Keep visual appearance similar (perceptual hash stays close)
    3. Make brute force impossible
    """
    # Convert PIL image to numpy array
    img_array = np.array(image)
    
    # Random JPEG quality degradation
    quality = np.random.randint(75, 96)
    
    # Random brightness adjustment (-15 to +15)
    brightness_shift = np.random.randint(-15, 16)
    img_array = np.clip(img_array.astype(np.int32) + brightness_shift, 0, 255).astype(np.uint8)
    
    # Random slight color shift
    color_shift = np.random.randint(-5, 6, size=3)
    img_array = np.clip(img_array.astype(np.int32) + color_shift, 0, 255).astype(np.uint8)
    
    # Add slight pixel noise
    noise = np.random.normal(0, 2, img_array.shape)
    img_array = np.clip(img_array.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    
    # Convert back to PIL
    transformed_image = Image.fromarray(img_array)
    
    # Apply JPEG compression
    buffer = BytesIO()
    transformed_image.save(buffer, format='JPEG', quality=quality)
    buffer.seek(0)
    transformed_image = Image.open(buffer)
    
    # Add random metadata comment (changes binary but not visual)
    metadata = transformed_image.info
    metadata['comment'] = f"Timeline artifact {uuid.uuid4()}"
    
    return transformed_image, buffer

def initialize_dataset():
    """Initialize the dataset and correct labels mapping"""
    global CORRECT_LABELS
    
    real_images, fake_images = get_image_files()
    
    # Map filenames to correct labels
    for filename in real_images:
        CORRECT_LABELS[filename] = 1  # Real timeline
    
    for filename in fake_images:
        CORRECT_LABELS[filename] = 0  # Temporal anomaly
    
    app.logger.info(f"Initialized dataset with {len(real_images)} real and {len(fake_images)} fake images")
    
    return real_images + fake_images

def build_artifact_list(session_id):
    """Build a shuffled list of artifacts for a session"""
    real_images, fake_images = get_image_files()
    
    if not real_images or not fake_images:
        app.logger.warning("Dataset not properly initialized!")
        return []
    
    all_images = real_images + fake_images
    
    # Shuffle images for this session
    np.random.seed(int(session_id.replace('-', ''), 16) % 2**32)
    shuffled = np.random.permutation(all_images).tolist()
    
    artifacts = []
    for idx, filename in enumerate(shuffled):
        artifact_id = str(uuid.uuid4())
        artifacts.append({
            "artifact_id": artifact_id,
            "url": f"/api/artifact/{artifact_id}",
            "index": idx
        })
    
    return artifacts

# ============================================================================
# ROUTES - FRONTEND
# ============================================================================

@app.route("/")
def index():
    """Serve the main challenge page"""
    return render_template("index.html")

@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@app.route("/api/debug/images", methods=["GET"])
def debug_images():
    """Debug endpoint to check image availability"""
    real_images, fake_images = get_image_files()
    
    return jsonify({
        "real_count": len(real_images),
        "fake_count": len(fake_images),
        "total": len(real_images) + len(fake_images),
        "real_dir_exists": ARTIFACT_REAL_DIR.exists(),
        "fake_dir_exists": ARTIFACT_FAKE_DIR.exists(),
        "real_dir_path": str(ARTIFACT_REAL_DIR),
        "fake_dir_path": str(ARTIFACT_FAKE_DIR),
        "sample_real": real_images[:3] if real_images else [],
        "sample_fake": fake_images[:3] if fake_images else []
    })

# ============================================================================
# API ROUTES - SESSION MANAGEMENT
# ============================================================================

@app.route("/api/timeline/start", methods=["POST"])
@rate_limit
def start_challenge():
    """
    Start a new timeline analysis session
    
    Returns:
    {
        "session_id": "<uuid>",
        "artifacts": [
            {"artifact_id": "...", "url": "/api/artifact/..."},
            ...
        ],
        "total": 30
    }
    """
    cleanup_expired_sessions()
    
    session_id = str(uuid.uuid4())
    artifacts = build_artifact_list(session_id)
    
    # Store artifact mapping for this session
    session_obj = Session(session_id, artifacts)
    
    with session_lock:
        sessions[session_id] = session_obj
    
    # Build response WITHOUT revealing correct answers
    response_artifacts = [
        {
            "artifact_id": artifact["artifact_id"],
            "url": artifact["url"]
        }
        for artifact in artifacts
    ]
    
    return jsonify({
        "session_id": session_id,
        "artifacts": response_artifacts,
        "total": len(response_artifacts)
    }), 200

# ============================================================================
# API ROUTES - IMAGE SERVING
# ============================================================================

# Mapping of artifact_id to (image_type, filename)
artifact_mapping = {}
artifact_mapping_lock = threading.Lock()

@app.route("/api/artifact/<artifact_id>", methods=["GET"])
@rate_limit
def get_artifact(artifact_id):
    """
    Serve an artifact image with random transformations applied.
    
    Each request returns the base image with different random transformations.
    This ensures:
    - Binary MD5 changes on each request
    - Perceptual hash remains similar
    """
    
    try:
        # Find which session and artifact this is
        found_session = None
        artifact_index = None
        
        with session_lock:
            for sid, session_obj in sessions.items():
                for idx, artifact in enumerate(session_obj.artifacts):
                    if artifact["artifact_id"] == artifact_id:
                        found_session = sid
                        artifact_index = idx
                        session_obj.update_access_time()
                        break
                if found_session:
                    break
        
        if not found_session or artifact_index is None:
            app.logger.warning(f"Artifact not found: {artifact_id}")
            return jsonify({"error": "Artifact not found"}), 404
        
        # Get the actual image filename from the session's artifact list
        session_obj = sessions[found_session]
        artifacts = session_obj.artifacts
        
        # Reconstruct which image this artifact corresponds to
        real_images, fake_images = get_image_files()
        all_images = real_images + fake_images
        
        if not all_images:
            app.logger.error("No images found in artifacts directories!")
            return jsonify({"error": "Image dataset not available"}), 500
        
        np.random.seed(int(found_session.replace('-', ''), 16) % 2**32)
        shuffled = np.random.permutation(all_images).tolist()
        
        original_filename = shuffled[artifact_index]
        
        # Determine if real or fake
        if original_filename in real_images:
            image_path = ARTIFACT_REAL_DIR / original_filename
        else:
            image_path = ARTIFACT_FAKE_DIR / original_filename
        
        # Verify image file exists
        if not image_path.exists():
            app.logger.error(f"Image file not found: {image_path}")
            return jsonify({"error": "Image file not found"}), 500
        
        # Load original image
        image = load_image(str(image_path))
        if not image:
            app.logger.error(f"Failed to load image: {image_path}")
            return jsonify({"error": "Failed to load artifact"}), 500
        
        # Apply random transformations
        transformed_image, buffer = apply_random_transformations(image)
        
        # Return the image with proper headers for production
        buffer.seek(0)
        image_data = buffer.read()
        buffer.close()
        
        response = Response(image_data, mimetype='image/jpeg')
        response.headers['Content-Disposition'] = f'inline; filename=artifact_{artifact_id}.jpg'
        response.headers['Content-Length'] = len(image_data)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response
        
    except Exception as e:
        app.logger.error(f"Error serving artifact {artifact_id}: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# ============================================================================
# API ROUTES - SCORING & VERIFICATION
# ============================================================================

@app.route("/api/timeline/verify", methods=["POST"])
@rate_limit
def verify_timeline():
    """
    Verify the player's verdicts against the correct timeline.
    
    Request body:
    {
        "session_id": "<uuid>",
        "timeline": [1, 0, 1, 1, 0, ...]  # 1=real, 0=anomaly
    }
    
    Response:
    {
        "stability": 0.63,
        "correct": 19,
        "total": 30,
        "flag": null or "CrackOn{...}"
    }
    
    IMPORTANT: Do NOT reveal per-image correctness!
    """
    
    data = request.get_json()
    
    if not data or 'session_id' not in data or 'timeline' not in data:
        return jsonify({"error": "Invalid request"}), 400
    
    session_id = data['session_id']
    user_answers = data['timeline']
    
    # Validate session exists
    if session_id not in sessions:
        return jsonify({"error": "Session not found or expired"}), 404
    
    session_obj = sessions[session_id]
    
    # Validate answer count
    if len(user_answers) != len(session_obj.artifacts):
        return jsonify({"error": f"Expected {len(session_obj.artifacts)} answers"}), 400
    
    # Get correct answers based on the session's artifact ordering
    real_images, fake_images = get_image_files()
    all_images = real_images + fake_images
    
    np.random.seed(int(session_id.replace('-', ''), 16) % 2**32)
    shuffled = np.random.permutation(all_images).tolist()
    
    correct_answers = []
    for filename in shuffled:
        correct_answers.append(CORRECT_LABELS.get(filename, 0))
    
    # Calculate score
    correct_count = sum(1 for i in range(len(user_answers)) 
                       if user_answers[i] == correct_answers[i])
    total_count = len(user_answers)
    accuracy = correct_count / total_count
    
    # Prepare response
    response = {
        "stability": round(accuracy, 2),
        "correct": correct_count,
        "total": total_count,
        "flag": None
    }
    
    # Grant flag if accuracy >= 90%
    if accuracy >= 0.90:
        response["flag"] = FLAG
    
    return jsonify(response), 200

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    app.logger.error(f"Server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

# ============================================================================
# INITIALIZATION (runs for both dev and production)
# ============================================================================

# Create directories if they don't exist
ARTIFACT_REAL_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_FAKE_DIR.mkdir(parents=True, exist_ok=True)

# Initialize the application
initialize_dataset()

if __name__ == "__main__":
    # Development server only
    app.logger.info("Sic Mundus Vision challenge initialized (dev mode)")
    app.run(debug=True, host="127.0.0.1", port=5000)
else:
    # Production (gunicorn) initialization
    app.logger.info("Sic Mundus Vision challenge initialized (production mode)")
