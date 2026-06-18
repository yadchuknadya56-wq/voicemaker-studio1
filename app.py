from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # стандартний жіночий голос

@app.route("/")
def home():
    return "VoiceMaker працює!"

@app.route("/speak", methods=["POST"])
def speak():
    text = request.json.get("text")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.content, 200, {
            "Content-Type": "audio/mpeg"
        }
    else:
        return jsonify({"error": response.text}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
