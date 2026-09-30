"""
Análise Exploratória de Dados (EDA) — Observatório de Negócio (Beaumont Bank)

Lê o banco SQLite (data/beaumont_bank.db), gera gráficos em reports/figures/
e um resumo em reports/eda_report.md com os principais achados sobre a
carteira de empréstimos.
"""
import os
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
DB_PATH = os.path.join(BASE_DIR, 'data', 'beaumont_bank.db')
FIG_DIR = os.path.join(BASE_DIR, 'reports', 'figures')
REPORT_PATH = os.path.join(BASE_DIR, 'reports', 'eda_report.md')

conn = sqlite3.connect(DB_PATH)
loan = pd.read_sql('SELECT * FROM loan', conn)
account = pd.read_sql('SELECT * FROM account', conn)
conn.close()

# status: A = pago sem problemas, B = pago mas com atraso no passado (contrato encerrado),
# C = em dia (contrato ativo), D = inadimplente (contrato ativo com problema)
loan['inadimplente'] = loan['status'].isin(['B', 'D'])

total_emprestado = loan['amount'].sum()
ticket_medio = loan['amount'].mean()
taxa_inadimplencia = loan['inadimplente'].mean()
duracao_media = loan['duration'].mean()

# --- Gráfico 1: distribuição do valor dos empréstimos ---
plt.figure(figsize=(8, 5))
plt.hist(loan['amount'], bins=30, color='#2b6cb0', edgecolor='white')
plt.title('Distribuição do valor dos empréstimos')
plt.xlabel('Valor (CZK)')
plt.ylabel('Quantidade de empréstimos')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, '01_distribuicao_valor.png'), dpi=120)
plt.close()

# --- Gráfico 2: taxa de inadimplência por status ---
status_counts = loan['status'].value_counts().sort_index()
plt.figure(figsize=(6, 5))
cores = ['#2f855a' if s in ('A', 'C') else '#c53030' for s in status_counts.index]
plt.bar(status_counts.index, status_counts.values, color=cores)
plt.title('Quantidade de empréstimos por status')
plt.xlabel('Status (A/C = adimplente, B/D = inadimplente)')
plt.ylabel('Quantidade')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, '02_status_emprestimos.png'), dpi=120)
plt.close()

# --- Gráfico 3: valor médio do empréstimo por duração ---
media_por_duracao = loan.groupby('duration')['amount'].mean().sort_index()
plt.figure(figsize=(8, 5))
plt.plot(media_por_duracao.index, media_por_duracao.values, marker='o', color='#805ad5')
plt.title('Valor médio do empréstimo por prazo (meses)')
plt.xlabel('Duração (meses)')
plt.ylabel('Valor médio (CZK)')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, '03_valor_por_duracao.png'), dpi=120)
plt.close()

# --- Gráfico 4: taxa de inadimplência por faixa de duração ---
taxa_por_duracao = loan.groupby('duration')['inadimplente'].mean().sort_index()
plt.figure(figsize=(8, 5))
plt.bar(taxa_por_duracao.index.astype(str), taxa_por_duracao.values, color='#dd6b20')
plt.title('Taxa de inadimplência por prazo do empréstimo')
plt.xlabel('Duração (meses)')
plt.ylabel('Taxa de inadimplência')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, '04_inadimplencia_por_duracao.png'), dpi=120)
plt.close()

relatorio = f"""# Relatório de EDA — Observatório de Negócio (Beaumont Bank)

Gerado automaticamente por `src/eda.py` a partir de `data/beaumont_bank.db`.

## Visão geral da carteira

| Métrica | Valor |
|---|---|
| Total de empréstimos | {len(loan)} |
| Total emprestado | {total_emprestado:,.2f} CZK |
| Ticket médio | {ticket_medio:,.2f} CZK |
| Duração média | {duracao_media:.1f} meses |
| Taxa de inadimplência (status B/D) | {taxa_inadimplencia:.1%} |
| Total de contas | {len(account)} |

## Distribuição do valor dos empréstimos
![Distribuição do valor](figures/01_distribuicao_valor.png)

A maior parte dos empréstimos se concentra nas faixas de menor valor, com uma
cauda longa de contratos de valores mais altos.

## Empréstimos por status
![Status dos empréstimos](figures/02_status_emprestimos.png)

- **A**: contrato encerrado, pago sem problemas
- **B**: contrato encerrado, mas com atraso no passado (inadimplência)
- **C**: contrato ativo, em dia
- **D**: contrato ativo, com problema (inadimplência)

## Valor médio por prazo do empréstimo
![Valor por duração](figures/03_valor_por_duracao.png)

## Taxa de inadimplência por prazo
![Inadimplência por duração](figures/04_inadimplencia_por_duracao.png)

Prazos mais longos tendem a concentrar contratos de maior valor — vale
observar se também concentram maior risco, o que reforça a necessidade do
modelo de classificação de risco (`src/classificacao_risco.py`).

## Limitação dos dados

Esta análise usa apenas as tabelas `account` e `loan` do dataset Berka
(as únicas recuperadas). O dataset completo tem também `district`, `client`,
`disp`, `trans` e `card`, que permitiriam quebras por região e por perfil de
cliente — não incluídas aqui por falta desses arquivos.
"""

with open(REPORT_PATH, 'w', encoding='utf-8') as f:
    f.write(relatorio)

print('EDA concluída.')
print(f'Total emprestado: {total_emprestado:,.2f} CZK')
print(f'Ticket médio: {ticket_medio:,.2f} CZK')
print(f'Taxa de inadimplência: {taxa_inadimplencia:.1%}')
print(f'Relatório salvo em: {REPORT_PATH}')
