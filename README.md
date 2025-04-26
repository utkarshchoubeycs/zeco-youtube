# YouTube Transcript API Server

A lightweight FastAPI server that fetches YouTube video transcripts and returns them in SRT format.

## Features

- Fetch transcripts from YouTube videos using the video ID
- Support for language selection
- Returns transcripts in SRT format suitable for subtitle applications
- Simple REST API with both GET and POST endpoints

## Installation

1. Make sure you have Python 3.7+ installed.

2. Create and activate a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS and Linux:
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Server

Start the server with:

```bash
# Make sure your virtual environment is activated
python server.py
```

This will start the server on `http://0.0.0.0:8000`.

## CORS Configuration

The server is configured to allow cross-origin requests from any origin (`*`). For production environments, you should restrict this to specific origins by updating the `allow_origins` parameter in the CORS middleware:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-app-domain.com"],  # Restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## API Usage

### GET Endpoint

Fetch a transcript using a GET request:

```
GET /transcript/{video_id}?language={language_code}
```

- `video_id`: The YouTube video ID (e.g., "dQw4w9WgXcQ")
- `language`: (Optional) Language code (e.g., "en", "es", "fr")

Example:

```
GET /transcript/dQw4w9WgXcQ
```

### POST Endpoint

Fetch a transcript using a POST request:

```
POST /transcript
```

Request body:

```json
{
	"video_id": "dQw4w9WgXcQ",
	"language": "en"
}
```

The `language` field is optional.

## API Documentation

FastAPI generates interactive documentation automatically. You can access it at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Error Handling

The API returns appropriate HTTP status codes:

- 404: Transcript not available
- 500: Server error when fetching transcript

## Example Response

The API returns transcript data in SRT format:

```
1
00:00:00,000 --> 00:00:03,000
Never gonna give you up

2
00:00:03,000 --> 00:00:06,000
Never gonna let you down
```

```

```
