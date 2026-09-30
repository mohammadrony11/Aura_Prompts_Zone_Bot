import os
import time
import requests
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN পাওয়া যায়নি!")

API = f"https://api.telegram.org/bot{TOKEN}"
CHANNEL = "@ronyeditzone"


# =========================================================
# PHOTO PROMPT
# =========================================================

PHOTO_PROMPT = """Use the uploaded person’s photo as the PRIMARY SUBJECT REFERENCE.

Create an ultra-realistic vertical 9:16 cinematic night portrait matching the reference image’s composition, framing, depth, lighting, and emotional atmosphere.

IDENTITY: Preserve the subject’s exact facial identity, face shape, skin tone, eyes, eyebrows, nose, lips, jawline, hairstyle, and natural features. Do not beautify, redesign, or change the face.

SCENE: Place the primary subject slightly center/right, looking emotionally toward a person standing very close in front of them. Add a SECONDARY FOREGROUND PERSON of the OPPOSITE GENDER—female if subject is male, male if subject is female. Show only their blurred back/shoulder/head in the lower-left foreground.

Use extremely shallow depth of field: primary subject sharp and detailed, foreground person heavily blurred with natural optical bokeh. Dark nighttime background with soft warm golden/orange practical lights and cinematic bokeh.

Give the primary subject a subtle sad, heartbroken expression with watery eyes or gentle tears. Soft low-key lighting, realistic skin texture, natural shadows, cinematic contrast, 50–85mm lens look, realistic focus falloff and filmic color grading.

Ultra-photorealistic, authentic camera optics, natural human proportions, realistic hair and skin, cinematic movie-frame quality.

Do not change identity, distort features, over-smooth skin, sharpen the foreground person, reveal their face clearly, duplicate people, or add text, watermark, logo, or captions."""


# =========================================================
# VIDEO PROMPT
# =========================================================

VIDEO_PROMPT = """Create a highly realistic cinematic video from the provided image, closely matching the provided reference video.

Keep the main subject’s face, identity, hairstyle, clothing and appearance exactly consistent with the input image.

Recreate the same emotional cinematic performance and shot composition: the subject looks emotionally toward the blurred opposite-gender person standing very close in the foreground, with the foreground person heavily out of focus. The subject subtly moves their eyes, blinks naturally, lowers their gaze, then looks back emotionally. Add subtle realistic facial expressions and watery eyes.

Use shallow depth of field, cinematic nighttime lighting, warm golden bokeh, realistic skin texture and natural camera focus.

Then smoothly transition to a slightly wider shot as the subject turns away and slowly walks away, maintaining the same emotional mood.

Natural human movement, realistic cinematic camera motion, smooth focus transitions, photorealistic quality, no face morphing, no identity change, no distorted body or hands, no extra people."""


# =========================================================
# CHANNEL BUTTONS
# =========================================================

KEYBOARD = {
    "inline_keyboard": [
        [
            {
                "text": "➤ COPY HERE PROMPT",
                "callback_data": "photo_prompt"
            }
        ],
        [
            {
                "text": "➤ COPY HERE VIDEO PROMPT",
                "callback_data": "video_prompt"
            }
        ]
    ]
}


# =========================================================
# START
# =========================================================

def send_start(chat_id):

    data = {
        "chat_id": chat_id,
        "text": (
            "👋 AURA PROMPTS-এ স্বাগতম! ✨\n\n"
            "📸 Bot-এ একটি ছবি পাঠালে সেটি Channel-এ পোস্ট করা যাবে।\n\n"
            "নিচের Channel-এ যুক্ত থাকুন 👇"
        ),
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "📢 AURA PROMPTS",
                        "url": "https://t.me/ronyeditzone"
                    }
                ]
            ]
        }
    }

    requests.post(
        f"{API}/sendMessage",
        json=data,
        timeout=20
    )


# =========================================================
# SEND IMAGE TO CHANNEL
# =========================================================

def post_photo_to_channel(file_id):

    caption = """🔥 AI ভাইরাল কান্না করার ভিডিও Prompt! 😢🎬

👦🏻👧🏻 ছেলে-মেয়ে সবাই এই দুইটি Prompt ব্যবহার করতে পারবেন।

📸 Photo Prompt ⬇️⤵️

🎬 Video Prompt ⬇️⤵️
"""

    data = {
        "chat_id": CHANNEL,
        "photo": file_id,
        "caption": caption,
        "reply_markup": KEYBOARD
    }

    response = requests.post(
        f"{API}/sendPhoto",
        json=data,
        timeout=30
    )

    print("CHANNEL POST:", response.text)

    return response.json()


