import asyncio
from playwright.async_api import async_playwright

async def run():
    #isso inicia o Playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        
        #Abre uma nova pagina
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://youtube.com")

        #pesquisa   
        item = "Geekoolize"
        p1 = await page.get_by_placeholder("Pesquisar").fill(item)
        print(f"Pesquisou: {p1}")
        await page.wait_for_load_state("networkidle")
        await page.click("button[aria-label='Search']")
        print("Clicou!")
        await page.wait_for_load_state("networkidle")
        await page.locator(f'a:has-text("{item}")').click()
        print("Clicou no canal")
        await page.wait_for_timeout(1500)
        await page.screenshot(path="Youtube_teste.png")
        print("Screenshot feita!")

        await browser.close()

    
asyncio.run(run())