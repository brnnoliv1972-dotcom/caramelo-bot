import os
import requests
from flask import Flask, request
from google import genai

app = Flask(__name__)

# Credenciais Z-API
INSTANCE_ID = "3F82F1A840F592680627F2CCB21A3920"
INSTANCE_TOKEN = "593C64792C43EADAA3AC305F"
CLIENT_TOKEN = "Fd227d386b55c4977ae1bc922b09cf89eS"

# Chave do Gemini e Tag da Amazon
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
AMAZON_TAG = "caramelobot-20"  # Substitua pelo seu ID de Afiliado Amazon

# CATÁLOGO DE PRODUTOS
CATALOGO = [
    {
        "nome": "Batedeira Planetária",
        "categoria": "cozinha eletrodomesticos",
        "link": f"https://www.amazon.com.br/dp/B0765C7ZND?tag={AMAZON_TAG}",
    },
    {
        "nome": "Ração para Cães Adultos 15kg",
        "categoria": "petshop pet cao cachorro ração",
        "link": f"https://www.amazon.com.br/dp/B07BN3NWN2?tag={AMAZON_TAG}",
    },
    {
        "nome": "Smartphone Samsung Galaxy",
        "categoria": "celular tecnologia eletronicos",
        "link": f"https://www.amazon.com.br/dp/B0CX23N8F1?tag={AMAZON_TAG}",
    },
    {
        "nome": "Fone de Ouvido Bluetooth Sem Fio",
        "categoria": "fone audio musica eletronicos",
        "link": f"https://www.amazon.com.br/dp/B0CS3W4P9Q?tag={AMAZON_TAG}",
    },
]


def gerar_resposta_ia(mensagem_cliente):
    """Usa a IA gratuita do Gemini para entender o cliente e responder com o catálogo."""
    if not GEMINI_API_KEY:
        return f"Olá! Confira nossas ofertas na Amazon: https://www.amazon.com.br?tag={AMAZON_TAG}"

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
    Você é o Caramelo Bot, um assistente virtual simpático, divertido e prestativo que ajuda pessoas a encontrarem promoções na Amazon Brasil.
    
    Aqui está o nosso catálogo de ofertas disponíveis no momento:
    {CATALOGO}
    
    Mensagem do cliente: "{mensagem_cliente}"
    
    Instruções:
    1. Responda de forma curta e amigável no WhatsApp.
    2. Se a mensagem tiver relação com algum produto do catálogo, recomende o produto e envie OBRIGATORIAMENTE o link dele.
    3. Se for uma mensagem geral ou item fora do catálogo, seja educado e envie o link geral da loja: https://www.amazon.com.br?tag={AMAZON_TAG}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Erro na chamada do Gemini: {e}")
        return f"Olá! Confira as melhores ofertas na Amazon: https://www.amazon.com.br?tag={AMAZON_TAG}"


@app.route("/", methods=["GET"])
def home():
    return "Caramelo Bot com IA ativo!"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if data:
        is_from_me = data.get("fromMe", False)

        if not is_from_me:
            phone = data.get("phone")
            text_data = data.get("text", {})
            user_message = text_data.get("message", "")

            # Processa a resposta com o Gemini
            resposta_bot = gerar_resposta_ia(user_message)

            url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{INSTANCE_TOKEN}/send-text"

            payload = {"phone": phone, "message": resposta_bot}

            headers = {
                "Content-Type": "application/json",
                "Client-Token": CLIENT_TOKEN,
            }

            try:
                requests.post(url, json=payload, headers=headers, timeout=10)
            except Exception as e:
                print(f"Erro ao enviar mensagem via Z-API: {e}")

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
