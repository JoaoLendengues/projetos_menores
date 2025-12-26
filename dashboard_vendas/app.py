import pandas as pd
import streamlit as st
import plotly.express as px


# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon='📊',
    layout='wide'
)

st.title('📊 Dashboard de Análise de Vendas')

# Upload do arquivo
arquivo = st.file_uploader(
   'Faça um upload do arquivo de vendas (.xlsx)',
   type=['xlsx'] 
)

if arquivo:
    df = pd.read_excel(arquivo)
    st.write('Colunas do arquivo:', df.columns.tolist())

    # Tratamento básico
    df['data'] = pd.to_datetime(df['data'])

    # KPIs
    total_vendas = df['VALOR'].sum()
    total_itens = df['QUANTIDADE'].sum()
    ticket_medio = total_vendas / total_itens

    col1, col2, col3, = st.columns(3)

    col1.metric('💰 Total de Vendas', f'R$ {total_vendas:,.2f}')
    col2.metric('📦 Itens Vendidos', int(total_itens))
    col3.metric('📊 Ticket médio', f'R$ {ticket_medio:,.2f}')

    st.divider()

    # vendas por mês
    vendas_mes = (
        df
        .groupby(df['data'].dt.to_period('M'))['VALOR']
        .sum()
        .reset_index()
    )

    vendas_mes['data'] = vendas_mes['data'].astype(str)

    fig_mes = px.bar(
        vendas_mes,
        x='data',
        y='VALOR',
        title='Vendas por Mês'
    )

    st.plotly_chart(fig_mes, use_container_width=True)

    # Vendas por categoria
    fig_categoria = px.pie(
        df,
        names='CATEGORIA',
        values='VALOR',
        title='Vendas por Categoria'
    )

    st.plotly_chart(fig_categoria, use_container_width=True)

else:
    st.info('📂 Envie um arquivo Excel para iniciar a análise.')
