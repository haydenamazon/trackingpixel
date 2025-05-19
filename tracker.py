from flask import Flask, request, make_response
from datetime import datetime
from io import BytesIO
from PIL import Image
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='tracker.log', level=logging.INFO, format='%(message)s')

@app.route('/pixel/<uid>.png')
def tracking_pixel(uid):
    # Try getting the real IP
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')

    # Dump all headers (for debugging)
    all_headers = dict(request.headers)

    # Build full log entry
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    log_entry = (
        f"[{timestamp}] UID: {uid}\n"
        f"IP: {ip}\n"
        f"User-Agent: {user_agent}\n"
        f"All Headers: {all_headers}\n"
        "------------------------------"
    )

    print(log_entry)
    logging.info(log_entry)

    # Create a 1x1 transparent PNG
    img = Image.new('RGB', (1, 1), (255, 255, 255))
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers.set('Content-Type', 'image/png')
    return response

@app.route('/')
def index():
    return "✅ Tracking Pixel Server is running."

# Optional: Handle favicon requests gracefully
@app.route('/favicon.ico')
def favicon():
    return '', 204
