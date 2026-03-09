#!/usr/bin/env python3
"""
Sic Mundus Vision - Automated Solver

This script demonstrates the intended vulnerability exploitation:
- Directly accesses the artifacts directory (or downloads all images once)
- Computes perceptual hashes for all base images
- Builds a complete mapping of perceptual hash -> correct verdict
- Uses this mapping to solve sessions with near-perfect accuracy

The vulnerability exists because:
1. The base images in artifacts/real and artifacts/fake don't change
2. Server applies random transformations but perceptual hash stays similar
3. Attacker can hash all base images once to build complete mapping
4. Then solve any session by matching perceptual hashes
"""

import requests
import json
import hashlib
import time
from io import BytesIO
from PIL import Image
import imagehash
from pathlib import Path
from typing import Dict, Tuple
import os

# Configuration
BASE_URL = "http://127.0.0.1:5000"
DELAY_BETWEEN_REQUESTS = 0.06  # Respect rate limiting (50ms + safety margin)
ARTIFACTS_DIR = Path(__file__).parent / "artifacts"

# Store hash -> verdict mapping
hash_verdict_map = {}  # phash -> verdict


class PerceptualHashSolver:
    """Solver that uses perceptual hashing to identify images across sessions"""
    
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session_history = []
    
    def download_image(self, url: str) -> Image.Image:
        """Download and return a PIL Image"""
        try:
            # Handle relative URLs by prepending base_url
            if url.startswith('/'):
                url = f"{self.base_url}{url}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            return img
        except Exception as e:
            print(f"[!] Failed to download image from {url}: {e}")
            return None
    
    def compute_hashes(self, image: Image.Image) -> Dict[str, str]:
        """Compute multiple perceptual hashes for an image"""
        if not image:
            return {}
        
        try:
            return {
                'ahash': str(imagehash.average_hash(image)),
                'phash': str(imagehash.phash(image)),
                'dhash': str(imagehash.dhash(image)),
            }
        except Exception as e:
            print(f"[!] Failed to compute hashes: {e}")
            return {}
    
    def start_session(self) -> Tuple[str, list]:
        """Start a new challenge session"""
        try:
            response = requests.post(f"{self.base_url}/api/timeline/start")
            response.raise_for_status()
            data = response.json()
            return data['session_id'], data['artifacts']
        except Exception as e:
            print(f"[!] Failed to start session: {e}")
            return None, None
    
    def build_hash_mapping_from_artifacts(self):
        """
        Build hash mapping directly from the artifacts directory.
        This is the main vulnerability - the base images are accessible.
        """
        global hash_verdict_map
        
        print(f"\n[*] Building hash mapping from local artifacts directory...")
        
        real_dir = ARTIFACTS_DIR / "real"
        fake_dir = ARTIFACTS_DIR / "fake"
        
        if not real_dir.exists() or not fake_dir.exists():
            print(f"[!] Artifacts directory not found at {ARTIFACTS_DIR}")
            print(f"[*] Falling back to API-based learning...")
            return False
        
        # Process real images - store ALL hash types
        real_images = [f for f in real_dir.glob("*") if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
        print(f"  Found {len(real_images)} real artifacts")
        
        for img_path in real_images:
            try:
                img = Image.open(img_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                hashes = self.compute_hashes(img)
                # Store all three hash types
                for hash_type in ['ahash', 'phash', 'dhash']:
                    hash_val = hashes.get(hash_type, '')
                    if hash_val:
                        hash_verdict_map[hash_val] = 1  # Real timeline
            except Exception as e:
                print(f"[!] Failed to process {img_path.name}: {e}")
        
        # Process fake images - store ALL hash types
        fake_images = [f for f in fake_dir.glob("*") if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
        print(f"  Found {len(fake_images)} fake artifacts")
        
        for img_path in fake_images:
            try:
                img = Image.open(img_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                hashes = self.compute_hashes(img)
                # Store all three hash types
                for hash_type in ['ahash', 'phash', 'dhash']:
                    hash_val = hashes.get(hash_type, '')
                    if hash_val:
                        hash_verdict_map[hash_val] = 0  # Temporal anomaly
            except Exception as e:
                print(f"[!] Failed to process {img_path.name}: {e}")
        
        print(f"[+] Built mapping for {len(hash_verdict_map)} unique hashes")
        return True
    
    def solve_session(self, new_session_id: str = None, artifacts_list: list = None) -> Tuple[list, float]:
        """
        Solve a session using the hash mapping without probing.
        
        Returns: (verdicts, estimated_accuracy)
        """
        if new_session_id:
            print(f"\n[*] Solving session {new_session_id}...")
        else:
            print(f"\n[*] Starting and solving new session...")
            new_session_id, artifacts_list = self.start_session()
        
        if not new_session_id:
            return None, 0
        
        verdicts = []
        matched = 0
        unmatched = 0
        
        # Use the provided artifacts or fetch new session
        if not artifacts_list:
            _, artifacts_list = self.start_session()
            if not artifacts_list:
                return None, 0
        
        print(f"  Session ID: {new_session_id}")
        
        for idx, artifact in enumerate(artifacts_list):
            print(f"  [{idx+1}/{len(artifacts_list)}] Analyzing...", end='', flush=True)
            
            image = self.download_image(artifact['url'])
            if not image:
                print(" [FAILED - defaulting to 0]")
                verdicts.append(0)
                unmatched += 1
                continue
            
            hashes = self.compute_hashes(image)
            
            # Use voting across all three hash types for robustness
            votes = []  # List of (verdict, confidence, hash_type)
            
            for hash_type in ['ahash', 'phash', 'dhash']:
                hash_val = hashes.get(hash_type, '')
                if not hash_val:
                    continue
                
                # Try exact match first
                if hash_val in hash_verdict_map:
                    votes.append((hash_verdict_map[hash_val], 1.0, hash_type))
                else:
                    # Try fuzzy matching
                    best_match = None
                    best_distance = float('inf')
                    threshold = 8  # More lenient threshold
                    
                    try:
                        img_hash = imagehash.hex_to_hash(hash_val)
                        for known_hash_str, known_verdict in hash_verdict_map.items():
                            try:
                                known_hash = imagehash.hex_to_hash(known_hash_str)
                                distance = img_hash - known_hash
                                if distance < best_distance:
                                    best_distance = distance
                                    best_match = known_verdict
                            except:
                                continue
                        
                        if best_distance <= threshold:
                            confidence = 1.0 - (best_distance / threshold)
                            votes.append((best_match, confidence, f"{hash_type}~{best_distance}"))
                    except:
                        pass
            
            # Aggregate votes
            if votes:
                # Weight votes by confidence
                real_score = sum(conf for verdict, conf, _ in votes if verdict == 1)
                fake_score = sum(conf for verdict, conf, _ in votes if verdict == 0)
                
                if real_score > fake_score:
                    verdict = 1
                else:
                    verdict = 0
                
                verdicts.append(verdict)
                matched += 1
                vote_summary = ", ".join([f"{ht}→{v}" for v, c, ht in votes[:2]])
                print(f" [VOTES: {vote_summary}] → {verdict}")
            else:
                # No matches found, default to 0
                verdict = 0
                verdicts.append(verdict)
                unmatched += 1
                print(f" [NO MATCH]")
            
            time.sleep(DELAY_BETWEEN_REQUESTS)
        
        print(f"\n  Matched: {matched}/{len(artifacts_list)}")
        print(f"  Unmatched: {unmatched}/{len(artifacts_list)}")
        
        # Submit verdicts
        try:
            response = requests.post(
                f"{self.base_url}/api/timeline/verify",
                json={
                    "session_id": new_session_id,
                    "timeline": verdicts
                }
            )
            result = response.json()
            accuracy = result['stability']
            print(f"\n[+] RESULT: {result['correct']}/{result['total']} correct ({accuracy*100:.1f}%)")
            
            if result['flag']:
                print(f"[+] FLAG: {result['flag']}")
            
            return verdicts, accuracy
        except Exception as e:
            print(f"[!] Failed to submit verdicts: {e}")
            return verdicts, 0
    
    def run_exploit(self):
        """Run the full exploit"""
        print("╔════════════════════════════════════════════════════════════╗")
        print("║     SIC MUNDUS VISION - AUTOMATED SOLVER (Exploit)        ║")
        print("║     Using Perceptual Hashing to Identify Images           ║")
        print("╚════════════════════════════════════════════════════════════╝")
        
        # Build hash mapping from artifacts directory
        success = self.build_hash_mapping_from_artifacts()
        
        if success and hash_verdict_map:
            print("\n" + "="*60)
            self.solve_session()
        else:
            print("[!] Failed to build hash mapping. Cannot solve challenge.")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Sic Mundus Vision Automated Solver"
    )
    parser.add_argument('--url', default='http://127.0.0.1:5000',
                       help='Base URL of the challenge')
    
    args = parser.parse_args()
    
    solver = PerceptualHashSolver(args.url)
    solver.run_exploit()


if __name__ == "__main__":
    main()
