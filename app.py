import base64
import os
import requests
import urllib.parse
from flask import Flask, request

app = Flask(__name__)

# Credenciais Z-API
INSTANCE_ID = "3F82F1A840F592680627F2CCB21A3920"
INSTANCE_TOKEN = "593C64792C43EADAA3AC305F"
CLIENT_TOKEN = "Fd227d386b55c4977ae1bc922b09cf89eS"

# Configurações do Afiliado e Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
AMAZON_TAG = "102030brn2586-20"
ML_TAG = "decl20240321112857"

# DOMÍNIOS SEGUROS PARA VERIFICAÇÃO ANTIFRAUDE
DOMINIOS_SEGUROS = [
    "amazon.com.br", "mercadolivre.com.br", "mercadolibre.com",
    "shopee.com.br", "magazineluiza.com.br", "casasbahia.com.br",
    "americanas.com.br", "kabum.com.br"
]

def verificar_link_suspeito(texto):
    """Verifica se há um link na mensagem e se ele pertence a uma loja oficial."""
    if "http://" in texto or "https://" in texto:
        eh_seguro = any(dominio in texto.lower() for dominio in DOMINIOS_SEGUROS)
        if not eh_seguro:
            return True  # É um link suspeito!
    return False

def gerar_links_busca(produto_nome):
    """Gera links dinâmicos de busca para Amazon e Mercado Livre de qualquer produto."""
    termo_encoded = urllib.parse.quote(produto_nome.strip())
    link_amz = f"https://www.amazon.com.br/s?k={termo_encoded}&tag={AMAZON_TAG}"
    link_ml = f"https://lista.mercadolivre.com.br/{termo_encoded}#matt={ML_TAG}"
    return link_amz, link_ml

def processar_resposta(mensagem_cliente, imagem_bytes=None, mime_type=None):
    # 1. VERIFICAÇÃO ANTIFRAUDE DE LINK SUSPEITO
    if verificar_link_suspeito(mensagem_cliente):
        return (
            "🚨 *ALERTA DO CARAMELO BOT!* 🐾\n\n"
            "Cuidado! Analisei o link enviado e ele *não pertence a uma loja oficial verificada*. "
            "Pode ser uma tentativa de golpe ou fraude!\n\n"
            "🛡️ *Dica de Segurança:* Nunca digite sua senha ou dados de cartão em sites desconhecidos.\n\n"
            f"Compre com total segurança na loja oficial Amazon: https://www.amazon.com.br?tag={AMAZON_TAG}"
        )

    # 2. GERAR LINKS DINÂMICOS
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
    
    SEUS LINKS OFICIAIS GERADOS PARA ESTE PRODUTO SÃO:
    - Link Amazon: {amz_direct}
    - Link Mercado Livre: {ml_direct}
    
    INSTRUÇÕES DE RESPOSTA:
    1. Sempre comece com uma saudação alegre de cachorro (ex: "Au au!", "AU AU! PERA AI!").
    2. Apresente SEMPRE os dois links de busca acima (Amazon e Mercado Livre) formatados com clareza.
    3. Adicione elementos simbólicos de confiança para valorizar a busca (ex: ⭐️ Produto de alta avaliação, 🏆 Vendedor Verificado / Loja Oficial, 📦 Envio Garantido).
    4. Mantenha a resposta curta, direta e amigável.
    """

    parts = [{"text": prompt_texto}]

    if imagem_bytes and mime_type:
        img_b64 = base64.b64encode(imagem_bytes).decode("utf-8")
        parts.append({"inline_data": {"mime_type": mime_type, "data": img_b64}})

    # Modelo Gemini 2.5 Flash Atualizado
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
    return "Caramelo Bot Antifraude + Visão IA Ativo!"


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json() or {}

        if not data.get("fromMe", False):
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

            # --- CONFIGURAÇÃO DE ENVIO - EVOLUTION API ---
API_KEY = os.getenv("ZAPI_TOKEN") or os.getenv("EVOLUTION_API_KEY") or os.getenv("ZAPI_CLIENT_TOKEN")

url_zapi = f"{ZAPI_URL}/message/sendText/{ZAPI_INSTANCE}"

headers = {
    "apikey": API_KEY,
    "Content-Type": "application/json"
}

# Limpa o número mantendo apenas dígitos
numero_limpo = "".join(filter(str.isdigit, str(telefone_cliente)))

payload = {
    "number": numero_limpo,
    "text": resposta_do_gemini
}

# Envio da requisição HTTP
response = requests.post(url_zapi, json=payload, headers=headers)

if response.status_code in [200, 201]:
    print("Mensagem enviada com sucesso pela Evolution API!")
else:
    print(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
