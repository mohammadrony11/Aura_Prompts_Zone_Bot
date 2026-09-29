import os
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@ronyeditzone"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def log_message(self, format, *args):
        pass

def send_post():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "📢 টেলিগ্রাম চ্যানেল", "url": "https://t.me/ronyeditzone"},
                {"text": "👤 এডমিন", "url": "https://t.me/mohammadrony110"}
            ],
            [
                {"text": "👥 ফেসবুক গ্রুপ", "url": "https://www.facebook.com/share/g/17ZhEcD8S8/"},
                {"text": "📘 ফেসবুক পেজ", "url": "https://www.facebook.com/share/1MMVGtYkhn/"}
            ],
            [
                {"text": "💬 WhatsApp", "url": "https://wa.me/8801340554830"}
            ]
        ]
    }

    data = {
        "chat_id": CHANNEL_ID,
        "text": "👋 আমাদের চ্যানেলে স্বাগতম!",
        "reply_markup": keyboard
    }

    response = requests.post(url, json=data)
    print(response.text)

send_post()

port = int(os.environ.get("PORT", 10000))
server = HTTPServer(("0.0.0.0", port), Handler)
server.serve_forever()
