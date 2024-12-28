from flask import Flask, request, jsonify, render_template
import instaloader

app = Flask(__name__)

# Define the function to download the Instagram video
def download_video(url):
    L = instaloader.Instaloader()

    # Log in to Instagram (optional, provide valid credentials if needed)
    try:
        L.login("chitikilamanikanta@gmail.com", "9346044678")  # Provide valid credentials if needed
    except Exception as e:
        return {"error": f"Login failed: {str(e)}"}

    try:
        # Extract the shortcode from the URL for Reels (it will work with posts too)
        post_shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, post_shortcode)

        # Debugging output
        print(f"Post found: {post}")
        
        if post.is_video:
            video_url = post.video_url
            return {"video_url": video_url}
        else:
            return {"error": "No video found at the provided URL"}
    except Exception as e:
        return {"error": f"Error fetching post: {str(e)}"}

# Route for serving the home page (HTML)
@app.route('/')
def home():
    return render_template('index.html')

# API route to handle video download request
@app.route('/api/v1/download', methods=['POST'])
def api_download_video():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    result = download_video(url)
    
    if "video_url" in result:
        return jsonify({"video_url": result["video_url"]}), 200
    else:
        return jsonify({"error": result["error"]}), 400

if __name__ == '__main__':
    app.run(debug=True)
