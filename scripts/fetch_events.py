import json
from playwright.sync_api import sync_playwright

def get_events():
    eventos = []
    
    with sync_playwright() as p:
        # Iniciando o navegador
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Simulando um navegador real
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        url = "https://www.sympla.com.br/eventos/sao-paulo-sp/musica-eletronica"
        print(f"Acessando: {url}")
        
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Buscando todos os cards de eventos
            # Selecionamos os elementos 'a' que contêm '/evento/' no link
            cards = page.query_selector_all("a[href*='/evento/']")
            print(f"Total de elementos encontrados: {len(cards)}")
            
            for card in cards:
                # 1. Título
                titulo_el = card.query_selector("h3") or card.query_selector("h2")
                titulo = titulo_el.inner_text().strip() if titulo_el else None
                
                # 2. Data (tenta encontrar em elementos que contenham 'date' ou 'data' na classe)
                data_el = card.query_selector("[class*='date']") or card.query_selector("[class*='data']")
                data = data_el.inner_text().strip() if data_el else "Data a confirmar"
                
                # 3. Link
                link = card.get_attribute("href")
                if link and not link.startswith("http"):
                    link = "https://www.sympla.com.br" + link
                
                # Adiciona na lista apenas se tiver um título válido
                if titulo:
                    eventos.append({
                        "title": titulo,
                        "start": data,  # FullCalendar aceita formatos de texto como "25 de Junho" ou "2026-06-25"
                        "url": link
                    })
            
            # Salvando o resultado
            with open('data/eventos.json', 'w', encoding='utf-8') as f:
                json.dump(eventos, f, indent=4, ensure_ascii=False)
                
            print(f"Sucesso! {len(eventos)} eventos salvos em data/eventos.json")
            
        except Exception as e:
            print(f"Erro na execução: {e}")
        
        browser.close()

if __name__ == "__main__":
    get_events()
        
