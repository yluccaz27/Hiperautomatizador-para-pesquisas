import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def cookie(page):
    try:
            await page.click("#accept-all-btn", timeout=3000)
            print("Cookies aceitos")
    except:
            print("Banner de cookies não apareceu, seguindo...")


async def run():
    #iniciando o Playwright
    async with async_playwright() as p:

        #Abrindo o navegador
        browser = await p.firefox.launch(headless=False)

        #Abre uma nova pagina sem cache
        context = await browser.new_context(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
        page = await context.new_page()
        await Stealth().apply_stealth_async(page) #Mascara o script pra não cair em captcha
        
        #vai até a pagina
        await page.goto("https://portaldatransparencia.gov.br/pessoa/visao-geral")
        await page.wait_for_timeout(3000)
        await page.wait_for_load_state("networkidle")
        

        #clica para consultar Pessoa Fisica
        await page.wait_for_timeout(3000)
        await cookie(page)
        await page.wait_for_timeout(3000)
        await page.click("#button-consulta-pessoa-fisica")
        await page.wait_for_timeout(3000)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)



        #preenche o campo corretamento:
        await cookie(page)
        await page.wait_for_timeout(3000)
        
        #pesquisa:
        pesquisa = "Maria da Silva"
        await page.get_by_placeholder("Busque por Nome, Nis ou CPF (123456789-00)").fill(pesquisa)
        await page.wait_for_timeout(3000)
        await page.click("button[aria-label='Enviar dados do formulário de busca']")
        await page.wait_for_selector("#countResultados")
        await page.wait_for_timeout(3000)
        resultado = await page.locator("p:has(#countResultados)").inner_text()
        print(resultado)

        #clicar no primeiro:

        primeiro = page.locator("#resultados a.link-busca-nome").first
        await primeiro.click()
        await page.wait_for_timeout(3000)

        await cookie(page)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)

        #Abre a tabela:
        tabela = page.locator("button[aria-controls='accordion-recebimentos-recursos']")
        await tabela.click()
        await page.wait_for_timeout(3000)
        detalhe = page.locator("a:has-text('Detalhar')")
        await detalhe.click()
        await page.wait_for_timeout(3000)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)
        await page.screenshot(path="aaaaaa.png", full_page=True)
        #fecha o navegador
        await browser.close()

    
asyncio.run(run())
