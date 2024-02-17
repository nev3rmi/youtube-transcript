import re
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)


@app.route('/')
def index():
  return 'Hello from Flask!'


@app.route('/transcript', methods=['GET'])
def get_transcript():
  video_url = request.args.get('video_url')
  if not video_url:
    return jsonify({'output': {'error': 'No video URL provided'}}), 400
  video_id = extract_video_id(video_url)
  if not video_id:
    return jsonify({'output': {'error': 'Invalid YouTube URL'}}), 400
  try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return jsonify({'output': transcript}), 200
  except TranscriptsDisabled:
    return jsonify(
        {'output': {
            'error': 'Transcripts are disabled for this video'
        }}), 404
  except NoTranscriptFound:
    return jsonify(
        {'output': {
            'error': 'No transcript found for the provided video ID'
        }}), 404
  except Exception as e:
    return jsonify({'output': {'error': str(e)}}), 500


def extract_video_id(video_url):
  pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n]+)'
  match = re.search(pattern, video_url)
  return match.group(1) if match else None


if __name__ == '__main__':
  # Set up ngrok tunnel to forward to port 5000
  public_url = ngrok.connect(5000)
  print(f"NGROK public URL: {public_url}")
  try:
    # Start the Flask app to listen on all interfaces on port 5000
    # (which is where we've told ngrok to forward to)
    app.run(host='0.0.0.0', port=5000)
  finally:
    # When you kill Flask, kill the ngrok tunnel as well
    ngrok.disconnect(public_url)
