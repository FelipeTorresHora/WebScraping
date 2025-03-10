import streamlit as st
import pandas as pd
import plotly.express as px
from data import obter_dados_fiis, get_historical_data
from ml import prever_preco_prophet

def main():
    st.set_page_config(page_title="Dashboard FIIs", layout="wide")
    
    st.title("Dashboard de Fundos Imobiliários")
    
    # Carregar os dados atuais dos FIIs
    try:
        df = obter_dados_fiis()
    except Exception as e:
        st.error(str(e))
        return
    
    # Configurar o botão de rádio na barra lateral
    st.sidebar.header("Selecione a Categoria")
    categoria = st.sidebar.radio(
        "Escolha uma categoria:",
        ["Sobre o Projeto", "Filtros Avançados", "Análise Avançada"]
    )

    # Lógica para cada categoria
    if categoria == "Sobre o Projeto":
        st.markdown(
            "Este é um projeto de dashboard de Fundos Imobiliários (FIIs) desenvolvido com Streamlit. "
            "O objetivo é mostrar informações sobre FIIs, filtrar por diversos critérios e realizar análises avançadas."
        )
    elif categoria == "Filtros Avançados":
        st.sidebar.subheader("Filtros Avançados")
        
        # Pesquisa por código
        pesquisa_codigo = st.sidebar.text_input("Pesquisar por Código (ex.: MXRF11)", "").upper()
        df_filtered_by_code = df
        if pesquisa_codigo:
            df_filtered_by_code = df[df['código'].str.contains(pesquisa_codigo, case=True)]
            if df_filtered_by_code.empty:
                st.sidebar.warning("Nenhum FII encontrado com esse código.")
        
        # Filtros avançados em duas colunas
        col_filtros1, col_filtros2 = st.sidebar.columns(2)
        
        with col_filtros1:
            min_cotacao = st.number_input(
                "Cotação Mínima (R$)", 
                value=30.0, 
                min_value=float(df_filtered_by_code['cotação'].min()), 
                max_value=float(df_filtered_by_code['cotação'].max()), 
                step=1.0
            )
            min_dy = st.number_input(
                "Dividend Yield Mínimo (%)", 
                value=9.0, 
                min_value=float(df_filtered_by_code['dividend_yield'].min()), 
                max_value=float(df_filtered_by_code['dividend_yield'].max()), 
                step=0.1
            )
            min_valor_mercado = st.number_input(
                "Valor de Mercado Mínimo (R$)", 
                value=100000000.0, 
                min_value=float(df_filtered_by_code['valor_mercado'].min()), 
                max_value=float(df_filtered_by_code['valor_mercado'].max()), 
                step=1000000.0
            )
        
        with col_filtros2:
            min_liquidez = st.number_input(
                "Liquidez Mínima (R$)", 
                value=10000.0, 
                min_value=float(df_filtered_by_code['liquidez'].min()), 
                max_value=float(df_filtered_by_code['liquidez'].max()), 
                step=1000.0
            )
            min_qt_imoveis = st.number_input(
                "Quantidade Mínima de Imóveis", 
                value=1, 
                min_value=int(df_filtered_by_code['qt_imoveis'].min()), 
                max_value=int(df_filtered_by_code['qt_imoveis'].max()), 
                step=1
            )
            max_vacancia = st.number_input(
                "Vacância Máxima (%)", 
                value=20.0, 
                min_value=float(df_filtered_by_code['vacancia'].min()), 
                max_value=float(df_filtered_by_code['vacancia'].max()), 
                step=1.0
            )
        
        # Aplicar filtros avançados
        df_filtrado = df_filtered_by_code[
            (df_filtered_by_code['cotação'] >= min_cotacao) &
            (df_filtered_by_code['dividend_yield'] >= min_dy) &
            (df_filtered_by_code['valor_mercado'] >= min_valor_mercado) &
            (df_filtered_by_code['liquidez'] >= min_liquidez) &
            (df_filtered_by_code['qt_imoveis'] >= min_qt_imoveis) &
            (df_filtered_by_code['vacancia'] <= max_vacancia)
        ]
        
        # Visualizações no corpo principal
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribuição por Segmento")
            fig_segmentos = df_filtrado['segmento'].value_counts()
            st.bar_chart(fig_segmentos)
        
        with col2:
            st.subheader("Relação Dividend Yield x P/VP")
            st.scatter_chart(data=df_filtrado, x='dividend_yield', y='p_vp')
        
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

    elif categoria == "Análise Avançada":
        st.sidebar.subheader("Análise Avançada")
        
        # Entrada para o código do FII
        fii_code = st.sidebar.text_input("Digite o código do FII (ex: MXRF11)", "MXRF11").upper()
        if st.sidebar.button("Buscar Dados Históricos"):
            # Obter dados históricos de preço
            df_historical = get_historical_data(fii_code)
            if df_historical is None or df_historical.empty:
                st.error("Não foi possível obter dados históricos para este FII.")
            else:
                # Garantir que 'date' seja datetime
                df_historical['date'] = pd.to_datetime(df_historical['date'])
                
                # Filtrar apenas dias úteis
                df_historical = df_historical[df_historical['date'].dt.weekday < 5].copy()
                
                if df_historical.empty:
                    st.error("Nenhum dado disponível após filtrar finais de semana.")
                else:
                    # Validar dados
                    if df_historical['price'].isnull().any():
                        st.warning("Dados contêm valores ausentes. Preenchendo com interpolação.")
                        df_historical['price'] = df_historical['price'].interpolate()
                    
                    # Suavizar os preços
                    df_historical['price_smooth'] = df_historical['price'].rolling(window=5, min_periods=1).mean()
                    
                    # Visualizar dados históricos de preço (original e suavizado)
                    st.subheader("Preço Histórico (Últimos 90 Dias - Dias Úteis)")
                    fig_historical = px.line(df_historical, x='date', y=['price', 'price_smooth'],
                                           labels={'value': 'Preço (R$)', 'date': 'Data'},
                                           title=f"Preço Original e Suavizado para {fii_code}")
                    fig_historical.update_traces(line=dict(dash='dash'), selector=dict(name='price_smooth'))
                    st.plotly_chart(fig_historical)
                    
                    # Previsão com machine learning para preços futuros
                    resultados = prever_preco_prophet(df_historical)
                    if resultados is None:
                        st.error("Falha ao gerar previsão. Verifique os logs para mais detalhes.")
                    else:
                        st.write(f"Previsão de preço daqui a 30 dias úteis: R$ {resultados['ultima_previsao']:.2f}")
                        st.write(f"R² do modelo: {resultados['r2']:.2f}")
                        st.write(f"MAE do modelo: R$ {resultados['mae']:.2f}")
                        
                        # Gráfico comparativo com Plotly
                        forecast_df = resultados['forecast'][['ds', 'yhat']].rename(columns={'ds': 'date', 'yhat': 'predicted_price'})
                        historical_df = df_historical[['date', 'price_smooth']]
                        
                        fig = px.line(historical_df, x='date', y='price_smooth', 
                                    labels={'price_smooth': 'Preço Suavizado (R$)', 'date': 'Data'}, 
                                    title=f"Histórico Suavizado e Previsão de Preço para {fii_code} (Dias Úteis)")
                        fig.add_scatter(x=forecast_df['date'], y=forecast_df['predicted_price'], 
                                      mode='lines', name='Previsão', line=dict(dash='dash'))
                        st.plotly_chart(fig)
        else:
            st.info("Digite o código do FII e clique em 'Buscar Dados Históricos' para começar.")

if __name__ == "__main__":
    main()