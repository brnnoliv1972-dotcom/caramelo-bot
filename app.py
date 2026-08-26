Python
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ZAPI_INSTANCE_ID = os.environ.get("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.environ.get("ZAPI_TOKEN")

# Cole o seu link da Amazon dentro das aspas abaixo:
LINK_AMAZON = "COLE_SEU_LINK_DA_AMAZON_AQUI"

@app.route("/", methods=["GET"])
def home():
    return "Servidor do Caramelo Bot está ativo e rodando!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    if data and not data.get("fromMe", True):
        phone = data.get("phone")
        user_message = data.get("text", {}).get("message", "")
        
        if user_message:
            bot_response = (
                f"Olá! Obrigado pelo contato! 🐶\n\n"
                f"Confira as melhores ofertas e recomendações no nosso link exclusivo da Amazon:\n"
                f"{LINK_AMAZON}\n\n"
                f"Em breve te atendo com mais detalhes!"
            )
            send_zapi_message(phone, bot_response)
            
    return jsonify({"status": "success"}), 200

def send_zapi_message(phone, message):
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"
    headers = {"Content-Type": "application/json"}
    payload = {
        "phone": phone,
        "message": message
    }
    try:
        requests.post(url, json=payload, headers=headers)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
