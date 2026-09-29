import os
import time
import requests

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@ronyeditzone"
WHATSAPP = os.getenv("WHATSAPP")

def send_post():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    keyboard = {
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
                    "url": WHATSAPP
                }
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

while True:
    time.sleep(60)
