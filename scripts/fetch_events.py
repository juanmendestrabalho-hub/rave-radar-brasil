import json
import time
from playwright.sync_api import sync_playwright

def get_events():
    eventos = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"})
        
        try:
            url = "https://www.sympla.com.br/eventos/sao-paulo-sp/musica-eletronica"
            page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Aumentamos o tempo de espera para garantir o carregamento
            time.sleep(5) 
            
            # Tentando um seletor mais genérico que engloba os cards no Sympla
            # Procuramos por elementos que contêm 'event-card' na estrutura
            cards = page.query_selector_all("div[data-testid='event-card'], a[data-testid='event-card']")
            
            print(f"Cards encontrados: {len(cards)}")
            
            for card in cards:
                titulo = card.inner_text().split('\n')[0] # Pega a primeira linha do card
                link = card.get_attribute("href")
                if link and not link.startswith("http"):
                    link = "https://www.sympla.com.br" + link
                
                eventos.append({"title": titulo, "start": "Data a confirmar", "url": link})
            
            with open('data/eventos.json', 'w', encoding='utf-8') as f:
                json.dump(eventos, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"Erro detalhado: {e}")
        finally:
            browser.close() # Isso garante que o navegador feche sem dar erro de "Event loop"

if __name__ == "__main__":
    get_events()
