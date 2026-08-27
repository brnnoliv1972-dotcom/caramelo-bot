import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Recupera as chaves salvas nas variáveis de ambiente do Render
ZAPI_INSTANCE_ID = os.environ.get("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.environ.get("ZAPI_TOKEN")


@app.route("/", methods=["GET"])
def home():
    return "Servidor do Caramelo Bot está ativo e rodando!"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    # Exibe no log tudo o que a Z-API enviou
    print("Payload recebido da Z-API:", data)

    if data:
        # Garante que ignora mensagens enviadas pelo próprio robô
        is_from_me = data.get("fromMe", False)

        if not is_from_me:
            phone = data.get("phone")  # Número do remetente

            # Monta a URL de envio da Z-API
            url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"

            payload = {
                "phone": phone,
                "message": "Olá! Seja bem-vindo ao Caramelo Bot. Confira nossas ofertas na Amazon: https://amazon.com.br",
            }

            headers = {"Content-Type": "application/json"}

            # Faz a requisição de envio de volta para a Z-API
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
