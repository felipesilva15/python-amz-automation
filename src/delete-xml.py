from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv('./envs/.env')
xml_download_folder = os.getenv("XML_DOWNLOAD_FOLDER")

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