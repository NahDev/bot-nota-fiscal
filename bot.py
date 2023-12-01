import csv
from playwright.sync_api import Playwright, sync_playwright

def run(playwright: Playwright, cnpj_emissor, senha_emissor, data_emissao, cnpj_cliente, telefone_cliente, email_cliente, valor, servico_search, cnae_servico, descrica_servico) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.nfse.gov.br/EmissorNacional/Login")
    page.get_by_placeholder("CPF/CNPJ").click()
    page.get_by_placeholder("CPF/CNPJ").fill(cnpj_emissor)
    page.get_by_placeholder("Senha").click()
    page.get_by_placeholder("Senha").fill(senha_emissor)
    page.get_by_role("button", name="Entrar").click()
    page.locator("#wgtAcessoRapido").get_by_role("link").first.click()

    # Incio do loop
    for row in zip(cnpj_cliente, telefone_cliente, email_cliente, valor, servico_search, cnae_servico, descrica_servico):
        cnpj_cliente, telefone_cliente, email_cliente, valor, servico_search, cnae_servico, descrica_servico = row

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

    context.close()
    browser.close()


# Lê as informações do arquivo CSV
with open('seuarquivo.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)

with sync_playwright() as playwright:
    for row in data:
        # Convertendo a coluna 'valor' para um número
        row['valor'] = float(row['valor'].replace(',', '.'))

        run(playwright, **row)