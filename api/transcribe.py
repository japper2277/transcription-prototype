from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import whisper
import tempfile
import os
import logging
import sys
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
logger.info("DEPLOYMENT: Starting FastAPI app initialization...")
app = FastAPI(title="Comedy Transcription API")
logger.info("DEPLOYMENT: FastAPI app initialized successfully")
logger.info(f"DEPLOYMENT: Running on Python {sys.version}")
logger.info(f"DEPLOYMENT: Working directory: {os.getcwd()}")

# Add CORS middleware
logger.info("DEPLOYMENT: Adding CORS middleware...")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
logger.info("DEPLOYMENT: CORS middleware added successfully")

# Load Whisper model (this happens once when the serverless function starts)
model = None

def get_model():
    global model
    if model is None:
        logger.info("DEPLOYMENT: Loading Whisper model...")
        start_time = time.time()
        model = whisper.load_model("base")
        load_time = time.time() - start_time
        logger.info(f"DEPLOYMENT: Whisper model loaded successfully in {load_time:.2f}s")
        logger.info(f"DEPLOYMENT: Model device: {getattr(model, 'device', 'unknown')}")
    return model

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Comedy Transcription API", "status": "running"}

@app.post("/api/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    logger.info("Transcribe endpoint accessed")
    if not file:
        logger.error("No file uploaded")
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Check file type
    if not file.content_type or not file.content_type.startswith('audio/'):
        # Allow common audio extensions even if content_type is wrong
        allowed_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.webm']
        if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Please upload an audio file (MP3, WAV, M4A, FLAC, OGG, WEBM)"
            )
    
    temp_path = None
    try:
        logger.info(f"Processing file: {file.filename}")
        
        # Get the Whisper model
        whisper_model = get_model()
        
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="File is empty")
            
            tmp.write(content)
            temp_path = tmp.name
        
        logger.info(f"File saved to {temp_path}, starting transcription...")
        
        # Transcribe the audio file
        result = whisper_model.transcribe(temp_path)
        
        logger.info("Transcription completed successfully")
        
        return {
            "filename": file.filename,
            "transcription": result["text"],
            "language": result.get("language", "unknown"),
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
        
    finally:
        # Clean up temporary file
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
                logger.info(f"Cleaned up temporary file: {temp_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up temp file {temp_path}: {e}")

@app.get("/health")
async def health_check():
    logger.info("Health check accessed")
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }