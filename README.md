# Automação de importação de XML de NF-e de E-commerces x Bling

## 🛠️ Instalação de ferramentas

- Python: <https://www.python.org/downloads/>

## ⚙ Instalação de dependências

- Selenium: ```pip install selenium```
- Python DotEnv: ```pip install python-dotenv```
- Pyautogui: ```pip install pyautogui```
- Pyinstaller: ```pip install pyinstaller```

## 🚀 Geração do executável

Certifique-se de que esteja baixada a dependência do pyinstaller.

Execute o comando abaixo:

```bash
    pyinstaller ./src/index.py --onefile --noconsole
```

Descrição dos parâmetros:

- ./src/index.py: Caminho do arquivo no qual será gerado o executável.
- onefile: Gera apenas um arquivo para a aplicação.
- noconsole: Não abre o console (CMD) ao abrir o executável.
