from flask import Flask, request, jsonify
from bot_logic import handle_message

app = Flask(__name__)

@app.route("/")
def home():
    return "AI WhatsApp Automation Server Running"

@app.route("/message", methods=["POST"])
def message():
    data = request.json
    
    client_id = data.get("client_id")
    phone = data.get("phone")
    message_text = data.get("message")
    
    reply = handle_message(client_id, phone, message_text)
    
    return jsonify({"reply": reply})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

