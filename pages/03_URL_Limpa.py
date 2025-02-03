import re

def extrair_ids(url):
    """
    Extrai o page_id e o post_id de uma URL do Facebook que esteja no formato:
    https://www.facebook.com/<page_id>/posts/<post_id>/...
    
    Retorna:
        tuple: (page_id, post_id)
    
    Lança ValueError se a URL não estiver no formato esperado.
    """
    # Expressão regular para capturar os IDs
    padrao = r"facebook\.com/(\d+)/posts/(\d+)"
    correspondencia = re.search(padrao, url)
    
    if correspondencia:
        page_id, post_id = correspondencia.groups()
        return page_id, post_id
    else:
        raise ValueError("A URL não está no formato esperado.")

# Exemplo de uso:
url_teste = ("https://www.facebook.com/61551247163885/posts/122192071058041572/"
             "?dco_ad_token=AapXK1yO1ATaWbfEB_jb_MOONPXE5BzrXjhlqK1f2CAFngcqD8NImR50bQ-DFZlaOFW098XzRK7TgK5s"
             "&dco_ad_id=120216377092080700")

try:
    page_id, post_id = extrair_ids(url_teste)
    print("page_id:", page_id)
    print("post_id:", post_id)
except ValueError as e:
    print("Erro:", e)
