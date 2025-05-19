from flask import Flask, request, send_file
from datetime import datetime
import logging

app = Flask(__name__)

# Logging setup
logging.basicConfig(filename='tracker.log', level=logging.INFO)

@app.route('/pixel/<uid>.png')
def pixel(uid):
    log_entry = f"[{datetime.now()}] UID: {uid}, IP: {request.remote_addr}, Agent: {request.headers.get('User-Agent')}"
    print(log_entry)
    logging.info(log_entry)
    return send_file('1x1.png', mimetype='image/png')

@app.route('/')
def home():
    return "Tracking pixel server is running."
