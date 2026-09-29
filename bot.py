import os
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("BOT_TOKEN")

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

def send_message(chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": "👋 আমাদের Bot-এ স্বাগতম!\n\nনিচের বাটন থেকে আপনার প্রয়োজনীয় লিংকে যান।",
        "reply_markup": keyboard
    }

    requests.post(url, json=data)

def bot_loop():
    offset = 0

    while True:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        params = {"offset": offset, "timeout": 30}

        response = requests.get(url, params=params)
        data = response.json()

        for update in data.get("result", []):
            offset = update["update_id"] + 1

            message = update.get("message", {})
            chat = message.get("chat", {})
            text = message.get("text", "")

            if text == "/start":
                send_message(chat["id"])

        time.sleep(1)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def log_message(self, format, *args):
        pass

import threading

threading.Thread(target=bot_loop, daemon=True).start()

port = int(os.environ.get("PORT", 10000))
server = HTTPServer(("0.0.0.0", port), Handler)
server.serve_forever()
