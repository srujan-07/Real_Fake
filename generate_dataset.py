#!/usr/bin/env python3
"""
Image dataset generator for Sic Mundus Vision challenge.

Generates 15 "real" images and 15 "fake" images using:
- PIL for real images (noise, patterns)
- PIL for fake images (AI-like patterns, distortions)
"""

import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
from pathlib import Path

# Configuration
REAL_DIR = Path(__file__).parent / "artifacts" / "real"
FAKE_DIR = Path(__file__).parent / "artifacts" / "fake"
NUM_REAL = 15
NUM_FAKE = 15
IMAGE_SIZE = (400, 400)


def create_real_image(index):
    """Generate a 'real' image - realistic looking patterns or photographs"""
    img = Image.new('RGB', IMAGE_SIZE, color=(30, 30, 40))
    draw = ImageDraw.Draw(img)
    
    # Create various realistic-looking patterns
    if index % 5 == 0:
        # Landscape-like
        for y in range(IMAGE_SIZE[1]):
            color_val = 50 + int(100 * np.sin(y / 50 + index))
            draw.line([(0, y), (IMAGE_SIZE[0], y)], 
                     fill=(color_val, color_val + 20, color_val + 40))
    
    elif index % 5 == 1:
        # Circular patterns (bokeh-like)
        for _ in range(random.randint(5, 15)):
            center = (random.randint(0, IMAGE_SIZE[0]), 
                     random.randint(0, IMAGE_SIZE[1]))
            radius = random.randint(20, 80)
            color = (random.randint(100, 255), 
                    random.randint(100, 255), 
                    random.randint(100, 255))
            draw.ellipse([center[0] - radius, center[1] - radius,
                         center[0] + radius, center[1] + radius],
                        fill=color, outline=color)
    
    elif index % 5 == 2:
        # Fractal-like structure
        def draw_fractal(x, y, size, depth):
            if depth == 0:
                return
            color = (100 + depth * 10, 100 + depth * 10, 150 + depth * 10)
            draw.rectangle([x, y, x + size, y + size], outline=color)
            if size > 10:
                new_size = size // 2
                draw_fractal(x, y, new_size, depth - 1)
                draw_fractal(x + new_size, y, new_size, depth - 1)
                draw_fractal(x, y + new_size, new_size, depth - 1)
                draw_fractal(x + new_size, y + new_size, new_size, depth - 1)
        
        draw_fractal(50, 50, 300, 4)
    
    elif index % 5 == 3:
        # Wave patterns
        for x in range(IMAGE_SIZE[0]):
            y = int(IMAGE_SIZE[1] / 2 + 50 * np.sin(x / 30 + index))
            color_val = 100 + int(100 * np.cos(x / 50))
            draw.point((x, y), fill=(color_val, color_val, color_val + 50))
    
    else:
        # Random noise (photographic texture)
        pixels = np.array(img)
        noise = np.random.normal(0, 40, pixels.shape)
        pixels = np.clip(pixels.astype(np.int32) + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(pixels)
    
    # Add slight blur for realism
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    
    # Adjust brightness and contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(random.uniform(0.8, 1.2))
    
    return img


def create_fake_image(index):
    """Generate a 'fake' image - artificial or AI-like patterns"""
    img = Image.new('RGB', IMAGE_SIZE, color=(50, 50, 50))
    draw = ImageDraw.Draw(img)
    
    # Create artificial/uncanny patterns
    if index % 5 == 0:
        # Perfect geometric grid (unrealistic)
        cell_size = 20
        for x in range(0, IMAGE_SIZE[0], cell_size):
            for y in range(0, IMAGE_SIZE[1], cell_size):
                color = (100 + (x // cell_size) * 5, 
                        100 + (y // cell_size) * 5, 150)
                draw.rectangle([x, y, x + cell_size, y + cell_size], 
                             outline=color, fill=color)
    
    elif index % 5 == 1:
        # Repeating symmetrical patterns (too perfect)
        quarter = IMAGE_SIZE[0] // 4
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
        for i in range(5):
            radius = 150 - i * 30
            center = (IMAGE_SIZE[0] // 2, IMAGE_SIZE[1] // 2)
            draw.ellipse([center[0] - radius, center[1] - radius,
                         center[0] + radius, center[1] + radius],
                        outline=colors[i % 3])
    
    elif index % 5 == 2:
        # Glitchy lines (AI artifact-like)
        for _ in range(20):
            x1 = random.randint(0, IMAGE_SIZE[0])
            y1 = random.randint(0, IMAGE_SIZE[1])
            x2 = x1 + random.randint(-50, 50)
            y2 = y1 + random.randint(-50, 50)
            color = (random.choice([0, 255]), 
                    random.choice([0, 255]), 
                    random.choice([0, 255]))
            draw.line([(x1, y1), (x2, y2)], fill=color, width=3)
    
    elif index % 5 == 3:
        # Unnatural color blocks
        block_size = 50
        for x in range(0, IMAGE_SIZE[0], block_size):
            for y in range(0, IMAGE_SIZE[1], block_size):
                color = (random.randint(200, 255), 
                        random.randint(0, 100), 
                        random.randint(200, 255))
                draw.rectangle([x, y, x + block_size, y + block_size], 
                             fill=color)
    
    else:
        # Procedural haxagon pattern (unnatural)
        size = 40
        for y in range(0, IMAGE_SIZE[1], size):
            for x in range(0, IMAGE_SIZE[0], size):
                points = [(x + size//2, y),
                         (x + size, y + size//4),
                         (x + size, y + 3*size//4),
                         (x + size//2, y + size),
                         (x, y + 3*size//4),
                         (x, y + size//4)]
                color = (100 + (x % 255), 100 + (y % 255), 150)
                draw.polygon(points, fill=color)
    
    # Add digital-looking noise
    pixels = np.array(img)
    noise = np.random.normal(0, 15, pixels.shape)
    pixels = np.clip(pixels.astype(np.int32) + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(pixels)
    
    return img


def generate_dataset():
    """Generate the complete dataset"""
    
    # Ensure directories exist
    REAL_DIR.mkdir(parents=True, exist_ok=True)
    FAKE_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating {NUM_REAL} 'real' images...")
    for i in range(NUM_REAL):
        img = create_real_image(i)
        filename = REAL_DIR / f"real_{i:02d}.jpg"
        img.save(filename, quality=90)
        print(f"  ✓ {filename.name}")
    
    print(f"\nGenerating {NUM_FAKE} 'fake' images...")
    for i in range(NUM_FAKE):
        img = create_fake_image(i)
        filename = FAKE_DIR / f"fake_{i:02d}.jpg"
        img.save(filename, quality=90)
        print(f"  ✓ {filename.name}")
    
    print(f"\nDataset generation complete!")
    print(f"Real images: {list(REAL_DIR.glob('*.jpg'))}")
    print(f"Fake images: {list(FAKE_DIR.glob('*.jpg'))}")


if __name__ == "__main__":
    generate_dataset()
