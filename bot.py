import logging
from playwright.sync_api import Playwright, sync_playwright, expect
import csv

# Configurar o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Ler credenciais do arquivo credenciais.csv
    with open('credenciais.csv', newline='', encoding='utf-8') as credenciais_file:
        credenciais_reader = csv.DictReader(credenciais_file)
        credenciais = next(credenciais_reader)
        cnpj_emissor = credenciais['cnpj_emissor']
        senha_emissor = credenciais['senha_emissor']

    # Ler dados de emissão do arquivo emissao_input.csv
    with open('emissao_input.csv', newline='', encoding='utf-8') as emissao_input_file:
        emissao_input_reader = csv.DictReader(emissao_input_file)
        emissao_input = next(emissao_input_reader)
        data_emissao = emissao_input['data_emissao']
        cnpj_cliente = emissao_input['cnpj_cliente']
        telefone_cliente = emissao_input['telefone_cliente']
        email_cliente = emissao_input['email_cliente']
        valor = emissao_input['valor']
        servico_search = emissao_input['servico_search']
        cnae_servico = emissao_input['cnae_servico']
        descrica_servico = emissao_input['descrica_servico']

    try:
            
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
        logger.info("Processo concluído com sucesso.")
    except Exception as e:
        logger.error(f"Erro durante a execução: {str(e)}")

    finally:
        context.close()
        browser.close()

if __name__ == "__main__":
    logging.info("Iniciando o Robô para Emitir faturasFaturas.")
    
    with sync_playwright() as playwright:
        run(playwright)

