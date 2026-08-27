import base64
import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Credenciais Z-API
INSTANCE_ID = "3F82F1A840F592680627F2CCB21A3920"
INSTANCE_TOKEN = "593C64792C43EADAA3AC305F"
CLIENT_TOKEN = "Fd227d386b55c4977ae1bc922b09cf89eS"

# Configurações do Afiliado e Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
AMAZON_TAG = "102030brn2586-20"
ML_TAG = "102030brn2586-20"  # Substitua pela sua Tag do Mercado Livre quando tiver

# DOMÍNIOS SEGUROS PARA VERIFICAÇÃO ANTIFRAUDE
DOMINIOS_SEGUROS = [
    "amazon.com.br", "mercadolivre.com.br", "mercadolibre.com",
    "shopee.com.br", "magazineluiza.com.br", "casasbahia.com.br"
]

# CATÁLOGO DE PRODUTOS E BUSCAS OFICIAIS
CATALOGO = [
    {
        "nome": "Batedeira Planetária",
        "categoria": "cozinha eletrodomesticos batedeira",
        "link_amazon": f"https://www.amazon.com.br/s?k=batedeira+planetaria&tag={AMAZON_TAG}",
        "link_ml": f"https://lista.mercadolivre.com.br/batedeira-planetaria#matt={ML_TAG}",
    },
    {
        "nome": "Ração para Cães Adultos 15kg",
        "categoria": "petshop pet cao cachorro ração",
        "link_amazon": f"https://www.amazon.com.br/s?k=racao+caes+adultos+15kg&tag={AMAZON_TAG}",
        "link_ml": f"https://lista.mercadolivre.com.br/racao-caes-15kg#matt={ML_TAG}",
    },
    {
        "nome": "Smartphone Samsung Galaxy",
        "categoria": "celular tecnologia eletronicos",
        "link_amazon": f"https://www.amazon.com.br/s?k=smartphone+samsung+galaxy&tag={AMAZON_TAG}",
        "link_ml": f"https://lista.mercadolivre.com.br/samsung-galaxy#matt={ML_TAG}",
    },
    {
        "nome": "Fone de Ouvido Bluetooth Sem Fio",
        "categoria": "fone audio musica eletronicos",
        "link_amazon": f"https://www.amazon.com.br/s?k=fone+de+ouvido+bluetooth&tag={AMAZON_TAG}",
        "link_ml": f"https://lista.mercadolivre.com.br/fone-bluetooth#matt={ML_TAG}",
    },
    {
        "nome": "Parafusadeira e Furadeira a Bateria",
        "categoria": "ferramentas furadeira parafusadeira",
        "link_amazon": f"https://www.amazon.com.br/s?k=parafusadeira+furadeira+bateria&tag={AMAZON_TAG}",
        "link_ml": f"https://lista.mercadolivre.com.br/parafusadeira-bateria#matt={ML_TAG}",
    },
]


def verificar_link_suspeito(texto):
    """Verifica se há um link na mensagem e se ele pertence a uma loja oficial."""
    if "http://" in texto or "https://" in texto:
        eh_seguro = any(dominio in texto.lower() for dominio in DOMINIOS_SEGUROS)
        if not eh_seguro:
            return True  # É um link suspeito!
    return False


