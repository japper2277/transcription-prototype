#!/usr/bin/env python3
"""
Comprehensive build script to troubleshoot every step of Vercel deployment
"""
import sys
import os
import subprocess
import time
import platform
import psutil
import json

def log(message):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] BUILD LOG: {message}")
    sys.stdout.flush()

def log_separator(title):
    log("=" * 60)
    log(f"  {title}")
    log("=" * 60)

def check_system_info():
    log_separator("SYSTEM INFORMATION")
    log(f"Platform: {platform.platform()}")
    log(f"Architecture: {platform.architecture()}")
    log(f"Machine: {platform.machine()}")
    log(f"Processor: {platform.processor()}")
    log(f"Python version: {sys.version}")
    log(f"Python executable: {sys.executable}")
    log(f"Python path: {sys.path[:3]}...")  # First 3 paths
    
def check_environment():
    log_separator("ENVIRONMENT VARIABLES")
    
    # Vercel-specific variables
    vercel_vars = [
        'VERCEL', 'VERCEL_ENV', 'VERCEL_REGION', 'VERCEL_URL',
        'AWS_LAMBDA_FUNCTION_MEMORY_SIZE', 'AWS_LAMBDA_FUNCTION_TIMEOUT',
        'NODE_ENV', 'PYTHONPATH', 'PATH'
    ]
    
    for var in vercel_vars:
        value = os.environ.get(var, 'NOT SET')
        log(f"{var}: {value}")
    
    log(f"Total environment variables: {len(os.environ)}")

def check_memory_disk():
    log_separator("SYSTEM RESOURCES")
    try:
        # Memory info
        memory = psutil.virtual_memory()
        log(f"Total memory: {memory.total / (1024**3):.2f} GB")
        log(f"Available memory: {memory.available / (1024**3):.2f} GB")
        log(f"Memory usage: {memory.percent}%")
        
        # Disk info
        disk = psutil.disk_usage('/')
        log(f"Total disk: {disk.total / (1024**3):.2f} GB")
        log(f"Free disk: {disk.free / (1024**3):.2f} GB")
        log(f"Disk usage: {(disk.used / disk.total) * 100:.1f}%")
        
        # CPU info
        log(f"CPU cores: {psutil.cpu_count()}")
        log(f"CPU usage: {psutil.cpu_percent()}%")
        
    except Exception as e:
        log(f"❌ Resource check failed: {e}")

def check_files_directories():
    log_separator("FILE SYSTEM ANALYSIS")
    log(f"Working directory: {os.getcwd()}")
    
    # List all files and directories
    log("Files in root directory:")
    try:
        for item in sorted(os.listdir('.')):
            path = os.path.join('.', item)
            if os.path.isfile(path):
                size = os.path.getsize(path)
                log(f"  📄 {item} ({size} bytes)")
            else:
                log(f"  📁 {item}/")
    except Exception as e:
        log(f"❌ Directory listing failed: {e}")
    
    # Check for key files
    key_files = ['requirements.txt', 'vercel.json', 'api/transcribe.py', 'build.py']
    log("\nKey files check:")
    for file in key_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            log(f"  ✅ {file} exists ({size} bytes)")
        else:
            log(f"  ❌ {file} missing")

def check_requirements():
    log_separator("REQUIREMENTS.TXT ANALYSIS")
    if os.path.exists('requirements.txt'):
        log("Reading requirements.txt:")
        with open('requirements.txt', 'r') as f:
            requirements = f.readlines()
            for i, line in enumerate(requirements, 1):
                log(f"  {i}: {line.strip()}")
    else:
        log("❌ requirements.txt not found")

def test_pip_install():
    log_separator("PIP INSTALLATION TEST")
    try:
        # Check pip version
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True, timeout=30)
        log(f"Pip version: {result.stdout.strip()}")
        
        # List installed packages
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                              capture_output=True, text=True, timeout=60)
        log("Installed packages:")
        for line in result.stdout.split('\n')[:20]:  # First 20 lines
            if line.strip():
                log(f"  {line.strip()}")
        
    except Exception as e:
        log(f"❌ Pip check failed: {e}")

