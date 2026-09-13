# Lista de Produtos Campeões com Links Diretos (Página do Anúncio)
PRODUTOS_DIRETOS = {
    "protetor solar": {
        "nome": "Protetor Solar Facial L'Oréal Paris FPS 60",
        "amz": f"https://www.amazon.com.br/dp/B077YW3N8Z?tag={AMAZON_TAG}",
        "ml": f"https://www.mercadolivre.com.br/p/MLB19876543?matt={ML_TAG}",
        "nota": "4.8/5.0 ⭐ (Mais de 3.000 avaliações)"
    },
    "air fryer": {
        "nome": "Fritadeira Sem Óleo Mondial Family 4 Litros",
        "amz": f"https://www.amazon.com.br/dp/B08DFG1234?tag={AMAZON_TAG}",
        "ml": f"https://www.mercadolivre.com.br/p/MLB23456789?matt={ML_TAG}",
        "nota": "4.9/5.0 ⭐ (Líder de vendas)"
    }
}

def gerar_links_busca(produto_nome):
    termo = produto_nome.strip().lower()
    
    # 1. Checa se o usuário pediu um produto do nosso Banco de Curadoria Direta
    for chave, dados in PRODUTOS_DIRETOS.items():
        if chave in termo:
            return dados["amz"], dados["ml"], dados["nome"], dados["nota"]
            
    # 2. Se não estiver no banco, gera a busca filtrada de segurança
    termo_encoded = urllib.parse.quote(produto_nome.strip())
    link_amz = f"https://www.amazon.com.br/s?k={termo_encoded}&s=review-rank&tag={AMAZON_TAG}"
    link_ml = f"https://lista.mercadolivre.com.br/{termo_encoded}_NoIndex_True#matt={ML_TAG}"
    return link_amz, link_ml, None, None