def processar_resposta(mensagem_cliente, imagem_bytes=None, mime_type=None):
    if not GEMINI_API_KEY:
        return f"Olá! Confira ofertas seguras na Amazon: https://www.amazon.com.br?tag={AMAZON_TAG}"

    # Verificação Antifraude Direta
    if verificar_link_suspeito(mensagem_cliente):
        return (
            "🚨 *ALERTA DO CARAMELO BOT!* 🐾\n\n"
            "Cuidado! Analisei o link enviado e ele *não pertence a uma loja oficial verificada*. "
            "Pode ser uma tentativa de golpe ou fraude!\n\n"
            "🛡️ *Dica de Segurança:* Nunca digite sua senha ou dados de cartão em sites desconhecidos.\n\n"
            f"Compre com total segurança na loja oficial Amazon: https://www.amazon.com.br?tag={AMAZON_TAG}"
        )

    prompt_texto = f"""
    Você é o Caramelo Bot, o cão farejador de ofertas seguras, simpático, prestativo e divertido.
    Sua missão é recomendar produtos com ótimo preço e PROTEGER os clientes contra fraudes.
    
    Catálogo de ofertas disponíveis:
    {CATALOGO}
    
    Link Geral da Loja Segura: https://www.amazon.com.br?tag={AMAZON_TAG}
    
    Instruções de Resposta:
    1. Sempre use emojis amigáveis (🐾, ⭐️, 🏆, 📦, 🛡️, 👉).
    2. Ao recomendar um produto, inclua informações de reputação simbólicas para reforçar a confiança (ex: ⭐️ Avaliação 4.8/5, 🏆 Vendedor Verificado / Loja Oficial, 📦 Envio Rápido).
    3. Se o cliente perguntar por um produto do catálogo (ex: batedeira, fone, ração, celular), envie o link direto de busca do catálogo com a tag oficial.
    4. Se o cliente pedir Mercado Livre especificamente, monte um link de busca no Mercado Livre (ex: https://lista.mercadolivre.com.br/nome-do-produto#matt={ML_TAG}).
    5. Se o cliente enviar uma FOTO: Identifique o item na imagem, confirme a qualidade e envie o link de busca seguro correspondente.
    
    Mensagem do cliente: "{mensagem_cliente}"
    """

    parts = [{"text": prompt_texto}]

    if imagem_bytes and mime_type:
        img_b64 = base64.b64encode(imagem_bytes).decode("utf-8")
        parts.append({"inline_data": {"mime_type": mime_type, "data": img_b64}})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": parts}]}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        res_json = response.json()

        if "candidates" in res_json and len(res_json["candidates"]) > 0:
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            if "batedeira" in mensagem_cliente.lower():
                return (
                    "Au au! 🐾 Achei as melhores opções de Batedeira Planetária com excelente reputação!\n\n"
                    "⭐️ *Avaliação:* 4.8 / 5.0 (Mais de 1.000 compradores satisfeitos)\n"
                    "🏆 *Vendedor:* Loja Oficial Verificada\n"
                    "📦 *Garantia:* Compra Segura\n\n"
                    f"👉 Confira aqui: https://www.amazon.com.br/s?k=batedeira+planetaria&tag={AMAZON_TAG}"
                )
            return f"Olá! Encontrei ofertas seguras na Amazon: https://www.amazon.com.br?tag={AMAZON_TAG}"
    except Exception as e:
        if "batedeira" in mensagem_cliente.lower():
            return f"Au au! 🐾 Confira opções de Batedeira Planetária em promoção: https://www.amazon.com.br/s?k=batedeira+planetaria&tag={AMAZON_TAG}"
        return f"Olá! Confira ofertas seguras na Amazon: https://www.amazon.com.br?tag={AMAZON_TAG}"


@app.route("/", methods=["GET"])
def home():
    return "Caramelo Bot Antifraude + Visão IA Ativo!"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if data and not data.get("fromMe", False):
        phone = data.get("phone")
        user_message = ""
        imagem_bytes = None
        mime_type = None

        if "text" in data:
            if isinstance(data["text"], dict):
                user_message = data["text"].get("message", "")
            elif isinstance(data["text"], str):
                user_message = data["text"]
        elif "body" in data:
            user_message = str(data.get("body", ""))
        elif "caption" in data:
            user_message = str(data.get("caption", ""))

        if "image" in data:
            image_info = data["image"]
            if isinstance(image_info, dict):
                user_message = image_info.get(
                    "caption", user_message or "O que é este produto da foto?"
                )
                image_url = image_info.get("imageUrl")
                if image_url:
                    try:
                        img_resp = requests.get(image_url, timeout=10)
                        if img_resp.status_code == 200:
                            imagem_bytes = img_resp.content
                            mime_type = image_info.get("mimeType", "image/jpeg")
                    except Exception as e:
                        print(f"Erro imagem: {e}")

        if not user_message and not imagem_bytes:
            user_message = "Olá!"

        resposta_bot = processar_resposta(user_message, imagem_bytes, mime_type)

        url_zapi = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{INSTANCE_TOKEN}/send-text"
        payload_zapi = {"phone": phone, "message": resposta_bot}
        headers_zapi = {
            "Content-Type": "application/json",
            "Client-Token": CLIENT_TOKEN,
        }

        try:
            requests.post(
                url_zapi, json=payload_zapi, headers=headers_zapi, timeout=10
            )
        except Exception as e:
            print(f"Erro Z-API: {e}")

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
