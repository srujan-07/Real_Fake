#!/bin/bash
# Quick test script for local gunicorn deployment

echo "Testing gunicorn startup..."
gunicorn app:app --bind 127.0.0.1:8000 --workers 2 --timeout 120 --log-level info
