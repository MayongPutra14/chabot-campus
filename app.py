from flask import Flask, request, jsonify, render_template
from chatbot.engine import ChatbotEngine

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")

# initializing Chabot Engine
chatbot = ChatbotEngine("data/dataset_poltekintaz.yml")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"reply": "Pesan tidak boleh kosong"}), 400
    
    bot_reply = chatbot.get_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)