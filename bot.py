from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    cnpj_emissor = "35.686.321/0001-76"
    senha_emissor = ''
    data_emissao = '28/11/2023'

    cnpj_cliente= '395.820.738/37'
    telefone_cliente = "(11)9874-56334"
    email_cliente ="nahuan89@gmail.com"
    valor = "100"
    servico_search = '01.'
    cnae_servico ="01.01.01 - Análise e"
    descrica_servico = "Serviço de Desenvolvimento de Aplicativo para controle de áudio."
    page.goto("https://www.nfse.gov.br/EmissorNacional/Login")
    page.get_by_placeholder("CPF/CNPJ").click()
    page.get_by_placeholder("CPF/CNPJ").fill(cnpj_emissor)
    page.get_by_placeholder("Senha").click()
    page.get_by_placeholder("Senha").fill(senha_emissor)
    page.get_by_role("button", name="Entrar").click()
    page.locator("#wgtAcessoRapido").get_by_role("link").first.click()
    page.locator("#DataCompetencia").click()
    page.locator("#DataCompetencia").fill(data_emissao)
    page.locator("#pnlTomador label").filter(has_text="Brasil").locator("i").click()
    page.locator("#Tomador_Inscricao").click()
    page.locator("#Tomador_Inscricao").fill(cnpj_cliente)
    page.get_by_role("button", name="").click()
    page.locator("#Tomador_Telefone").click()
    page.locator("#Tomador_Telefone").fill(telefone_cliente)
    page.locator("#Tomador_Telefone").press("Tab")
    page.locator("#Tomador_Email").fill(email_cliente)
    page.get_by_role("button", name="Avançar").click()
    page.locator("#pnlLocalPrestacao").get_by_label("").click()
    page.get_by_label("Search").fill("São Pa")
    page.get_by_role("option", name="São Paulo/SP").click()
    page.get_by_label("", exact=True).click()
    page.get_by_label("Search").fill(servico_search)
    page.get_by_role("option", name=cnae_servico).click()
    page.locator("#pnlServicoPrestado").get_by_text("Não", exact=True).click()
    page.locator("#ServicoPrestado_Descricao").click()
    page.locator("#ServicoPrestado_Descricao").fill(descrica_servico)
    page.get_by_role("button", name="Avançar").click()
    page.locator("#Valores_ValorServico").click()
    page.locator("#Valores_ValorServico").fill(valor)
    page.get_by_role("button", name="Avançar").click()
    page.locator("#btnProsseguir").click()
    with page.expect_download() as download_info:
        page.get_by_role("link", name="Baixar XML").click()
    download = download_info.value
    with page.expect_download() as download1_info:
        page.get_by_role("link", name="Baixar DANFSe").click()
    download1 = download1_info.value
    page.get_by_role("link", name=" Nova NFS-e").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
