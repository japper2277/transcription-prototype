#!/usr/bin/env python3
"""
Build script to check dependencies and environment during Vercel build
"""
import sys
import os
import subprocess
import time

def log(message):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] BUILD LOG: {message}")
    sys.stdout.flush()

def main():
    log("Starting build script")
    log(f"Python version: {sys.version}")
    log(f"Working directory: {os.getcwd()}")
    
    # Check if we're in Vercel environment
    if 'VERCEL' in os.environ:
        log("Running in Vercel environment")
        log(f"Vercel region: {os.environ.get('VERCEL_REGION', 'unknown')}")
        log(f"Memory limit: {os.environ.get('AWS_LAMBDA_FUNCTION_MEMORY_SIZE', 'unknown')}MB")
    else:
        log("Running in local environment")
    
    # List files
    log("Files in current directory:")
    for item in os.listdir('.'):
        log(f"  - {item}")
    
    # Check if requirements.txt exists
    if os.path.exists('requirements.txt'):
        log("requirements.txt found:")
        with open('requirements.txt', 'r') as f:
            for line in f:
                log(f"  - {line.strip()}")
    
    # Try importing key dependencies
    log("Testing dependency imports...")
    
    try:
        import fastapi
        log(f"✅ FastAPI version: {fastapi.__version__}")
    except ImportError as e:
        log(f"❌ FastAPI import failed: {e}")
    
    try:
        import whisper
        log(f"✅ Whisper imported successfully")
    except ImportError as e:
        log(f"❌ Whisper import failed: {e}")
    
    try:
        import torch
        log(f"✅ PyTorch version: {torch.__version__}")
        log(f"✅ PyTorch CPU-only: {not torch.cuda.is_available()}")
    except ImportError as e:
        log(f"❌ PyTorch import failed: {e}")
    
    log("Build script completed successfully")

if __name__ == "__main__":
    main()