from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import SRTFormatter
from functools import wraps

app = Flask(__name__)
formatter = SRTFormatter()

def cors_enabled(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        response = f(*args, **kwargs)
        if isinstance(response, str):
            response = app.make_response(response)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return decorated_function

@app.route('/', methods=['GET'])
def home():
    """Home route"""
    return 'Welcome to the Transcript API!'

@app.route('/health', methods=['GET'])
def health():
    """Health check route"""
    return jsonify({'status': 'ok'})

@app.route('/api/transcript/<video_id>', methods=['GET', 'OPTIONS'])
@cors_enabled
def get_transcript(video_id):
    """Get YouTube video transcript in SRT format by video ID"""
    try:
        language = request.args.get('language')

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
        return jsonify({"error": f"Transcript not available: {str(e)}"}), 404
    except Exception as e:
        return jsonify({"error": f"Error fetching transcript: {str(e)}"}), 500

@app.route('/api/transcript', methods=['POST', 'OPTIONS'])
@cors_enabled
def post_transcript():
    """Get YouTube video transcript in SRT format via POST request"""
    try:
        data = request.get_json()
        video_id = data.get('video_id')
        language = data.get('language')

        if not video_id:
            return jsonify({"error": "video_id is required"}), 400

        return get_transcript(video_id)
    except Exception as e:
        return jsonify({"error": f"Error processing request: {str(e)}"}), 500

# This is required for Vercel
app = app