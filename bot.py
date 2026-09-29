import os
import time
import requests
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("BOT_TOKEN")

KEYBOARD = {
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
        "text": "👋 আমাদের Bot-এ স্বাগতম!\n\nনিচের বাটনে ক্লিক করুন 👇",
        "reply_markup": KEYBOARD
    }

    response = requests.post(url, json=data)
    print(response.text)

def telegram_bot():
    offset = 0

    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            params = {
                "offset": offset,
                "timeout": 30
            }

            response = requests.get(url, params=params, timeout=40)
            result = response.json()

            for update in result.get("result", []):
                offset = update["update_id"] + 1

                message = update.get("message")

                if message:
                    text = message.get("text", "")
                    chat_id = message["chat"]["id"]

                    if text == "/start":
                        send_message(chat_id)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def log_message(self, format, *args):
        pass

def start_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

Thread(target=telegram_bot, daemon=True).start()
start_server()
