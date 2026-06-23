import json
from playwright.sync_api import sync_playwright

def get_events():
    # Iniciando o navegador invisível
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Vamos usar um site de busca de eventos como alvo inicial 
        # (Substitua esta URL pela página de eventos que você deseja monitorar)
        url = "https://www.sympla.com.br/eventos/sao-paulo-sp/musica-eletronica"
        print(f"Conectando em: {url}")
        
        try:
            page.goto(url, wait_until="networkidle")
            
            # Aqui simulamos a extração de dados
            # NOTA: Você precisará identificar as classes CSS reais no seu navegador
            # Exemplo genérico:
            eventos = page.eval_on_selector_all(".sympla-card", """
                elements => elements.map(e => ({
                    title: e.querySelector('.title') ? e.querySelector('.title').innerText : 'Sem título',
                    start: '2026-07-30', 
                    url: e.querySelector('a') ? e.querySelector('a').href : '#'
                }))
            """)
            
            # Salvando os dados no arquivo JSON
            with open('data/eventos.json', 'w', encoding='utf-8') as f:
                json.dump(eventos, f, indent=4, ensure_ascii=False)
            
            print(f"Sucesso! {len(eventos)} eventos encontrados.")
            
        except Exception as e:
            print(f"Erro ao buscar eventos: {e}")
            
        browser.close()

if __name__ == "__main__":
    get_events()
    
