# GlenTok

GlenTok is a lightweight, self-hosted alternative to TikTok built with Python and configured to run on port `3003`. Unlike traditional platforms, all video content is managed and uploaded directly on the server backend rather than through the user interface.

## Features
- **Autoscroll** for hands-free playback
- **Up/Down scroll buttons** on either side for an improved mobile experience
- **Shuffle** mode
- **Remote Access ready** (works over your local network or behind a tunnel/reverse proxy)
- **Ad Free** experience (no ads, pop-ups, or algorithms)

## Prerequisites
* **Python:** Ensure you have Python installed on your system.
* **Custom Favicon (Optional):** To display a browser tab icon, place a PNG image named `logo.png` in the root folder alongside `server.py`.
* **Auto-Start (Windows):** GlenTok does not start automatically with your system. To run it on startup, create a shortcut to `start.bat` and place it in your Windows Startup folder (`shell:startup`) or on your desktop.

## How to Install
1. **Download all files** from this GitHub repository (click **Code** > **Download ZIP** and extract it).
2. **Create a folder** named `glentok--server` (e.g., `C:\glentok--server`).
3. **Move all extracted files** (`server.py`, `start.bat`, etc.) into that folder.
4. **Create a subfolder** named `Content` inside `glentok--server` and place your videos in it.
5. **Run `start.bat`** to launch the server.
6. *(Optional)* **Add a PNG file named `logo.png`** to the `glentok--server` folder to use as your browser tab favicon.
  
## Configuration
Before starting the application, configure your target video directory path (default: `C:\glentok-server\Content`):

1. Open `server.py` in your preferred text editor.
2. Navigate to **line 8**.
3. Update the directory path variable to point to your desired local folder.
4. Save the file.

## Usage
1. Start the application by running `start.bat` in the main folder.
2. Once running, open your web browser and navigate to:
   - Local access: `http://localhost:3003`
   - Network access: `http://<your-machine-ip>:3003`

## Remote Access
GlenTok can be accessed remotely over the internet using a **Cloudflare Tunnel** or a reverse proxy such as **Nginx**.

## License
Copyright © 2026 Glens Alarms. Licensed under the [MIT License](LICENSE).

* GlenTok is an independent open-source project and is not affiliated with, endorsed by, or connected to TikTok or ByteDance.
