import base64
import os
import requests
import urllib.parse
from flask import Flask, request

app = Flask(__name__)

# Configurações com fallback e leitura segura de variáveis de ambiente
EVOLUTION_URL = os.environ.get("EVOLUTION_URL", "https://evolution-api-production-5008.up.railway.app").rstrip("/")
EVOLUTION_INSTANCE = os.environ.get("EVOLUTION_INSTANCE", "atendimento")
API_KEY = os.environ.get("API_KEY", "97d3f3aee5196398da165c49b3a5a8fe2d28507ac3742c356fe88c897fec9bcc")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
AMAZON_TAG = "102030brn2586-20"
ML_TAG = "decl20240321112857"

DOMINIOS_SEGUROS = [
    "amazon.com.br", "mercadolivre.com.br", "mercadolibre.com",
    "shopee.com.br", "magazineluiza.com.br", "casasbahia.com.br",
    "americanas.com.br", "kabum.com.br"
]

def verificar_link_suspeito(texto):
    if "http://" in texto or "https://" in texto:
        eh_seguro = any(dominio in texto.lower() for dominio in DOMINIOS_SEGUROS)
        if not eh_seguro:
            return True
    return False

def gerar_links_busca(produto_nome):
    termo_encoded = urllib.parse.quote(produto_nome.strip())
    link_amz = f"https://www.amazon.com.br/s?k={termo_encoded}&tag={AMAZON_TAG}"
    link_ml = f"https://lista.mercadolivre.com.br/{termo_encoded}#matt={ML_TAG}"
    return link_amz, link_ml

def processar_resposta(mensagem_cliente, imagem_bytes=None, mime_type=None):
    if verificar_link_suspeito(mensagem_cliente):
        return (
            "🚨 *ALERTA DO CARAMELO BOT!* 🐾\n\n"
            "Cuidado! Analisei o link enviado e ele *não pertence a uma loja oficial verificada*. "
            "Pode ser uma tentativa de golpe ou fraude!\n\n"
            "🛡️ *Dica de Segurança:* Nunca digite sua senha ou dados de cartão em sites desconhecidos.\n\n"
            f"Compre com total segurança na loja oficial Amazon: https://www.amazon.com.br?tag={AMAZON_TAG}"
        )

    termo_limpo = mensagem_cliente.replace("http://", "").replace("https://", "").strip()
    amz_direct, ml_direct = gerar_links_busca(termo_limpo if termo_limpo else "ofertas")

    if not GEMINI_API_KEY:
        return (
            f"Au au! 🐾 O Caramelo farejou os menores preços pra você!\n\n"
            f"📦 **Opção na Amazon:**\n👉 {amz_direct}\n\n"
            f"🟡 **Opção no Mercado Livre:**\n👉 {ml_direct}\n\n"
            f"🛡️ *Compre com segurança em lojas oficiais!*"
        )

    prompt_texto = f"""
    Você é o Caramelo Bot, o cão farejador de ofertas seguras do Caramelo Shop! Seu tom é simpático, alegre e divertido.
    
    O usuário enviou a seguinte mensagem/produto: "{mensagem_cliente}"
    
    INSTRUÇÕES RÍGIDAS DE FORMATO:
    1. Comece com uma saudação alegre de cachorro (ex: "Au au! 🐾").
    2. Apresente os links de busca abaixo EXATAMENTE UMA VEZ cada:
       - Amazon: {amz_direct}
       - Mercado Livre: {ml_direct}
    3. Mantenha a resposta objetiva e amigável.
    """

    parts = [{"text": prompt_texto}]

    if imagem_bytes and mime_type:
        img_b64 = base64.b64encode(imagem_bytes).decode("utf-8")
        parts.append({"inline_data": {"mime_type": mime_type, "data": img_b64}})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": parts}]}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=12)
        res_json = response.json()

        if "candidates" in res_json and len(res_json["candidates"]) > 0:
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return (
                f"Au au! 🐾 O Caramelo farejou os menores preços pra você!\n\n"
                f"📦 **Opção na Amazon:**\n👉 {amz_direct}\n\n"
                f"🟡 **Opção no Mercado Livre:**\n👉 {ml_direct}\n\n"
                f"🛡️ *Compre com segurança em lojas oficiais!*"
            )
    except Exception as e:
        print(f"Erro na requisição Gemini: {e}")
        return (
            f"Au au! 🐾 O Caramelo farejou os menores preços pra você!\n\n"
            f"📦 **Opção na Amazon:**\n👉 {amz_direct}\n\n"
            f"🟡 **Opção no Mercado Livre:**\n👉 {ml_direct}\n\n"
            f"🛡️ *Compre com segurança em lojas oficiais!*"
        )
        

    termo_limpo = mensagem_cliente.replace("http://", "").replace("https://", "").strip()
    amz_direct, ml_direct = gerar_links_busca(termo_limpo if termo_limpo else "ofertas")

    if not GEMINI_API_KEY:
        return (
            f"Au au! 🐾 O Caramelo farejou os menores preços pra você!\n\n"
            f"📦 **Opção na Amazon:**\n👉 {amz_direct}\n\n"
            f"🟡 **Opção no Mercado Livre:**\n👉 {ml_direct}\n\n"
            f"🛡️ *Compre com segurança em lojas oficiais!*"
        )

    prompt_texto = f"""
    Você é o Caramelo Bot, o cão farejador de ofertas seguras do Caramelo Shop! Seu tom é simpático, alegre e divertido.
    
    O usuário enviou a seguinte mensagem/produto: "{mensagem_cliente}"
    
    INSTRUÇÕES RÍGIDAS DE FORMATO:
    1. Comece com uma saudação alegre de cachorro (ex: "Au au! 🐾").
    2. Apresente os links de busca abaixo EXATAMENTE UMA VEZ cada:
       - Amazon: {amz_direct}
       - Mercado Livre: {ml_direct}
    3. Mantenha a resposta objetiva e amigável.
    """

    parts = [{"text": prompt_texto}]

    if imagem_bytes and mime_type:
        img_b64 = base64.b64encode(imagem_bytes).decode("utf-8")
        parts.append({"inline_data": {"mime_type": mime_type, "data": img_b64}})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": parts}]}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=12)
        res_json = response.json()

        if "candidates" in res_json and len(res_json["candidates"]) > 0:
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return (
                f"Au au! 🐾 O Caramelo farejou os menores preços pra você!\n\n"
                f"📦 **Opção na Amazon:**\n👉 {amz_direct}\n\n"
                f"🟡 **Opção no Mercado Livre:**\n👉 {ml_direct}\n\n"
                f"🛡️ *Compre com segurança em lojas oficiais!*"
            )
    except Exception as e:
        print(f"Erro na requisição Gemini: {e}")
        return (
            f"Au au! 🐾 O Caramelo farejou os menores preços pra você!\n\n"
            f"📦 **Opção na Amazon:**\n👉 {amz_direct}\n\n"
            f"🟡 **Opção no Mercado Livre:**\n👉 {ml_direct}\n\n"
            f"🛡️ *Compre com segurança em lojas oficiais!*"
        )

