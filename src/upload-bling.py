from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import time
import os
import pyautogui

#########
# Setup #
#########

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv('./envs/.env')

amazon_username = os.getenv("AMAZON_USERNAME")
amazon_password = os.getenv("AMAZON_PASSWORD")
amazon_baseurl = os.getenv("AMAZON_BASEURL")
bling_username = os.getenv("BLING_USERNAME")
bling_password = os.getenv("BLING_PASSWORD")
bling_baseurl = os.getenv("BLING_BASEURL")
xml_download_folder = os.getenv("XML_DOWNLOAD_FOLDER")
#driver_path = os.getenv("WEBDRIVER_PATH")

# Cria a pasta de download se ela não existir
if not os.path.exists(xml_download_folder):
    os.makedirs(xml_download_folder)

# Configura as opções do Chrome para definir a pasta de download
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': xml_download_folder}
chrome_options.add_experimental_option('prefs', prefs)

# Iniciar o navegador com as opções configuradas
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

# Instância o mouse
mouse = ActionChains(driver)

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
    print(full_path)
    #pyautogui.press('enter')
    
    time.sleep(5)

print('Finalizando o processo...')

# Fecha o navegador
driver.quit()