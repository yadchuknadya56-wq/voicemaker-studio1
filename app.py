from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"

@app.route("/")
def home():
    return """
    <h1>VoiceMaker</h1>
    <textarea id="text" rows="5" cols="40"></textarea><br>
    <button onclick="speak()">Озвучити</button>

    <script>
    async function speak() {
        const text = document.getElementById('text').value;

        const res = await fetch('/speak', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text})
        });

        const audioBlob = await res.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
    }
    </script>
    """

@app.route("/speak", methods=["POST"])
def speak():
    text = request.json["text"]

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2"
    }

    r = requests.post(url, json=data, headers=headers)

    if r.status_code == 200:
        return r.content, 200, {"Content-Type": "audio/mpeg"}
    else:
        return jsonify({"error": r.text}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
