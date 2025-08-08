import streamlit as st
import pandas as pd 
import plotly.express as px

st.set_page_config(page_title="Dashboard de Salários na Área de Dados", page_icon="📊", layout="wide")

df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

st.sidebar.header("🔍Filtros")

anos_disponiveis = sorted(df["ano"].unique())
anos_selecionados = st.sidebar.multiselect("Ano:",anos_disponiveis, default=anos_disponiveis)

senioridades_disponiveis = sorted(df["senioridade"].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade:", senioridades_disponiveis, default=senioridades_disponiveis)  

contratos_disponiveis = sorted(df["contrato"].unique())
contratos_selecionados = st.sidebar.multiselect("Contrato:", contratos_disponiveis, default=contratos_disponiveis)  

tamanhos_disponiveis = sorted(df["tamanho_empresa"].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa:", tamanhos_disponiveis, default=tamanhos_disponiveis)   

df_filtrado = df[
    (df["ano"].isin(anos_selecionados)) &       
    (df["senioridade"].isin(senioridades_selecionadas)) &
    (df["contrato"].isin(contratos_selecionados)) & 
    (df["tamanho_empresa"].isin(tamanhos_selecionados))
]

st.title("🎲 Dashboard de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Ultilize os filtros na barra lateral para personalizar a visualização.")

st.subheader("Métricas Gerais (Salário Anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado["usd"].mean()
    salario_maximo = df_filtrado["usd"].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio, salario_maximo, total_registros, cargo_mais_frequente = 0, 0, 0, "N/A"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário Médio (USD)", f"${salario_medio:,.2f}")
col2.metric("Salário Máximo (USD)", f"${salario_maximo:,.2f}")
col3.metric("Total de Registros", f"${total_registros:,.2f}")      
col4.metric("Cargo Mais Frequente", cargo_mais_frequente)

st.markdown("---")

st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)    

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(top_cargos, x='usd', y='cargo', orientation='h', title="Top 10 Cargos por Salário Médio", labels={'usd': 'Média Salarial Anula (USD)', 'cargo': ''})
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_senioridade = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title="Distribuição Salarial Anual",
            labels={'usd': 'Faixa Salarial (USD)', 'count': ''}
        )
        grafico_senioridade.update_layout(title_x=0.1)
        st.plotly_chart(grafico_senioridade, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        contagem_remoto = df_filtrado['remoto'].value_counts().reset_index()
        contagem_remoto.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
              contagem_remoto,
              values='quantidade',
              names='tipo_trabalho',
              title="Proporção dos Tipos de Trabalho",
              hole=0.5
         )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)   
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
                    locations='residencia_iso3',
                    color='usd',
                    color_continuous_scale='rdylgn',
                    title='Média de Salário de Cientista de Dados por País',
                    labels={'usd': 'Salário Médio Anual (USD)', 'residencia_iso3': 'País'},
                    )
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
    
st.subheader("Tabela de Dados Detalhados")
st.dataframe(df_filtrado)