from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import time
import os
import pyautogui
import logging
import sys

#########
# Setup #
#########

# Configura o arquivo de log
logging.basicConfig(filename='log.txt', level=logging.INFO, encoding='utf-8', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Definir um manipulador para registrar exceções em um arquivo de log
def exception_handler(type, value, traceback):
    logging.critical("Exceção não tratada:", exc_info=(type, value, traceback))

sys.excepthook = exception_handler

try:
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv('./envs/.env')

    amazon_username = os.getenv("AMAZON_USERNAME")
    amazon_password = os.getenv("AMAZON_PASSWORD")
    amazon_baseurl = os.getenv("AMAZON_BASEURL")
    bling_username = os.getenv("BLING_USERNAME")
    bling_password = os.getenv("BLING_PASSWORD")
    bling_baseurl = os.getenv("BLING_BASEURL")
    xml_download_folder = os.getenv("XML_DOWNLOAD_FOLDER")

    # Cria a pasta de download se ela não existir
    if not os.path.exists(xml_download_folder):
        os.makedirs(xml_download_folder)

    # Configura as opções do Chrome para definir a pasta de download
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': xml_download_folder}
    chrome_options.add_experimental_option('prefs', prefs)

    # Iniciar o navegador com as opções configuradas e maximiza a janela
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    # Instancia o mouse
    mouse = ActionChains(driver)

    #################################
    # Download de XML do e-commerce #
    #################################

    # # Abre a página de login
    # driver.get(amazon_baseurl + '/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fsellercentral.amazon.com%2Fhome&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=sc_na_amazon_v2&openid.mode=checkid_setup&language=pt_BR&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=sc_na_amazon_v2&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&ssoResponse=eyJ6aXAiOiJERUYiLCJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiQTI1NktXIn0.86NwBB-6i8PvO3Ggeo0nrekONfZGINNTDSnvQUfaBiFuM3dcyyVT4w.vC-3yeqa6w0pqsaf.PWmSiYIlMF-Qw6yfl7CqPBl2sVovv4u8zGIVKWYTESRfTE5GUxsD0kunwA8PcjuoqHqh0UkDYY3uu1kS4cdPWw8nS51KEpD8CEZxWvA70rPo3NDSI_wGvkLu1R7Y-sq_dYYvRN4Fe95Q9b84cgutJLHSPXWTXSdIHWYKK6UaQFmnobXco4bVYJMwvARWjOMWvGhbGrFYVYA.RwyU8bqJaQdow3N0OJ-Cqw')

    # # Busca e preenche os campos de login
    # username_field = driver.find_element(By.ID, 'ap_email')
    # password_field = driver.find_element(By.ID, 'ap_password')

    # username_field.send_keys(amazon_username)
    # password_field.send_keys(amazon_password)
    # password_field.send_keys(Keys.RETURN)

    # # aguarda o carregamento do login
    # time.sleep(8)

    # # Navega para a página de download de XMLs
    # driver.get(amazon_baseurl + '/download-xmls')
    # time.sleep(3)

    # # Verificar se todos os XMLs foram baixados
    # while True:
    #     # Lista os arquivos da pasta de download
    #     xml_downloaded_files = os.listdir(xml_download_folder)
        
    #     # Verificar se todos os XMLs esperados estão na pasta de download
    #     if all(xml_file_name in xml_downloaded_files for xml_file_name in expected_xml_files):
    #         break
        
    #     # Aguarda alguns segundos e verifica novamente
    #     time.sleep(3)

    ##########################
    # Upload de XML no Bling #
    ##########################

    print('Realizando o upload de XML no Bling...')

    # Abre a página de login
    driver.get(bling_baseurl)

    # Passa o mouse até o botão de login para exibir o formulário
    login_button = driver.find_element(By.ID, 'dropdown')
    mouse.move_to_element(login_button).perform()

    # Busca e preenche os campos de login
    username_field = driver.find_element(By.ID, 'username')
    password_field = driver.find_element(By.ID, 'senha')

    username_field.send_keys(bling_username)
    password_field.send_keys(bling_password)
    password_field.send_keys(Keys.RETURN)

    # aguarda o carregamento do login
    time.sleep(8)

    # Navega para a página de upload de XMLs
    driver.get(bling_baseurl + '/notas.fiscais.php#list')
    time.sleep(3)

    # Acessa o modal de importação notas por XML
    more_options_button = driver.find_element(By.CSS_SELECTOR, 'span.open-more-actions')
    mouse.move_to_element(more_options_button).click().perform()
    time.sleep(1)

    import_nfe_button = driver.find_element(By.CSS_SELECTOR, 'li.action-item[data-function="buscarXMLNFe"]')
    mouse.move_to_element(import_nfe_button).click().perform()
    time.sleep(1)

    # Lista os arquivos da pasta de download
    xml_downloaded_files = os.listdir(xml_download_folder)

    if len(xml_downloaded_files) == 0:
        logging.info('Nenhum arquivo para importar!')
    
    # Realizao upload de cada XML
    for xml_file_name in xml_downloaded_files:
        # Verifica se o arquivo possui a extensão de xml
        if not xml_file_name.endswith('.xml'):
            continue
        
        # Clica no container de upload de XML
        upload_container = driver.find_element(By.CSS_SELECTOR, 'div.qq-uploader')
        mouse.move_to_element(upload_container).click().perform()
        time.sleep(1)

        # Preenche o caminho completo de onde está o arquivo e o seleciona
        full_path = os.path.join(xml_download_folder, xml_file_name)
        pyautogui.write(full_path)
        #pyautogui.press('enter')
        
        logging.warning('Não foi possível importar a NF-e no Bling')
        
        time.sleep(5)

    #############################################
    # Finalização do processo excluindo os XMLs #
    #############################################

    print('Excluindo arquivos XML...')

    # Lista os arquivos da pasta de download
    xml_downloaded_files = os.listdir(xml_download_folder)

    # Apaga os XMLs da pasta de download após o processo ser finalizado
    for xml_file_name in xml_downloaded_files:
        if not xml_file_name.endswith('.xml'):
            continue
        
        full_path = os.path.join(xml_download_folder, xml_file_name)
        os.remove(full_path)
        
    print('Finalizando o processo...')

    # Fecha o navegador
    driver.quit()
except Exception as e:
    logging.critical(f"Ocorreu uma exceção: {e}")