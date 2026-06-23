import json
import requests
from bs4 import BeautifulSoup

def get_events():
    url = "https://www.sympla.com.br/eventos/sao-paulo-sp/musica-eletronica"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # O Sympla guarda os dados em uma tag script chamada __NEXT_DATA__
        script_tag = soup.find('script', id='__NEXT_DATA__')
        
        if script_tag:
            data = json.loads(script_tag.string)
            # Navegando na estrutura JSON que o site usa
            eventos_raw = data['props']['pageProps']['events']
            
            eventos = []
            for e in eventos_raw:
                eventos.append({
                    "title": e.get('name'),
                    "start": e.get('startDate'),
                    "url": f"https://www.sympla.com.br/evento/{e.get('id')}"
                })
            
            with open('data/eventos.json', 'w', encoding='utf-8') as f:
                json.dump(eventos, f, indent=4, ensure_ascii=False)
            print(f"Sucesso! {len(eventos)} eventos encontrados.")
        else:
            print("Não foi possível encontrar a tag de dados.")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    get_events()
