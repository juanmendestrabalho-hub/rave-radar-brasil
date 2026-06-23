import json
import requests

def get_events():
    url = "https://www.sympla.com.br/eventos/sao-paulo-sp/musica-eletronica"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        # Salva o texto bruto para sabermos se o site está bloqueando
        with open('data/eventos.json', 'w', encoding='utf-8') as f:
            json.dump({"status": "teste", "tamanho_conteudo": len(response.text)}, f)
    except Exception as e:
        with open('data/eventos.json', 'w', encoding='utf-8') as f:
            json.dump({"status": "erro", "erro": str(e)}, f)

if __name__ == "__main__":
    get_events()