@app.route("/", methods=["GET"])
def home():
    return "Caramelo Bot Antifraude + IA Ativo!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        raw_payload = request.get_json(silent=True)

        if not raw_payload:
            return "OK", 200

        if isinstance(raw_payload, list):
            if len(raw_payload) == 0:
                return "OK", 200
            data = raw_payload[0]
        elif isinstance(raw_payload, dict):
            data = raw_payload
        else:
            return "OK", 200

        if not isinstance(data, dict):
            return "OK", 200

        sub_data = data.get("data", {})
        if isinstance(sub_data, list):
            sub_data = sub_data[0] if len(sub_data) > 0 and isinstance(sub_data[0], dict) else {}
        if not isinstance(sub_data, dict):
            sub_data = {}

        from_me = data.get("fromMe", False) or sub_data.get("key", {}).get("fromMe", False)
        if from_me:
            return "OK", 200

        key_data = sub_data.get("key", {}) if isinstance(sub_data, dict) else {}
        remote_jid = key_data.get("remoteJid", "") if isinstance(key_data, dict) else ""
        
        phone = data.get("phone") or (str(remote_jid).split("@")[0] if "@" in str(remote_jid) else "")

        if not phone or "status" in str(data.get("event", "")).lower():
            return "OK", 200

        user_message = ""
        message_obj = sub_data.get("message", {}) if isinstance(sub_data, dict) and "message" in sub_data else data
        if isinstance(message_obj, list):
            message_obj = message_obj[0] if len(message_obj) > 0 and isinstance(message_obj[0], dict) else {}

        if isinstance(message_obj, dict):
            if "conversation" in message_obj:
                user_message = message_obj["conversation"]
            elif "extendedTextMessage" in message_obj and isinstance(message_obj["extendedTextMessage"], dict):
                user_message = message_obj["extendedTextMessage"].get("text", "")

        if not user_message and isinstance(data, dict):
            if "text" in data:
                if isinstance(data["text"], dict):
                    user_message = data["text"].get("message", "")
                elif isinstance(data["text"], str):
                    user_message = data["text"]
            elif "body" in data:
                user_message = str(data.get("body", ""))

        if not user_message:
            user_message = "Olá!"

        resposta_bot = processar_resposta(user_message)
        
        url_envio = f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}"

        headers = {
            "apikey": API_KEY,
            "Content-Type": "application/json"
        }

        numero_limpo = "".join(filter(str.isdigit, str(phone)))

        payload_envio = {
            "number": numero_limpo,
            "text": resposta_bot
        }

        try:
            resp_envio = requests.post(url_envio, json=payload_envio, headers=headers, timeout=10)
            print(f"Status do Envio: {resp_envio.status_code}")
        except Exception as err_envio:
            print(f"Erro ao enviar requisição HTTP: {err_envio}")

        return "OK", 200

    except Exception as e:
        print(f"Erro no processamento do webhook: {e}")
        return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