def test_imports():
    log_separator("DEPENDENCY IMPORT TESTS")
    
    dependencies = [
        ('os', 'Built-in OS module'),
        ('sys', 'Built-in sys module'),
        ('json', 'Built-in JSON module'),
        ('tempfile', 'Built-in tempfile module'),
        ('logging', 'Built-in logging module'),
        ('fastapi', 'FastAPI web framework'),
        ('uvicorn', 'ASGI server'),
        ('whisper', 'OpenAI Whisper'),
        ('torch', 'PyTorch'),
        ('numpy', 'NumPy (from whisper)'),
        ('python-multipart', 'Multipart form data')
    ]
    
    for module_name, description in dependencies:
        try:
            if module_name == 'python-multipart':
                import python_multipart
                module = python_multipart
            else:
                module = __import__(module_name)
            
            version = getattr(module, '__version__', 'Unknown version')
            log(f"  ✅ {module_name}: {description} (v{version})")
            
            # Special checks for key modules
            if module_name == 'torch':
                log(f"    - CUDA available: {hasattr(module, 'cuda') and module.cuda.is_available()}")
                log(f"    - CPU tensors: {hasattr(module, 'zeros')}")
                
            elif module_name == 'whisper':
                log(f"    - Available models: {getattr(module, 'available_models', 'Unknown')()}")
                
        except ImportError as e:
            log(f"  ❌ {module_name}: Import failed - {e}")
        except Exception as e:
            log(f"  ⚠️  {module_name}: Import succeeded but error during checks - {e}")

def test_whisper_model():
    log_separator("WHISPER MODEL TEST")
    try:
        import whisper
        log("Attempting to load Whisper 'base' model...")
        start_time = time.time()
        
        model = whisper.load_model("base")
        load_time = time.time() - start_time
        
        log(f"✅ Whisper model loaded successfully in {load_time:.2f} seconds")
        log(f"Model type: {type(model)}")
        
        # Test model attributes
        if hasattr(model, 'device'):
            log(f"Model device: {model.device}")
        if hasattr(model, 'dims'):
            log(f"Model dimensions: {model.dims}")
            
    except Exception as e:
        log(f"❌ Whisper model test failed: {e}")

def test_fastapi_import():
    log_separator("FASTAPI APPLICATION TEST")
    try:
        from fastapi import FastAPI, UploadFile, File, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
        
        log("✅ FastAPI imports successful")
        
        # Try creating FastAPI app
        app = FastAPI(title="Test API")
        log("✅ FastAPI app creation successful")
        
        # Try adding CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=False,
            allow_methods=["GET", "POST"],
            allow_headers=["*"],
        )
        log("✅ CORS middleware setup successful")
        
    except Exception as e:
        log(f"❌ FastAPI test failed: {e}")

def test_file_operations():
    log_separator("FILE OPERATIONS TEST")
    try:
        import tempfile
        
        # Test temporary file creation
        with tempfile.NamedTemporaryFile(delete=False, suffix='.test') as tmp:
            test_content = b"Test content for file operations"
            tmp.write(test_content)
            temp_path = tmp.name
            
        log(f"✅ Temporary file created: {temp_path}")
        
        # Test file reading
        with open(temp_path, 'rb') as f:
            content = f.read()
            log(f"✅ File read successful: {len(content)} bytes")
        
        # Clean up
        os.remove(temp_path)
        log("✅ File cleanup successful")
        
    except Exception as e:
        log(f"❌ File operations test failed: {e}")

def create_output_directory():
    log_separator("OUTPUT DIRECTORY CREATION")
    try:
        # Create public directory for Vercel
        os.makedirs('public', exist_ok=True)
        log("✅ Created public directory")
        
        # Create a simple index.html
        with open('public/index.html', 'w') as f:
            f.write('''<!DOCTYPE html>
<html>
<head>
    <title>Transcription API</title>
</head>
<body>
    <h1>Comedy Transcription API</h1>
    <p>API is running! Use /api/transcribe to upload audio files.</p>
    <p>Health check: <a href="/health">/health</a></p>
</body>
</html>''')
        log("✅ Created public/index.html")
        
        # List contents of public directory
        if os.path.exists('public'):
            log("Contents of public directory:")
            for item in os.listdir('public'):
                size = os.path.getsize(os.path.join('public', item))
                log(f"  📄 {item} ({size} bytes)")
        
    except Exception as e:
        log(f"❌ Failed to create output directory: {e}")

def final_summary():
    log_separator("BUILD SCRIPT SUMMARY")
    log("Build script execution completed")
    log("Check logs above for any ❌ failures that need attention")
    log("✅ indicates successful operations")
    log("⚠️  indicates warnings or partial failures")
    log("Script finished at: " + time.strftime("%H:%M:%S"))

def main():
    log_separator("STARTING COMPREHENSIVE BUILD ANALYSIS")
    
    try:
        check_system_info()
        check_environment() 
        check_memory_disk()
        check_files_directories()
        check_requirements()
        test_pip_install()
        test_imports()
        test_fastapi_import()
        test_file_operations()
        test_whisper_model()  # This might be slow, do it last
        create_output_directory()  # Create public directory for Vercel
        final_summary()
        
    except KeyboardInterrupt:
        log("❌ Build script interrupted by user")
        sys.exit(1)
    except Exception as e:
        log(f"❌ Build script failed with unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()