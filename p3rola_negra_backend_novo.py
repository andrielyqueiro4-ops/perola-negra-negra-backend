# -*- coding: utf-8 -*-
"""Backend Pérola Negra - versão para Streamlit Cloud"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações da página
st.set_page_config(page_title="💎 Pérola Negra - Bot Analítico", layout="wide")

st.title("💎 Painel Analítico - Pérola Negra")

# Função para carregar dados
def carregar_dados(uploaded_file=None):
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_excel("alpha_pet_insights.xlsx")
    return df

# Upload da planilha
uploaded_file = st.file_uploader("📂 Envie sua planilha de vendas (Excel)", type=["xlsx"])
usar_alpha = st.button("Usar dados Alpha Pet Insights")

if uploaded_file or usar_alpha:
    df = carregar_dados(uploaded_file if uploaded_file else None)
    st.success("✅ Planilha carregada com sucesso!")

    # Cálculos principais
    receita_total = df["Receita"].sum()
    transacoes = len(df)
    ticket_medio = receita_total / transacoes if transacoes > 0 else 0
    produto_top = df.groupby("Produto")["Receita"].sum().idxmax()

    # Exibição dos indicadores principais
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Receita Total", f"R$ {receita_total:,.2f}")
    col2.metric("🧾 Transações", transacoes)
    col3.metric("🎟️ Ticket Médio", f"R$ {ticket_medio:,.2f}")
    col4.metric("🏆 Produto Top", produto_top)

    st.divider()

    # Gráfico de pizza por categoria
    if "Categoria" in df.columns:
        fig_cat = px.pie(df, names="Categoria", values="Receita", title="📊 Receita por Categoria")
        st.plotly_chart(fig_cat, use_container_width=True)
    else:
        st.warning("⚠️ A coluna 'Categoria' não foi encontrada na planilha.")

    # Gráfico de barras por região
    if "Região" in df.columns:
        fig_reg = px.bar(df, x="Região", y="Receita", title="📈 Receita por Região", color="Região")
        st.plotly_chart(fig_reg, use_container_width=True)
    else:
        st.warning("⚠️ A coluna 'Região' não foi encontrada na planilha.")
else:
    st.info("📄 Envie uma planilha ou clique em 'Usar dados Alpha Pet Insights' para começar.")
