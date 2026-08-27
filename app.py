import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Credenciais da Instância
INSTANCE_ID = "3F82F1A840F592680627F2CCB21A3920"
INSTANCE_TOKEN = "593C64792C43EADAA3AC305F"

# COLE AQUI O CÓDIGO DE SEGURANÇA QUE CHEGOU NO SEU WHATSAPP
CLIENT_TOKEN = "COLE_SEU_CODIGO_AQUI"


@app.route("/", methods=["GET"])
def home():
    return "Servidor do Caramelo Bot está ativo e rodando!"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    print("Payload recebido da Z-API:", data)

    if data:
        is_from_me = data.get("fromMe", False)

        if not is_from_me:
            phone = data.get("phone")

            url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{INSTANCE_TOKEN}/send-text"

            payload = {
                "phone": phone,
                "message": "Olá! Seja bem-vindo ao Caramelo Bot. Confira nossas ofertas na Amazon: https://amazon.com.br",
            }

            # Envia o Client-Token autenticado exigido pela Z-API
            headers = {
                "Content-Type": "application/json",
                "Client-Token": CLIENT_TOKEN,
            }

            try:
                response = requests.post(
                    url, json=payload, headers=headers, timeout=10
                )
                print(f"Status do disparo Z-API: {response.status_code}")
                print(f"Resposta detalhada Z-API: {response.text}")
            except Exception as e:
                print(f"Erro ao tentar enviar mensagem via Z-API: {e}")
        else:
            print("Mensagem ignorada: enviada pelo próprio robô (fromMe=True).")

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
