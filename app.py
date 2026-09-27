from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os

app = Flask(__name__)
CORS(app)

client = anthropic.Anthropic(api_key=os.environ.get("CLAUDE_API_KEY"))

SYSTEM_PROMPT = """Jesteś pomocnym asystentem AI o nazwie SI Automation. Odpowiadasz po polsku, krótko i konkretnie."""

@app.route("/")
def home():
    return "SI Automation Backend dziala!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    history = data.get("history", [])

    messages = []
    for h in history:
        if h.get("role") in ["user", "assistant"]:
            messages.append({"role": h["role"], "content": h["content"]})

    if not messages or messages[-1]["content"] != user_message:
        messages.append({"role": "user", "content": user_message})

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=messages
        )
        reply = response.content[0].text
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Blad: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
