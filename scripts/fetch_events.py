import json
from playwright.sync_api import sync_playwright

def get_events():
    eventos = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
        
        url = "https://www.sympla.com.br/eventos/sao-paulo-sp/musica-eletronica"
        page.goto(url, wait_until="networkidle")
        
        # Tentativa: buscar pelo container de eventos (geralmente uma lista ou grid)
        # Vamos buscar qualquer elemento que pareça um card de evento
        cards = page.query_selector_all("div[class*='EventCard']")
        
        print(f"Cards encontrados: {len(cards)}")
        
        for card in cards:
            # Tenta pegar o título dentro do card
            titulo_el = card.query_selector("h3") or card.query_selector("h2")
            titulo = titulo_el.inner_text().strip() if titulo_el else "Evento sem título"
            
            # Tenta pegar o link
            link_el = card.query_selector("a")
            link = link_el.get_attribute("href") if link_el else "#"
            if link and not link.startswith("http"):
                link = "https://www.sympla.com.br" + link
                
            eventos.append({"title": titulo, "start": "2026-06-30", "url": link})
            
        with open('data/eventos.json', 'w', encoding='utf-8') as f:
            json.dump(eventos, f, indent=4, ensure_ascii=False)
            
    browser.close()

if __name__ == "__main__":
    get_events()
