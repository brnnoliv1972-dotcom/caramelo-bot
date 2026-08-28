# --- CONFIGURAÇÃO DE ENVIO - EVOLUTION API ---
url_zapi = f"{ZAPI_URL}/message/sendText/{ZAPI_INSTANCE}"

headers = {
    "apikey": ZAPI_CLIENT_TOKEN,
    "Content-Type": "application/json"
}

# Tratamento do número de telefone (apenas números)
numero_limpo = "".join(filter(str.isdigit, str(telefone_cliente)))

payload = {
    "number": numero_limpo,
    "text": resposta_do_gemini
}

# Envio da requisição HTTP
response = requests.post(url_zapi, json=payload, headers=headers)

if response.status_code == 200 or response.status_code == 201:
    print("Mensagem enviada com sucesso pela Evolution API!")
else:
    print(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")
            
