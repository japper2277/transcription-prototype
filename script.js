// Serverless Function Configuration
const API_BASE_URL = window.location.origin; // Will use the same domain when deployed
const TRANSCRIBE_URL = `${API_BASE_URL}/api/transcribe`;

class TranscriptionTester {
    constructor() {
        this.audioFile = document.getElementById('audioFile');
        this.result = document.getElementById('result');
        this.transcript = document.getElementById('transcript');
        
        this.audioFile.addEventListener('change', this.handleFileUpload.bind(this));
    }

    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        this.showLoading();
        
        try {
            console.log('Starting serverless transcription...');
            
            // Transcription via serverless function
            const transcriptionResult = await this.transcribeWithServerless(file);
            console.log('Transcription completed');
            
            // Display result
            this.showResult(transcriptionResult.transcription);
            
        } catch (error) {
            console.error('Transcription failed:', error);
            this.showError(error.message);
        }
    }

    async transcribeWithServerless(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(TRANSCRIBE_URL, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(`Transcription failed: ${response.status} ${response.statusText} - ${errorData.detail || 'Unknown error'}`);
        }

        return await response.json();
    }

    showLoading() {
        this.result.style.display = 'block';
        this.transcript.innerHTML = 'Processing audio with AI...';
        this.transcript.className = 'loading';
    }

    showResult(text) {
        this.transcript.innerHTML = text || 'No transcript generated.';
        this.transcript.className = '';
    }

    showError(message) {
        this.transcript.innerHTML = `Error: ${message}\n\nMake sure to:\n1. Use a supported audio format (MP3, WAV, M4A, FLAC, etc.)\n2. Check your internet connection\n3. File is not empty or corrupted\n4. File is under 25MB`;
        this.transcript.className = 'error';
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    new TranscriptionTester();
});