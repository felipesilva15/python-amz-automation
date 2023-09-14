import logging
import sys

# Configurar o arquivo de log e o nível de registro
logging.basicConfig(filename='log.txt', level=logging.INFO, encoding='utf-8', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Registrar mensagens no arquivo de log
logging.debug('Esta é uma mensagem de depuração')
logging.info('Esta é uma mensagem informativa')
logging.warning('Esta é uma mensagem de aviso')
logging.error('Esta é uma mensagem de erro')
logging.critical('Esta é uma mensagem crítica')
logging.info('Esta é uma mensagem informativa')
logging.info('Esta é uma mensagem informativa')

# Definir um manipulador para registrar exceções em um arquivo de log
def excecao_handler(type, value, traceback):
    logging.critical("Exceção não tratada:", exc_info=(type, value, traceback))

sys.excepthook = excecao_handler

# Seu código

try:
    # Seu código aqui
    resultado = 10 / 0  # Isso causará uma exceção
except Exception as e:
    # Você pode lidar com a exceção aqui se desejar
    logging.critical(f"Ocorreu uma exceção: {e}")
