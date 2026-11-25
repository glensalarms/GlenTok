import http.server
import socketserver
import os
import json
import urllib.parse

PORT = 3003
VIDEO_DIR = r"C:\glentok--server\Content"
VALID_EXTS = (".mp4", ".webm", ".mov", ".m4v")

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GlenTok - Beat Your Boredom!</title>
    <link rel="icon" type="image/png" href="/Logo.png">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: #0f0f0f;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100dvh;
            overflow: hidden;
        }
        .top-bar {
            position: absolute;
            top: 16px;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 8px;
            z-index: 10;
            padding: 0 10px;
        }
        .action-btn {
            background-color: rgba(39, 39, 39, 0.85);
            color: #ffffff;
            border: 1px solid #3f3f3f;
            padding: 8px 14px;
            border-radius: 20px;
            font-size: 13px;
            cursor: pointer;
            backdrop-filter: blur(6px);
            transition: border-color 0.2s, background-color 0.2s;
        }
        .action-btn:hover { background-color: #3f3f3f; }
        .carousel-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 24px;
            height: 78dvh;
            width: 100%;
            padding: 0 16px;
        }
        .nav-stack {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .video-wrapper {
            position: relative;
            height: 100%;
            aspect-ratio: 9 / 16;
            max-width: 100%;
            background-color: #000;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.8);
            border: 1px solid #222;
        }
        video {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .nav-btn {
            background-color: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            width: 52px;
            height: 52px;
            font-size: 20px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            transition: background-color 0.2s, transform 0.2s;
            user-select: none;
        }
        .nav-btn:hover { background-color: rgba(255, 255, 255, 0.25); transform: scale(1.08); }
        .nav-btn:active { transform: scale(0.95); }
        .video-info {
            margin-top: 12px;
            font-size: 13px;
            color: #aaaaaa;
            max-width: 340px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            text-align: center;
        }
        footer {
            margin-top: 8px;
            font-size: 11px;
            color: #666666;
            text-align: center;
        }
        @media (max-width: 600px) {
            .carousel-container { gap: 10px; padding: 0 8px; height: 75dvh; }
            .nav-btn { width: 42px; height: 42px; font-size: 16px; }
        }
    </style>
</head>
<body>
    <div class="top-bar">
        <span style="font-weight: bold; font-size: 18px; align-self: center; margin-right: 6px;">Glen<span style="color: #0000FF;">Tok</span></span>
        <button class="action-btn" id="shuffleBtn">Shuffle</button>
        <button class="action-btn" id="refreshBtn">Refresh</button>
        <button class="action-btn" id="autoBtn">Auto: Off</button>
    </div>

    <div class="carousel-container">
        <div class="nav-stack">
            <button class="nav-btn prev-btn" aria-label="Previous">▲</button>
            <button class="nav-btn next-btn" aria-label="Next">▼</button>
        </div>

        <div class="video-wrapper">
            <video id="videoPlayer" controls loop playsinline autoplay></video>
        </div>

        <div class="nav-stack">
            <button class="nav-btn prev-btn" aria-label="Previous">▲</button>
            <button class="nav-btn next-btn" aria-label="Next">▼</button>
        </div>
    </div>

    <div class="video-info" id="videoTitle">Loading videos...</div>

    <footer>
        &copy; 2026 Glens Alarms.</span>
    </footer>

    <script>
        let videos = [];
        let currentIndex = 0;
        let autoAdvance = false;

        const player = document.getElementById("videoPlayer");
        const titleEl = document.getElementById("videoTitle");
        const autoBtn = document.getElementById("autoBtn");

        async function fetchVideos(shouldShuffle = true) {
            const res = await fetch("/api/videos");
            videos = await res.json();
            if (videos.length === 0) {
                titleEl.textContent = "No videos found in folder";
                return;
            }
            if (shouldShuffle) shuffleList();
            currentIndex = 0;
            loadVideo(currentIndex);
        }

        function shuffleList() {
            for (let i = videos.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [videos[i], videos[j]] = [videos[j], videos[i]];
            }
        }

        function loadVideo(index) {
            if (!videos.length) return;
            const filename = videos[index];
            player.src = "/video/" + encodeURIComponent(filename);
            const cleanName = filename.replace(/\\.[^/.]+$/, "");
            titleEl.textContent = `${cleanName} (${index + 1} / ${videos.length})`;
            player.play().catch(() => {});
        }

        function prevVideo() {
            if (!videos.length) return;
            currentIndex = (currentIndex - 1 + videos.length) % videos.length;
            loadVideo(currentIndex);
        }

        function nextVideo() {
            if (!videos.length) return;
            currentIndex = (currentIndex + 1) % videos.length;
            loadVideo(currentIndex);
        }

        document.querySelectorAll(".prev-btn").forEach(btn => btn.onclick = prevVideo);
        document.querySelectorAll(".next-btn").forEach(btn => btn.onclick = nextVideo);

        document.getElementById("shuffleBtn").onclick = () => {
            shuffleList();
            currentIndex = 0;
            loadVideo(currentIndex);
        };

        document.getElementById("refreshBtn").onclick = () => fetchVideos(true);

        autoBtn.onclick = () => {
            autoAdvance = !autoAdvance;
            player.loop = !autoAdvance;
            autoBtn.textContent = autoAdvance ? "Auto: On" : "Auto: Off";
            autoBtn.style.borderColor = autoAdvance ? "#0000FF" : "#3f3f3f";
        };

        player.addEventListener("ended", () => {
            if (autoAdvance) nextVideo();
        });

        document.addEventListener("keydown", (e) => {
            if (e.key === "ArrowLeft" || e.key === "ArrowUp") prevVideo();
            if (e.key === "ArrowRight" || e.key === "ArrowDown") nextVideo();
        });

        fetchVideos(true);
    </script>
</body>
</html>
"""
class RangeHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
            return
        if parsed.path == "/Logo.png":
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logo.png")
            if os.path.isfile(icon_path):
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.end_headers()
                with open(icon_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404)
            return
        if parsed.path == "/api/videos":
            os.makedirs(VIDEO_DIR, exist_ok=True)
            files = [
                f for f in os.listdir(VIDEO_DIR)
                if os.path.isfile(os.path.join(VIDEO_DIR, f)) and f.lower().endswith(VALID_EXTS)
            ]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(files).encode("utf-8"))
            return
        if parsed.path.startswith("/video/"):
            filename = urllib.parse.unquote(parsed.path[len("/video/"):])
            safe_name = os.path.basename(filename)
            filepath = os.path.join(VIDEO_DIR, safe_name)
            if not os.path.isfile(filepath):
                self.send_error(404, "Video not found")
                return
            file_size = os.path.getsize(filepath)
            range_header = self.headers.get("Range")
            ext = os.path.splitext(safe_name)[1].lower()
            mime = {
                ".mp4": "video/mp4",
                ".webm": "video/webm",
                ".mov": "video/quicktime",
                ".m4v": "video/x-m4v"
            }.get(ext, "application/octet-stream")
            if range_header:
                byte_range = range_header.replace("bytes=", "").split("-")
                start = int(byte_range[0]) if byte_range[0] else 0
                end = int(byte_range[1]) if len(byte_range) > 1 and byte_range[1] else file_size - 1
                end = min(end, file_size - 1)
                length = end - start + 1
                self.send_response(206)
                self.send_header("Content-Type", mime)
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                self.send_header("Content-Length", str(length))
                self.end_headers()
                with open(filepath, "rb") as f:
                    f.seek(start)
                    remaining = length
                    while remaining > 0:
                        chunk = f.read(min(65536, remaining))
                        if not chunk:
                            break
                        try:
                            self.wfile.write(chunk)
                        except (BrokenPipeError, ConnectionResetError):
                            break
                        remaining -= len(chunk)
            else:
                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Length", str(file_size))
                self.end_headers()
                with open(filepath, "rb") as f:
                    while True:
                        chunk = f.read(65536)
                        if not chunk:
                            break
                        try:
                            self.wfile.write(chunk)
                        except (BrokenPipeError, ConnectionResetError):
                            break
            return
        self.send_error(404, "Not found")

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == "__main__":
    with ThreadingTCPServer(("", PORT), RangeHTTPRequestHandler) as httpd:
        print(f"GlenTok server running at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
