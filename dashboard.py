import streamlit as st
import pandas as pd
from data import obter_dados_fiis

def main():
    st.set_page_config(page_title="Dashboard FIIs", layout="wide")
    
    st.title("Dashboard de Fundos Imobiliários")
    
    # Sidebar com filtros
    st.sidebar.header("Filtros")
    
    try:
        df = obter_dados_fiis()
    except Exception as e:
        st.error(str(e))
        return
    
    # Pesquisa por código
    pesquisa_codigo = st.sidebar.text_input("Pesquisar por Código (ex.: MXRF11)", "").upper()
    if pesquisa_codigo:
        df = df[df['código'].str.contains(pesquisa_codigo, case=True)]
        if df.empty:
            st.sidebar.warning("Nenhum FII encontrado com esse código.")

    # Filtros
    col_filtros1, col_filtros2 = st.sidebar.columns(2)
    
    with col_filtros1:
        min_cotacao = st.number_input("Cotação Mínima (R$)", value=30.0, min_value=float(df['cotação'].min()), max_value=float(df['cotação'].max()), step=1.0)
        min_dy = st.number_input("Dividend Yield Mínimo (%)", value=9.0, min_value=float(df['dividend_yield'].min()), max_value=float(df['dividend_yield'].max()), step=0.1)
        min_valor_mercado = st.number_input("Valor de Mercado Mínimo (R$)", value=100000000.0, min_value=float(df['valor_mercado'].min()), max_value=float(df['valor_mercado'].max()), step=1000000.0)

    with col_filtros2:
        min_liquidez = st.number_input("Liquidez Mínima (R$)", value=10000.0, min_value=float(df['liquidez'].min()), max_value=float(df['liquidez'].max()), step=1000.0)
        min_qt_imoveis = st.number_input("Quantidade Mínima de Imóveis", value=1, min_value=int(df['qt_imoveis'].min()), max_value=int(df['qt_imoveis'].max()), step=1)
        max_vacancia = st.number_input("Vacância Máxima (%)", value=20.0, min_value=float(df['vacancia'].min()), max_value=float(df['vacancia'].max()), step=1.0)

    # Aplicando filtros
    df_filtrado = df[
        (df['cotação'] >= min_cotacao) &
        (df['dividend_yield'] >= min_dy) &
        (df['valor_mercado'] >= min_valor_mercado) &
        (df['liquidez'] >= min_liquidez) &
        (df['qt_imoveis'] >= min_qt_imoveis) &
        (df['vacancia'] <= max_vacancia)
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
            'valor_mercado': 'R$ {:.0f}',
            'liquidez': 'R$ {:.0f}',
            'vacancia': '{:.2f}%',
            'qt_imoveis': '{:d}'
        })
    )
    st.write(f"Total de FIIs encontrados: {len(df_filtrado)}")

if __name__ == "__main__":
    main()