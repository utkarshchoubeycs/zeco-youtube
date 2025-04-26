from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import SRTFormatter
import uvicorn
from typing import Optional
from pydantic import BaseModel

app = FastAPI(title="YouTube Transcript API", description="API to fetch YouTube video transcripts")

# Add CORS middleware to allow cross-origin requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify exact origins like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscriptRequest(BaseModel):
    video_id: str
    language: Optional[str] = None

# Using the built-in SRTFormatter instead of our custom formatting function
formatter = SRTFormatter()

@app.get("/transcript/{video_id}", response_class=PlainTextResponse)
async def get_transcript(video_id: str, language: Optional[str] = None):
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

@app.post("/transcript", response_class=PlainTextResponse)
async def post_transcript(request: TranscriptRequest):
    """Get YouTube video transcript in SRT format via POST request"""
    return await get_transcript(request.video_id, request.language)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