# =========================================================
# SEND PROMPT TO USER
# =========================================================

def send_prompt(chat_id, prompt, title):

    data = {
        "chat_id": chat_id,
        "text": f"{title}\n\n{prompt}"
    }

    response = requests.post(
        f"{API}/sendMessage",
        json=data,
        timeout=30
    )

    print("PROMPT:", response.text)


# =========================================================
# CALLBACK ANSWER
# =========================================================

def answer_callback(callback_id):

    requests.post(
        f"{API}/answerCallbackQuery",
        json={
            "callback_query_id": callback_id,
            "text": "✅ Prompt পাঠানো হয়েছে!"
        },
        timeout=20
    )


# =========================================================
# TELEGRAM BOT
# =========================================================

def telegram_bot():

    try:
        requests.get(
            f"{API}/deleteWebhook",
            params={
                "drop_pending_updates": True
            },
            timeout=20
        )

    except Exception as e:
        print("Webhook Error:", e)


    offset = 0

    print("AURA PROMPTS BOT STARTED!")

    while True:

        try:

            response = requests.get(
                f"{API}/getUpdates",
                params={
                    "offset": offset,
                    "timeout": 30,
                    "allowed_updates": [
                        "message",
                        "callback_query"
                    ]
                },
                timeout=40
            )

            result = response.json()

            if not result.get("ok"):
                print("Telegram Error:", result)
                time.sleep(5)
                continue


            for update in result.get("result", []):

                offset = update["update_id"] + 1


                # =================================================
                # MESSAGE
                # =================================================

                message = update.get("message")

                if message:

                    chat_id = message["chat"]["id"]

                    text = message.get(
                        "text",
                        ""
                    ).strip()


                    # /start
                    if text.startswith("/start"):

                        send_start(chat_id)


                    # PHOTO RECEIVED
                    if message.get("photo"):

                        photos = message["photo"]

                        # সবচেয়ে বড় resolution
                        largest_photo = photos[-1]

                        file_id = largest_photo["file_id"]

                        print(
                            "Photo received:",
                            file_id
                        )


                        result = post_photo_to_channel(
                            file_id
                        )


                        if result.get("ok"):

                            requests.post(
                                f"{API}/sendMessage",
                                json={
                                    "chat_id": chat_id,
                                    "text": (
                                        "✅ তোমার ছবিটি "
                                        "Channel-এ পোস্ট হয়েছে!\n\n"
                                        "📢 @ronyeditzone"
                                    )
                                },
                                timeout=20
                            )

                        else:

                            requests.post(
                                f"{API}/sendMessage",
                                json={
                                    "chat_id": chat_id,
                                    "text": (
                                        "❌ Channel-এ পোস্ট করা যায়নি।\n\n"
                                        "Bot-এর Channel Admin permission "
                                        "চেক করো।"
                                    )
                                },
                                timeout=20
                            )


                # =================================================
                # BUTTON CLICK
                # =================================================

                callback = update.get(
                    "callback_query"
                )

                if callback:

                    callback_id = callback["id"]

                    callback_data = callback.get(
                        "data",
                        ""
                    )

                    user_id = callback["from"]["id"]


                    answer_callback(
                        callback_id
                    )


                    if callback_data == "photo_prompt":

                        send_prompt(
                            user_id,
                            PHOTO_PROMPT,
                            "📸 PHOTO PROMPT"
                        )


                    elif callback_data == "video_prompt":

                        send_prompt(
                            user_id,
                            VIDEO_PROMPT,
                            "🎬 VIDEO PROMPT"
                        )


        except Exception as e:

            print(
                "BOT ERROR:",
                e
            )

            time.sleep(5)


# =========================================================
# RENDER SERVER
# =========================================================

class Handler(
    BaseHTTPRequestHandler
):

    def do_GET(self):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/plain"
        )

        self.end_headers()

        self.wfile.write(
            b"AURA PROMPTS Bot is running!"
        )

    def log_message(
        self,
        format,
        *args
    ):
        pass


def start_server():

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    server = HTTPServer(
        (
            "0.0.0.0",
            port
        ),
        Handler
    )

    print(
        f"Server running on port {port}"
    )

    server.serve_forever()


# =========================================================
# START
# =========================================================

Thread(
    target=telegram_bot,
    daemon=True
).start()

start_server()
