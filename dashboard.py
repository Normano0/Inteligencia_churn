import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

tabela = pd.read_csv('online_retail_customer_churn.csv')
tabela =tabela.rename(columns={'Customer_ID':'ID','Age':'Idade', 'Gender':'Genero', 'Annual_Income':'Renda_Anual', 
    'Num_of_Purchases':'Num_Compras', 'Average_Transaction_Amount':'Valor_Medio_Transacao',
      'Last_Purchase_Days_Ago':'Ultima_Compra_Dias'})

tabela_normal = tabela.copy()
colunas_normal = ['Idade', 'Renda_Anual', 'Num_Compras', 'Valor_Medio_Transacao', 'Ultima_Compra_Dias']

min_max_para = {}
for col in colunas_normal:
    min_val = tabela[col].min()
    max_val = tabela[col].max()
    min_max_para[col] = {'min': min_val, 'max': max_val}
    if max_val != min_val: 
        tabela_normal[col] = (tabela[col] -  min_val) / (max_val - min_val)
    else:
        tabela_normal[col] = 0 


idade_categoria = [17,29,44,59, tabela['Idade'].max()]
labels_idade = ['18-29 anos', '30-44 anos', '45-59 anos', '60+ anos']
tabela["Faixa_Etaria"] =pd.cut(tabela['Idade'], bins=idade_categoria, labels=labels_idade)
#print(tabela[['Idade', 'Faixa_Etaria']].head())

engajamento_categoria = [0, 25, 75, tabela['Num_Compras'].max()]
labels_engajamento = ['Baixo','Médio','Alto']
tabela['Engajamento'] = pd.cut(tabela['Num_Compras'], bins=engajamento_categoria, labels=labels_engajamento)
#print(tabela[['Num_Compras', 'Engajamento']])

valorCliente_categoria = [0, 150, 350, tabela['Valor_Medio_Transacao'].max()]
labels_ValorCLiente = ['Baixo Valor', 'Médio Valor', 'Alto Valor']
tabela['Valor_Cliente'] = pd.cut(tabela['Valor_Medio_Transacao'], bins=valorCliente_categoria, labels=labels_ValorCLiente)
#print(tabela[['Valor_Medio_Transacao','Valor_Cliente']].head())

tabela['Cliente_Risco'] = np.where(tabela['Ultima_Compra_Dias']> 180, 'Sim', 'Não')
#print(tabela[['Ultima_Compra_Dias', 'Cliente_Risco']].head())


st.title("Dashboard Inteligência para negócios")

st.sidebar.header("Filtros do Dashboard")

filtro_risco = st.sidebar.selectbox("Cliente em Risco?", options=["Todos", "Sim", "Não"])

filtro_genero =st.sidebar.selectbox("Gênero do Cliente:", options=["Todos"] + list(tabela['Genero'].unique()))

tabela_filtro = tabela.copy()
if filtro_risco != 'Todos':
    tabela_filtro = tabela_filtro[tabela_filtro["Cliente_Risco"] == filtro_risco]

if filtro_genero != "Todos":
    tabela_filtro = tabela_filtro[tabela_filtro['Genero'] == filtro_genero]

plot_faixa = (tabela_filtro["Faixa_Etaria"].value_counts().reset_index())
grafico_faixa = px.bar(plot_faixa, x="Faixa_Etaria", y="count", 
                       title="Clientes por Faixa Etária", labels={"count":"Quantidade", "Faixa_Etaria":"Faixa Etária"},)

plot_valor = (tabela_filtro['Valor_Cliente'].value_counts().reset_index())
grafico_valor = px.bar(plot_valor, x="Valor_Cliente", y="count", title="Clientes por categoraia de Valor",
                       labels={"count":"Quantidade", "Valor_Cliente":"Categoria de Valor"},)

plot_engajamento = (tabela_filtro['Engajamento'].value_counts().reset_index())
grafico_engajamento = px.bar(plot_engajamento, x="Engajamento",y="count", title="Clientes por nível de Engajamento",
                             labels={"count":"Quantidade", "Engajamento":"Nível de Engajamento"},)


kpi1, kpi2, kpi3 = st.columns(3)

total_clientes = len(tabela_filtro)

ticket_medio = tabela_filtro['Valor_Medio_Transacao'].mean()

if len(tabela_filtro) > 0:
    total_risco = len(tabela_filtro[tabela_filtro["Cliente_Risco"] == "Sim"])
    taxa_risco = (total_risco/total_clientes)*100
else:
    taxa_risco = 0

with kpi1:
    st.metric(label="Total de Clientes", value=f"{total_clientes}")

with kpi2:
    st.metric(label="Ticket Médio Geral", value=f"${ticket_medio:.2f}")

with kpi3:
    st.metric(label="Taxa de Clientes em Risco:", value=f"{taxa_risco:.1f}%")

st.markdown("---")

col1, col2, col3 =st.columns(3)


with col1:
    st.plotly_chart(grafico_faixa, use_container_width=True)

with col2:
    st.plotly_chart(grafico_valor, use_container_width=True)

with col3:
    st.plotly_chart(grafico_engajamento, use_container_width=True)

#pra rodar o streamlit, abre o terminal e põe: streamlit run dashboard.py