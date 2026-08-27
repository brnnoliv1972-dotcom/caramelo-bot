import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Pegando as variáveis do Render
ZAPI_INSTANCE_ID = os.environ.get("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.environ.get("ZAPI_TOKEN")


@app.route("/", methods=["GET"])
def home():
    return "Servidor do Caramelo Bot está ativo e rodando!"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    # Verifica se a mensagem veio de outra pessoa (não enviada por você)
    if data and not data.get("fromMe", True):
        phone = data.get("phone")  # Número de quem mandou a mensagem

        # URL exata de disparo da Z-API
        url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"

        payload = {
            "phone": phone,
            "message": "Olá! Seja bem-vindo ao Caramelo Bot. Confira nossas ofertas na Amazon: https://amazon.com.br",
        }

        headers = {"Content-Type": "application/json"}

        # Dispara a resposta via Z-API
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status do disparo Z-API: {response.status_code}")
        print(f"Resposta Z-API: {response.text}") print(f"Status do disparo Z-API: {response.status_code}") e print(f"Resposta Z-API: {response.text}")

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
