from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import SRTFormatter
from typing import Optional
import os
from pydantic import BaseModel

app = FastAPI(title="YouTube Transcript API", description="API to fetch YouTube video transcripts")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key security scheme
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == os.getenv("API_KEY"):
        return api_key_header
    raise HTTPException(
        status_code=403,
        detail="Invalid API Key"
    )

class TranscriptRequest(BaseModel):
    video_id: str
    language: Optional[str] = None

# Using the built-in SRTFormatter
formatter = SRTFormatter()

@app.get("/")
async def root():
    """Welcome message"""
    return {
        "message": "Welcome to Zeco YouTube Transcript API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "youtube-transcript-api"
    }

@app.get("/transcript/{video_id}")
async def get_transcript(
    video_id: str,
    language: Optional[str] = None,
    api_key: APIKey = Depends(get_api_key)
):
    """Get YouTube video transcript in SRT format by video ID"""
    try:
        # Get transcript
        if language:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript([language])
            transcript_data = transcript.fetch()
        else:
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Format as SRT using the built-in formatter
        srt_content = formatter.format_transcript(transcript_data)
        return srt_content
        
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        raise HTTPException(
            status_code=404,
            detail=f"Transcript not available: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching transcript: {str(e)}"
        )

@app.post("/transcript")
async def post_transcript(
    request: TranscriptRequest,
    api_key: APIKey = Depends(get_api_key)
):
    """Get YouTube video transcript in SRT format via POST request"""
    return await get_transcript(request.video_id, request.language)

# This is required for Vercel
app = app 