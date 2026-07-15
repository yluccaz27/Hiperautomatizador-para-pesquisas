import asyncio, os, base64, json
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def cookie(page):
    try:
            await page.click("#accept-all-btn", timeout=500)
            print("Cookies aceitos")
    except:
            pass


async def esperar_verificacao_humana(page):
    try:
        await page.wait_for_selector("text=Let's confirm you are human", timeout=15000)
        print("⚠️ Verificação detectada. Resolve no navegador...")
        
        await page.wait_for_function(
            "() => !window.location.href.includes('challenges.cloudflare.com')",
            timeout=180000
        )
        print("Seguindo...")
    except:
        pass

async def salva_base(dados_user):
     with open(f"arquivos/imagens/{dados_user}.png", "rb") as f:
          bytes_img = f.read()
          encoded = base64.b64encode(bytes_img)
          str_base = encoded.decode("utf-8")
          
          print(str_base[:100])
          return str_base, dados_user

async def salva_json(str_base, nome, cpf, nis):

    dados = {
          "nome" : nome,
          "cpf" : cpf,
          "nis" : nis,
          "screenshot" : str_base
            }
    json_string = json.dumps(dados, ensure_ascii= False, indent = 2)
    print(json_string)

    with open(f"arquivos/{nome}.json", "w", encoding="utf-8") as f:
         json.dump(dados, f, ensure_ascii = False, indent = 2)


async def captura_dados(page):
    try:
        nome = await page.locator("section.dados-tabelados div.col-xs-12.col-sm-4:has(strong:text('Nome')) span").inner_text(timeout=3000)
        nome = nome.strip()
    except:
        nome = None

    try:
        cpf = await page.locator("section.dados-tabelados div.col-xs-12.col-sm-3:has(strong:text('CPF')) span").inner_text(timeout=3000)
        cpf = cpf.strip()
    except:
        cpf = None

    try:
        nis = await page.locator("#tabela-visao-geral-sancoes tbody tr:first-child td:nth-child(2)").inner_text(timeout=3000)
        nis = nis.strip()
    except:
        nis = None

    return nome, cpf, nis


async def run():
    #iniciando o Playwright
    async with async_playwright() as p:

        #Abrindo o navegador
        browser = await p.chromium.launch(headless=False, channel="chrome")

        if os.path.exists("sessao.json"):
            print("Sessão encontrada, carregando...")
            context = await browser.new_context(
                viewport={"width": 1366, "height": 768},
                locale="pt-BR",
                timezone_id="America/Sao_Paulo",
                storage_state="sessao.json"
            )
        else:
            print("Sem sessão salva, abrindo do zero...")
            context = await browser.new_context(
                viewport={"width": 1366, "height": 768},
                locale="pt-BR",
                timezone_id="America/Sao_Paulo"
            )
        #Abre uma nova pagina sem cache
        page = await context.new_page()
        #Mascara o script pra não cair em captcha
        
        
        #vai até a pagina
        await page.goto("https://portaldatransparencia.gov.br/pessoa/visao-geral")
        await page.wait_for_timeout(500)
        await page.wait_for_load_state("networkidle")
        

        #clica para consultar Pessoa Fisica
        await page.wait_for_timeout(500)
        await cookie(page)
        await page.wait_for_timeout(500)
        await page.click("#button-consulta-pessoa-fisica")
        await page.wait_for_timeout(500)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(500)


        while True:
                pesquisa = input("Digite o termo a ser buscado: ")
                await page.get_by_placeholder("Busque por Nome, Nis ou CPF (123456789-00)").fill(pesquisa)
                await page.wait_for_timeout(500)
                await page.click("button[aria-label='Enviar dados do formulário de busca']")
                await page.wait_for_selector("#countResultados")
                await page.wait_for_timeout(500)
                resultado = await page.locator("p:has(#countResultados)").inner_text()
                print(resultado)
                await page.wait_for_load_state("networkidle")

                if "0 resultados" not in resultado.lower():
                        break  # achou — sai do loop

                print("Sem resultados, tente novamente.")


                    #clicar no primeiro:
        await page.wait_for_load_state("networkidle")
        primeiro = page.locator("#resultados a.link-busca-nome").first
        await primeiro.click()
        await page.wait_for_timeout(500)

        await cookie(page)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(500)

                #Abre a tabela:
        tabela = page.locator("button[aria-controls='accordion-recebimentos-recursos']")
        await tabela.click()
        await page.wait_for_timeout(500)
        nome, cpf, nis = await captura_dados(page)
        await page.screenshot(path=f"arquivos/imagens/{nome}.png", full_page=True)
        str_base, _ = await salva_base(nome)
        await salva_json(str_base, nome, cpf, nis)

        detalhe = page.locator("a:has-text('Detalhar')")
        await detalhe.click()
        await esperar_verificacao_humana(page)
        await page.wait_for_timeout(500)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(500)
        await page.screenshot(path=f"{nome}.png", full_page=True)
        await salva_base(nome)


                        
        await context.storage_state(path="sessao.json")
                #fecha o navegador
        await browser.close()



asyncio.run(run())
