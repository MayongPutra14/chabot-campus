from flask import Flask, request, jsonify, render_template
from chatbot.engine import ChatbotEngine

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")

# initializing Chabot Engine
chatbot = ChatbotEngine("data/knowledge")

# API FULL SCREEN CHATBOT: METHOD GET
@app.route("/chatbot")
def chatbot_page():
    return render_template("index.html")

# API CHATING: METHOD POST
@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json(silent=True)

    if not data or "message" not in data:
        return jsonify({
            "reply": "Permintaan tidak valid."
        }), 400

    user_message = data["message"].strip()

    if not user_message:
        return jsonify({
            "reply": "Pesan kosong tidak dapat diproses"
            }), 400
    
    bot_reply = chatbot.get_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)