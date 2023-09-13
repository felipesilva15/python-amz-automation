from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from dotenv import load_dotenv

#########
# Setup #
#########

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as variáveis de ambiente
amazon_username = os.getenv("AMAZON_USERNAME")
amazon_password = os.getenv("AMAZON_PASSWORD")
amazon_baseurl = os.getenv("AMAZON_BASEURL")
bling_username = os.getenv("BLING_USERNAME")
bling_password = os.getenv("BLING_PASSWORD")
bling_baseurl = os.getenv("BLING_BASEURL")
xml_download_folder = os.getenv("XML_DOWNLOAD_FOLDER")
driver_path = os.getenv("WEBDRIVER_PATH")

# Cria a pasta de download se ela não existir
if not os.path.exists(xml_download_folder):
    os.makedirs(xml_download_folder)

# Configura as opções do Chrome para definir a pasta de download
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': xml_download_folder}
chrome_options.add_experimental_option('prefs', prefs)

# Iniciar o navegador com as opções configuradas
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)

#################################
# Download de XML do e-commerce #
#################################

# Abre o site de login
driver.get(amazon_baseurl + '/login')
time.sleep(2)  # Esperar um pouco para o carregamento da página

# Busca e preenche os campos de login
username_field = driver.find_element_by_id('username')
password_field = driver.find_element_by_id('password')

username_field.send_keys(amazon_username)
password_field.send_keys(amazon_password)
password_field.send_keys(Keys.RETURN)
time.sleep(10)

# Navega para a página de download de XMLs
driver.get(amazon_baseurl + '/download-xmls')
time.sleep(3)

# Verificar se todos os XMLs foram baixados
while True:
    # Lista os arquivos da pasta de download
    xml_downloaded_files = os.listdir(xml_download_folder)
    
    # Verificar se todos os XMLs esperados estão na pasta de download
    if all(xml_file_name in xml_downloaded_files for xml_file_name in expected_xml_files):
        break
    
    # Aguarda alguns segundos e verifica novamente
    time.sleep(3)

##########################
# Upload de XML no Bling #
##########################

# Abre o site de login
driver.get(bling_baseurl + '/login')
time.sleep(2)  # Esperar um pouco para o carregamento da página

# Busca e preenche os campos de login
username_field = driver.find_element_by_id('username')
password_field = driver.find_element_by_id('senha')

username_field.send_keys(bling_username)
password_field.send_keys(bling_password)
password_field.send_keys(Keys.RETURN)
time.sleep(10)

# Navega para a página de upload de XMLs
driver.get(bling_baseurl + '/notas.fiscais.php#list')
time.sleep(5)

# Seleciona a opção de importação de NF-e via XML
upload_option = driver.find_element_by_classname('nfe-list-options')
upload_option.send_keys(Keys.RETURN)
time.sleep(1)

# Lista os arquivos da pasta de download
xml_downloaded_files = os.listdir(xml_download_folder)

# Importa os XMLs das notas para o Bling
for xml_file_name in xml_downloaded_files:
    # Verifica se o arquivo possui a extensão de xml
    if not xml_file_name.endswith('.xml'):
        continue

    # Encontrar o botão ou elemento para fazer o upload do arquivo
    upload_button = driver.find_element_by_classname('qq-uploader') 

    # Enviar o caminho completo do arquivo para o campo de upload
    file_path = os.path.join(xml_download_folder, xml_file_name)
    upload_button.send_keys(file_path)

    # Aguardar um momento para o processo de importação
    time.sleep(5)  # Ajuste conforme necessário

#############################################
# Finalização do processo excluindo os XMLs #
#############################################

# Apaga os XMLs da pasta de download após o processo ser finalizado
for xml_file_name in xml_downloaded_files:
    xml_file_path = os.path.join(xml_download_folder, xml_file_name)
    os.remove(xml_file_path)

# Fecha o navegador
driver.quit()