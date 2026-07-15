# Hiperautomatizador para Pesquisas

Automação desenvolvida em Python utilizando Playwright para realizar consultas no Portal da Transparência, capturar informações do usuário e gerar um arquivo JSON contendo os dados obtidos e uma captura da tela em Base64.

## Tecnologias

- Python 3.13+
- Playwright
- Playwright Stealth

## Funcionalidades

- Pesquisa por Nome, CPF ou NIS
- Captura automática das informações
- Screenshot da página
- Conversão da imagem para Base64
- Geração de arquivo JSON

## Como executar

pip install -r requirements.txt

playwright install

python reboot_test.py

## exemplo de JSON


{
  "nome": "João da Silva",
  "cpf": "***.***.***-**",
  "nis": "123456789",
  "screenshot": "<base64>"
}