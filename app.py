"""
Demo interativa — Observatório de Negócio (Beaumont Bank)

Rode com: streamlit run app.py
(a partir da raiz do projeto, com as dependências de requirements.txt instaladas)
"""
import os
import pickle
import sqlite3

import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'data', 'beaumont_bank.db')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'modelo_arvore.pkl')

st.set_page_config(page_title='Observatório de Negócio — Beaumont Bank', layout='wide')


@st.cache_data
def carregar_dados():
    conn = sqlite3.connect(DB_PATH)
    loan = pd.read_sql('SELECT * FROM loan', conn)
    conn.close()
    loan['inadimplente'] = loan['status'].isin(['B', 'D'])
    return loan


@st.cache_resource
def carregar_modelo():
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)


loan = carregar_dados()
modelo = carregar_modelo()

st.title('📊 Observatório de Negócio — Beaumont Bank')
st.caption('Análise e previsão de risco de crédito sobre o dataset Berka (banco tcheco)')

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric('Total de empréstimos', f"{len(loan)}")
col2.metric('Total emprestado', f"{loan['amount'].sum():,.0f} CZK")
col3.metric('Ticket médio', f"{loan['amount'].mean():,.0f} CZK")
col4.metric('Taxa de inadimplência', f"{loan['inadimplente'].mean():.1%}")

st.divider()

# --- Gráficos ---
col_esq, col_dir = st.columns(2)
with col_esq:
    st.subheader('Distribuição do valor dos empréstimos')
    st.bar_chart(loan['amount'].value_counts(bins=20).sort_index())
with col_dir:
    st.subheader('Empréstimos por status')
    st.bar_chart(loan['status'].value_counts().sort_index())

st.divider()

# --- Demo do modelo preditivo ---
st.subheader('🔮 Simular risco de um novo empréstimo')
st.write('Preencha os dados de um empréstimo hipotético e veja a classificação do modelo (Árvore de Decisão).')

col_a, col_b, col_c = st.columns(3)
with col_a:
    account_id = st.number_input('ID da conta', min_value=1, value=1787)
with col_b:
    valor = st.number_input('Valor do empréstimo (CZK)', min_value=1000, value=96396, step=1000)
with col_c:
    duracao = st.selectbox('Duração (meses)', [12, 24, 36, 48, 60], index=2)

data_ref = st.number_input('Data (AAMMDD, formato do dataset)', min_value=930101, value=930705)
parcela = round(valor / duracao, 2)
st.caption(f'Parcela mensal calculada automaticamente: {parcela:,.2f} CZK')

if st.button('Classificar risco'):
    entrada = pd.DataFrame([{
        'loan_id': 0,
        'account_id': account_id,
        'date': data_ref,
        'amount': valor,
        'duration': duracao,
        'payments': parcela,
    }])
    predicao = modelo.predict(entrada)[0]
    mapa_status = {
        'A': ('✅ Baixo risco', 'contrato tende a ser pago sem problemas'),
        'B': ('⚠️ Risco elevado', 'padrão histórico associado a atraso'),
        'C': ('✅ Baixo risco', 'padrão histórico de contratos em dia'),
        'D': ('🔴 Alto risco', 'padrão histórico associado a inadimplência'),
    }
    rotulo, explicacao = mapa_status.get(predicao, (predicao, ''))
    st.metric('Classificação do modelo', rotulo)
    st.caption(explicacao)

st.divider()
st.caption(
    'Dados: dataset Berka (subset account + loan). '
    'Modelo: Árvore de Decisão treinada em src/classificacao_risco.py.'
)
