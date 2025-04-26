# YouTube Transcript API Server

A lightweight FastAPI server that fetches YouTube video transcripts and returns them in SRT format. Deployed on Vercel.

## Features

- Fetch transcripts from YouTube videos using the video ID
- Support for language selection
- Returns transcripts in SRT format suitable for subtitle applications
- Simple REST API with both GET and POST endpoints
- Vercel deployment ready
- API Key authentication for secure access
- Health check endpoint for monitoring

## Installation

1. Make sure you have Python 3.12+ installed (latest stable version, compatible with Vercel deployment).

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

4. Set up environment variables:
   - Create a `.env` file for local development
   - Set up environment variables in Vercel dashboard for production
   - Required environment variable: `API_KEY` (your secret API key)

## Dependencies

The project uses the following main dependencies:
- FastAPI: Modern web framework for building APIs
- youtube-transcript-api: For fetching YouTube video transcripts
- python-dotenv: For environment variable management

## Project Structure

```
.
├── api/
│   └── index.py      # Main FastAPI application
├── requirements.txt  # Python dependencies
├── vercel.json      # Vercel deployment configuration
└── README.md        # Project documentation
```

## Local Development

For local development, you can run:

```bash
uvicorn api.index:app --reload
```

This will start the server on `http://localhost:8000`.

## API Endpoints

### Public Endpoints

#### Root Endpoint
```
GET /api
```
Returns a welcome message and API information.

Example response:
```json
{
    "message": "Welcome to Zeco YouTube Transcript API",
    "version": "1.0.0",
    "docs": "/docs"
}
```

#### Health Check
```
GET /api/health
```
Returns the health status of the API.

Example response:
```json
{
    "status": "healthy",
    "service": "youtube-transcript-api"
}
```

### Protected Endpoints

All transcript endpoints require API key authentication.

## API Authentication

All API endpoints are protected with API key authentication. To access the API:

1. Include the API key in the request header:
```
X-API-Key: your-api-key-here
```

2. Set up the API key:
   - For local development: Add `API_KEY=your-secret-key` to your `.env` file
   - For production: Add the `API_KEY` environment variable in your Vercel project settings

## API Usage

### GET Endpoint

Fetch a transcript using a GET request:

```
GET /api/transcript/{video_id}?language={language_code}
```

Headers:
```
X-API-Key: your-api-key-here
```

- `video_id`: The YouTube video ID (e.g., "dQw4w9WgXcQ")
- `language`: (Optional) Language code (e.g., "en", "es", "fr")

Example:

```
GET /api/transcript/dQw4w9WgXcQ
```

### POST Endpoint

Fetch a transcript using a POST request:

```
POST /api/transcript
```

Headers:
```
X-API-Key: your-api-key-here
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

- 403: Invalid or missing API key
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
