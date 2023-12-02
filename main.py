import requests
from bs4 import BeautifulSoup

#header necessário para que o servidor entenda que estamos buscando informações no servidor.
headers = {"User-Agent" : "Mozilla/5.0"} 
resposta = requests.get('https://fundamentus.com.br/fii_resultado.php', headers = headers)
soup = BeautifulSoup(resposta.text, 'html.parser')
linhas = soup.find(id='tabelaResultado').find('tbody').find_all('tr')

for linha in linhas:
    dados_fundo = linha.find_all('td')
    print(
        f"[{dados_fundo[0].text}]\n"
        f"\tCotação: {dados_fundo[2].text}\n"
        f"\t\Setores: {dados_fundo[1].text}\n"
        f"\tDY %: {dados_fundo[4].text}\n"
        f"\tP/VP: {dados_fundo[5].text}\n"
    )

