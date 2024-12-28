<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Video Downloader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
        }
        input, button {
            padding: 10px;
            margin: 10px;
        }
        #video-container {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Instagram Video Downloader</h1>
    <input type="text" id="urlInput" placeholder="Enter Instagram Video Link" />
    <button onclick="downloadVideo()">Download</button>

    <div id="video-container"></div>

    <script>
        async function downloadVideo() {
            const url = document.getElementById('urlInput').value;
            if (!url) {
                alert('Please enter a valid URL');
                return;
            }

            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/download', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url }),
                });

                const data = await response.json();

                if (response.ok) {
                    document.getElementById('video-container').innerHTML = `
                        <video controls width="600">
                            <source src="${data.video_url}" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                        <p><a href="${data.video_url}" download>Click here to download</a></p>
                    `;
                } else {
                    alert(data.error);
                }
            } catch (err) {
                console.error(err);
                alert('An error occurred. Please try again.');
            }
        }
    </script>
</body>
</html>