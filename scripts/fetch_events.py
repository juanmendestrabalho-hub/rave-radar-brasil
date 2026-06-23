import json
import requests

def get_events():
    # URL de busca do Sympla (versão mobile/API que é mais aberta)
    url = "https://www.sympla.com.br/api/v4/events?city=Sao%20Paulo&categories=musica-eletronica"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # O Sympla retorna uma lista em 'data'
        eventos = []
        for e in data.get('data', []):
            eventos.append({
                "title": e.get('name'),
                "start": e.get('start_date'),
                "url": e.get('url')
            })
            
        with open('data/eventos.json', 'w', encoding='utf-8') as f:
            json.dump(eventos, f, indent=4, ensure_ascii=False)
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    get_events()
