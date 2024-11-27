import streamlit as st
import requests
from bs4 import BeautifulSoup
import locale
import pandas as pd
from modelos import *
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
def obter_dados_fiis():
    headers = {"User-Agent": "Mozilla/5.0"}
    resposta = requests.get('https://fundamentus.com.br/fii_resultado.php', headers=headers)
    soup = BeautifulSoup(resposta.text, 'html.parser')
    
    dados = []
    try:
        tabela = soup.find(id='tabelaResultado')
        if tabela and tabela.find('tbody'):
            linhas = tabela.find('tbody').find_all('tr')
            for linha in linhas:
                dados_fundo = linha.find_all('td')
                cotacao = locale.atof(dados_fundo[2].text.split()[0])
                dy = locale.atof(dados_fundo[4].text.split('%')[0])
                
                # Filtro de outliers
                if cotacao <= 3000 and dy <= 300:
                    dados.append({
                        'código': dados_fundo[0].text,
                        'segmento': dados_fundo[1].text,
                        'cotação': cotacao,
                        'dividend_yield': dy,
                        'p_vp': locale.atof(dados_fundo[5].text.split()[0]),
                        'valor_mercado': locale.atof(dados_fundo[6].text.split()[0]),
                        'liquidez': locale.atof(dados_fundo[7].text.split()[0]),
                        'qt_imoveis': int(dados_fundo[8].text),
                        'vacancia': locale.atof(dados_fundo[12].text.split('%')[0])
                    })
    except Exception as e:
        st.error(f"Erro ao obter dados: {str(e)}")
    
    return pd.DataFrame(dados)
def main():
    st.set_page_config(page_title="Dashboard FIIs", layout="wide")
    
    st.title("Dashboard de Fundos Imobiliários")
    
    # Sidebar com filtros
    st.sidebar.header("Filtros")
    
    df = obter_dados_fiis()
    
    # Filtros com number_input
    col_filtros1, col_filtros2 = st.sidebar.columns(2)
    
    with col_filtros1:
        min_cotacao = st.number_input(
            "Cotação Mínima (R$)", 
            value=30.0,
            min_value=float(df['cotação'].min()),
            max_value=float(df['cotação'].max()),
            step=1.0
        )
    
    with col_filtros2:
        min_dy = st.number_input(
            "Dividend Yield Mínimo (%)", 
            value=9.0,
            min_value=float(df['dividend_yield'].min()),
            max_value=float(df['dividend_yield'].max()),
            step=0.1
        )
    
    # Aplicando filtros
    df_filtrado = df[
        (df['cotação'] >= min_cotacao) &
        (df['dividend_yield'] >= min_dy)
    ]
    
    # Layout principal
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribuição por Segmento")
        fig_segmentos = df_filtrado['segmento'].value_counts()
        st.bar_chart(fig_segmentos)
    
    with col2:
        st.subheader("Relação Dividend Yield x P/VP")
        st.scatter_chart(data=df_filtrado, x='dividend_yield', y='p_vp')
    
    # Tabela com resultados
    st.subheader("FIIs Filtrados")
    st.dataframe(
        df_filtrado.style.format({
            'cotação': 'R$ {:.2f}',
            'dividend_yield': '{:.2f}%',
            'p_vp': '{:.2f}',
            'valor_mercado': '{:.0f}',
            'liquidez': '{:.0f}',
            'vacancia': '{:.2f}%'
        })
    )
if __name__ == "__main__":
    main()