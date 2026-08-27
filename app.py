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
    """Processa texto e/ou imagens com o Gemini 1.5 Flash."""
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
    2
