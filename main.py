import requests
from bs4 import BeautifulSoup
import locale
from modelos import FundoImobiliario,Estrategia

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 
def trata_porcentagem(porcentagem):
    """
    Função para tratar o caracter de porcentagem.
    """
    return locale.atof(porcentagem.split('%')[0])

def trata_decimal(decimal):
    """
    Função para tirar o R$ e o decimal.
    """
    return locale.atof(decimal.split)
#header necessário para que o servidor entenda que estamos buscando informações no servidor.
headers = {"User-Agent" : "Mozilla/5.0"} 
resposta = requests.get('https://fundamentus.com.br/fii_resultado.php', headers = headers)
soup = BeautifulSoup(resposta.text, 'html.parser')
linhas = soup.find(id='tabelaResultado').find('tbody').find_all('tr')

resultado = []
estrategia = Estrategia(
    cotacao_atual_minima=50.0,
    dividend_yield_minimo=10,
    p_vp_minimo=0.70,
    valor_mercado_minimo=20000000,
    qt_minima_imoveis=5,
    maxima_vacancia_media=10
)

for linha in linhas:
    dados_fundo = linha.find_all('td')
    
    codigo = dados_fundo[0].text
    segmento = dados_fundo[1].text
    cotacao_atual = trata_decimal(dados_fundo[2].text)
    ffo_yield = trata_porcentagem(dados_fundo[3].text)
    dividend_yield = trata_porcentagem(dados_fundo[4].text)
    p_vp = trata_decimal(dados_fundo[5].text)
    valor_mercado = trata_decimal(dados_fundo[6].text)
    liquidez = trata_decimal(dados_fundo[7].text)
    qt_imoveis = int(dados_fundo[8].text)
    preco_m2 = trata_decimal(dados_fundo[9].text)
    aluguel_m2 = trata_decimal(dados_fundo[10].text)
    cap_rate = trata_porcentagem(dados_fundo[11].text)
    vacancia_media = trata_porcentagem(dados_fundo[12].text)

    fundo_imobiliario = FundoImobiliario(codigo, segmento, cotacao_atual,dividend_yield, ffo_yield, p_vp,   
                        valor_mercado,liquidez, qt_imoveis, preco_m2, aluguel_m2, cap_rate, vacancia_media
                        )
     
    if estrategia.aplica_estrategia(fundo_imobiliario):
        resultado.append(fundo_imobiliario)
print(resultado)