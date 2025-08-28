# Comedy Transcription Prototype

## Purpose
Test if AI transcription creates genuine value for comedians. This is the core hypothesis validation tool.

## Deployment (5 minutes)

1. **Deploy to Vercel:**
   ```bash
   npm install -g vercel
   vercel --prod
   ```
   - Follow prompts to create account/login
   - Get permanent public URL

2. **Alternative - Manual Upload:**
   - Go to https://vercel.com
   - Drag and drop the entire project folder
   - Get instant deployment

3. **No API keys required** - everything runs serverless

## Testing Protocol

### For User Testing:
1. Give user the Vercel URL (e.g., https://your-app.vercel.app)
2. Provide a 30-60 second audio file of comedy material
3. Say: "Show me what you would do with this"
4. **SHUT UP** and observe
5. Time from transcript display to first positive reaction
6. Record exact quotes

### Audio Requirements:
- Format: MP3, WAV, M4A, FLAC, WEBM, etc.
- Length: 30 seconds to 2 minutes optimal  
- Max size: 25MB per file
- Content: Spoken comedy material (jokes, bits, crowd work)

### What to Measure:
- **Time to comprehension**: Seconds from transcript appearing to "aha moment"
- **User quotes**: Exact words when they see value (or don't)
- **Usage patterns**: What they do with the transcript

## Success Criteria
- User says "Oh, cool" or equivalent within 30 seconds of seeing transcript
- They immediately start editing/using the text
- They ask "Can I save this?" or "How do I get more?"

## Failure Criteria  
- Confusion about what they're looking at
- "This is wrong" or accuracy complaints
- No observable change in behavior after seeing transcript

## Notes
- NO authentication required
- NO database - just instant transcription
- NO styling beyond basic readability
- Focus ONLY on the core value moment
- Uses Whisper base model via serverless function
- Completely free - no per-usage costs