from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.nfse.gov.br/EmissorNacional/Login")
    page.get_by_placeholder("CPF/CNPJ").click()
    page.get_by_placeholder("CPF/CNPJ").fill("35.686.321/0001-76")
    page.get_by_placeholder("Senha").click()
    page.get_by_placeholder("Senha").fill("Nhn.sk89")
    page.get_by_role("button", name="Entrar").click()
    page.locator("#wgtAcessoRapido").get_by_role("link").first.click()
    page.locator("#btn_DataCompetencia").click()
    page.get_by_role("cell", name="1", exact=True).first.click()
    page.locator("#pnlTomador label").filter(has_text="Brasil").locator("i").click()
    page.locator("#Tomador_Inscricao").click()

    #empresa prestadora de serviço
    cnpj_contratante = '39582073837'
    estado = 'São Paulo'
    estado1 = 'São Paulo/SP'
    servico = "01.01.01 - Análise e"
    descricao_servico = "Serviço de Desenvolvimento de Aplicativo para controle de áudio."
    valor_servico = "10000" # 100,00 reais, nesse caso
    
    page.locator("#Tomador_Inscricao").fill(cnpj_contratante)
    page.locator("#Tomador_Inscricao").press("Tab")
    page.get_by_role("button", name="Avançar").click()
    page.locator("#pnlLocalPrestacao").get_by_label("").click()
    page.get_by_label("Search").fill(estado)
    page.get_by_role("option", name=estado1).click()
    page.get_by_label("", exact=True).click()
    page.get_by_label("Search").fill(servico)
    page.get_by_role("option", name=servico).click()
    page.locator("#pnlServicoPrestado label").filter(has_text=re.compile(r"^Não$")).locator("i").click()
    page.locator("#ServicoPrestado_Descricao").click()
    page.locator("#ServicoPrestado_Descricao").fill(descricao_servico)
    page.locator("#ServicoPrestado_CodigoNBS_chosen a").click()
    page.locator("#ServicoPrestado_CodigoNBS_chosen").get_by_role("textbox").fill("desen")
    page.locator("#ServicoPrestado_CodigoNBS_chosen").get_by_text("112012200 - Serviços de").click()
    page.get_by_role("button", name="Avançar").click()
    page.locator("#Valores_ValorServico").click()
    page.locator("#Valores_ValorServico").fill(valor_servico)
    page.locator("a").filter(has_text="Nenhum").click()
    page.get_by_role("button", name="Avançar").click()
    page.locator("#btnProsseguir").click()
    with page.expect_download() as download_info:
        page.get_by_role("link", name="Baixar XML").click()
    download = download_info.value
    with page.expect_download() as download1_info:
        page.get_by_role("link", name="Baixar DANFSe").click()
    download1 = download1_info.value
    page.get_by_role("link", name=" Visualizar NFS-e").click()
    page.goto("https://www.nfse.gov.br/EmissorNacional/DPS/NFSe?idr=Q3d5RkUrcG5veXRoV0NkOTVLYTQrUT090")
    page.get_by_role("link", name=" Nova NFS-e").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
