import os
import requests

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@ronyeditzone"

def send_post():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "🔗 আমাদের চ্যানেল",
                    "url": "https://t.me/ronyeditzone"
                }
            ]
        ]
    }

    data = {
        "chat_id": CHANNEL_ID,
        "text": "👋 আমাদের চ্যানেলে স্বাগতম!",
        "reply_markup": keyboard
    }

    requests.post(url, json=data)

send_post()
