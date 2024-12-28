from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# Serve the index.html page when accessing the root URL
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/download', methods=['POST'])
def download_video():
    """
    Extract the video URL from an Instagram link provided by the user.
    """
    try:
        # Extract URL from the request body
        data = request.get_json()  # Use get_json() to parse incoming JSON
        url = data.get('url')
        if not url or 'instagram.com' not in url:
            return jsonify({"error": "Invalid Instagram URL"}), 400

        # Fetch the Instagram page content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch Instagram page"}), 500

        # Parse the HTML to find the video URL
        soup = BeautifulSoup(response.text, 'html.parser')
        video_meta_tag = soup.find('meta', property='og:video')
        if video_meta_tag and video_meta_tag.get('content'):
            video_url = video_meta_tag['content']
            return jsonify({"video_url": video_url}), 200
        else:
            return jsonify({"error": "No video found at the provided URL"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Make sure the 'templates' folder contains index.html
    app.run(debug=True)
