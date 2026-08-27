import base64
import os
import requests
from flask import Flask, request
from google import genai
from google.genai import types

app = Flask(__name__)

# Credenciais Z-API
INSTANCE_ID = "3F82F1A840F592680627F2CCB21A3920"
INSTANCE_TOKEN = "593C64792C43EADAA3AC305F"
CLIENT_TOKEN = "Fd227d386b55c4977ae1bc922b09cf89eS"

# Configurações do Afiliado e Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
AMAZON_TAG = "102030brn2586-20"

# CATÁLOGO DE PRODUTOS
CATALOGO = [
    {
        "nome": "Batedeira Planetária",
        "categoria": "cozinha eletrodomesticos batedeira",
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
    {
        "nome": "Parafusadeira e Furadeira a Bateria",
        "categoria": "ferramentas furadeira parafusadeira",
        "link": f"https://www.amazon.com.br/dp/B0753H4G8X?tag={AMAZON_TAG}",
    },
]


def processar_resposta(mensagem_cliente, imagem_bytes=None, mime_type=None):
    """Processa texto e/ou imagens com o Gemini 2.5 Flash."""
    if not GEMINI_API_KEY:
        return f"Olá! Confira nossas ofertas na Amazon: https://www.amazon.com.br?tag={AMAZON_TAG}"

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
    Você é o Caramelo Bot, um assistente virtual simpático, divertido e prestativo especializado em ofertas da Amazon Brasil.
    
    Catálogo de ofertas em destaque:
    {CATALOGO}
    
    Link Geral da Loja: https://www.amazon.com.br?tag={AMAZON_TAG}
    
    Instruções:
    1. Se o cliente perguntar de algum produto específico (ex: batedeira, fone, ração, celular, parafusadeira), recomende o produto do catálogo e inclua OBRIGATORIAMENTE o link direto dele.
    2. Se o produto não estiver no catálogo, seja amigável, diga que vai procurar as melhores promoções e envie o Link Geral da Loja.
    3. Se o cliente enviar uma FOTO: Identifique o produto na imagem, explique o que é e envie o link do item (ou link geral se não houver no catálogo).
    4. Se o cliente enviar um LINK SUSPEITO pedindo análise: Verifique se é oficial (ex: amazon.com.br). Se for suspeito, alerte sobre fraude/golpe e ofereça o link seguro com a tag oficial.
    
    Mensagem do cliente: "{mensagem_cliente}"
    """

    contents = [prompt]

    if imagem_bytes and mime_type:
        contents.append(
            types.Part.from_bytes(data=imagem_bytes, mime_type=mime_type)
        )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=contents
        )
        return response.text
    except Exception as e:
        print(f"Erro no Gemini: {e}")
        return f"Olá! Encontrei ótimas ofertas na Amazon! Acesse aqui: https://www.amazon.com.br?tag={AMAZON_TAG}"


@app.route("/", methods=["GET"])
def home():
    return "Caramelo Bot Visão + IA Ativo!"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if data and not data.get("fromMe", False):
        phone = data.get("phone")
        user_message = ""
        imagem_bytes = None
        mime_type = None

        # Captura texto da mensagem
        if "text" in data and isinstance(data["text"], dict):
            user_message = data["text"].get("message", "")
        elif "body" in data:
            user_message = data.get("body", "")

        # Captura imagem
        if "image" in data and isinstance(data["image"], dict):
            image_info = data["image"]
            caption = image_info.get("caption")
            if caption:
                user_message = caption
            else:
                user_message = "O que é este produto da foto?"

            image_url = image_info.get("imageUrl")
            if image_url:
                try:
                    img_resp = requests.get(image_url, timeout=10)
                    if img_resp.status_code == 200:
                        imagem_bytes = img_resp.content
                        mime_type = image_info.get("mimeType", "image/jpeg")
                except Exception as e:
                    print(f"Erro ao baixar imagem: {e}")

        if not user_message and not imagem_bytes:
            user_message = "Olá!"

        # Processa resposta no Gemini
        resposta_bot = processar_resposta(
            user_message, imagem_bytes, mime_type
        )

        # Envia de volta para a Z-API
        url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{INSTANCE_TOKEN}/send-text"
        payload = {"phone": phone, "message": resposta_bot}
        headers = {
            "Content-Type": "application/json",
            "Client-Token": CLIENT_TOKEN,
        }

        try:
            requests.post(url, json=payload, headers=headers, timeout=10)
        except Exception as e:
            print(f"Erro ao enviar via Z-API: {e}")

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
