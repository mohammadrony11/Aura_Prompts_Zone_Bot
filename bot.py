import os
import time
import requests
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN environment variable পাওয়া যায়নি!")

API = f"https://api.telegram.org/bot{TOKEN}"


KEYBOARD = {
    "inline_keyboard": [
        [
            {
                "text": "📢 টেলিগ্রাম চ্যানেল",
                "url": "https://t.me/ronyeditzone"
            },
            {
                "text": "👤 এডমিন",
                "url": "https://t.me/mohammadrony110"
            }
        ],
        [
            {
                "text": "👥 ফেসবুক গ্রুপ",
                "url": "https://www.facebook.com/share/g/17ZhEcD8S8/"
            },
            {
                "text": "📘 ফেসবুক পেজ",
                "url": "https://www.facebook.com/share/1MMVGtYkhn/"
            }
        ],
        [
            {
                "text": "💬 WhatsApp",
                "url": "https://wa.me/8801340554830"
            }
        ]
    ]
}


def delete_webhook():
    try:
        response = requests.get(
            f"{API}/deleteWebhook",
            params={"drop_pending_updates": True},
            timeout=20
        )
        print("Webhook:", response.text)
    except Exception as e:
        print("Webhook Error:", e)


def send_message(chat_id):
    try:
        data = {
            "chat_id": chat_id,
            "text": (
                "👋 আমাদের Bot-এ স্বাগতম!\n\n"
                "✨ AURA PROMPTS-এ আপনাকে স্বাগতম।\n\n"
                "নিচের বাটনগুলো ব্যবহার করুন 👇"
            ),
            "reply_markup": KEYBOARD
        }

        response = requests.post(
            f"{API}/sendMessage",
            json=data,
            timeout=20
        )

        print("Send message:", response.text)

    except Exception as e:
        print("Send Error:", e)


def telegram_bot():

    # পুরোনো webhook থাকলে সরিয়ে দেবে
    delete_webhook()

    offset = 0

    print("Telegram bot started...")

    while True:
        try:

            response = requests.get(
                f"{API}/getUpdates",
                params={
                    "offset": offset,
                    "timeout": 30,
                    "allowed_updates": ["message"]
                },
                timeout=40
            )

            result = response.json()

            print("Updates:", result)

            if not result.get("ok"):
                print("Telegram API Error:", result)
                time.sleep(5)
                continue

            for update in result.get("result", []):

                offset = update["update_id"] + 1

                message = update.get("message")

                if not message:
                    continue

                chat = message.get("chat", {})
                chat_id = chat.get("id")

                text = message.get("text", "").strip()

                print("Message:", text)

                if text.startswith("/start"):
                    send_message(chat_id)

        except Exception as e:
            print("Bot Error:", e)
            time.sleep(5)


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def log_message(self, format, *args):
        pass


def start_server():

    port = int(os.environ.get("PORT", 10000))

    server = HTTPServer(
        ("0.0.0.0", port),
        Handler
    )

    print(f"Web server running on port {port}")

    server.serve_forever()


# Bot চালু
Thread(
    target=telegram_bot,
    daemon=True
).start()

# Render web server চালু
start_server()
