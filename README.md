# 📊 Observatório de Negócio

Projeto de dados ponta a ponta sobre uma carteira bancária real, construído enquanto aprendo a trilha de **Ciência de Dados** — do dado bruto ao insight de negócio, e do insight ao modelo preditivo, do jeito que se faz de verdade no mercado.

> 👀 **Não é da área técnica ou só quer ver funcionando rápido?** Abra [`para-recrutadores/demo.html`](para-recrutadores/demo.html) — uma página única que abre em qualquer navegador, sem instalar nada, com os KPIs, os gráficos e um simulador de risco interativo.

## 🎯 Problema de negócio

Como está a saúde da carteira de contas e empréstimos do banco? Onde estão os riscos de inadimplência, e onde estão as oportunidades de receita?

O projeto responde isso em duas camadas: **análise** (KPIs, dashboards, EDA) e **previsão** (um modelo que classifica o risco de um empréstimo antes de ele acontecer).

## 🗂️ Dataset

**[Berka Dataset (PKDD'99 Financial Dataset)](https://www.kaggle.com/datasets/marceloventura/the-berka-dataset)**

Dados reais anonimizados de um banco tcheco, com 8 tabelas relacionadas (`account`, `client`, `disp`, `order`, `trans`, `loan`, `card`, `district`), incluindo mais de 1 milhão de transações e 682 empréstimos.

## 📈 KPIs e o modelo

**Camada de análise** (`src/eda.py`, `src/kpis.py`, `src/dashboard_excel.py`):
- Ticket médio de empréstimo · Taxa de inadimplência · Distribuição de valores e prazos · Volume total emprestado

> Nota: os dados recuperados cobrem apenas as tabelas `account` e `loan` do dataset Berka (2 das 8 originais). Métricas por região ou perfil de cliente exigiriam as tabelas `district`/`client`, não incluídas aqui.

**Camada de previsão** (`src/classificacao_risco.py`, `app.py`):
- Classificação de risco de crédito (`status` do empréstimo: A/B/C/D) — Árvore de Decisão vs. KNN, com o melhor modelo exportado (`modelo_arvore.pkl`) e disponível para teste interativo na demo Streamlit

## 🛠️ Stack

| Etapa | Ferramenta | Onde |
|---|---|---|
| Lógica e KPIs | Python | `src/kpis.py` |
| Machine Learning | Scikit-Learn (Árvore de Decisão, KNN) | `src/classificacao_risco.py` |
| Modelagem e consultas | SQL (SQLite) | `sql/`, `src/criar_banco_sqlite.py` |
| Limpeza e EDA | Pandas + Matplotlib | `src/eda.py`, `reports/` |
| Dashboard | Excel (openpyxl) | `src/dashboard_excel.py` → `reports/dashboard.xlsx` |
| Demo interativa | Streamlit | `app.py` |
| Escala | Google Cloud Run (Docker) | `Dockerfile`, `DEPLOY.md` |

## ▶️ Como rodar

```bash
pip install -r requirements.txt

# 1. Cria o banco SQLite a partir dos dados brutos
python src/criar_banco_sqlite.py

# 2. Treina o modelo de risco de crédito
python src/classificacao_risco.py

# 3. Gera a EDA (gráficos + relatório em reports/)
python src/eda.py

# 4. Gera o dashboard em Excel (reports/dashboard.xlsx)
python src/dashboard_excel.py

# 5. Sobe a demo interativa
streamlit run app.py
```

Para publicar a demo na nuvem, veja o passo a passo em [`DEPLOY.md`](DEPLOY.md).

## 📁 Estrutura do repositório

```
beaumont-bank/
├── README.md
├── LICENSE
├── DEPLOY.md
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── .gitignore
├── app.py                       # demo interativa (Streamlit)
├── data/
│   ├── beaumont_bank.db         # banco SQLite gerado (account, loan)
│   └── raw/
│       ├── account.asc          # tabela account do dataset Berka
│       └── loan.asc             # tabela loan do dataset Berka
├── sql/
│   ├── schema.sql                # estrutura relacional (account, loan)
│   └── consultas_referencia.sql  # queries de referência (INSERT, SELECT, UPDATE)
├── src/
│   ├── kpis.py                   # funções de KPI (total de vendas, ticket médio, status de meta)
│   ├── classificacao_risco.py    # treino do modelo de risco de crédito (Árvore vs. KNN)
│   ├── criar_banco_sqlite.py     # cria e popula o banco a partir do schema + dados brutos
│   ├── eda.py                    # análise exploratória: gráficos + relatório
│   └── dashboard_excel.py        # gera o dashboard em Excel
├── reports/
│   ├── eda_report.md             # relatório gerado pela EDA
│   ├── dashboard.xlsx            # dashboard gerado
│   └── figures/                  # gráficos gerados pela EDA
└── models/
    └── modelo_arvore.pkl         # modelo de Árvore de Decisão treinado e exportado
```

## 🚧 Status do projeto

Construído em **sprints**, buscando aplicar práticas ágeis (entregas incrementais, revisão constante do que já estava pronto).

- [x] **Sprint 0 — Fundação** — repositório, README, dataset definido
- [x] **Sprint 1 — Python** — motor de KPIs
- [x] **Sprint 2 — Machine Learning** — modelo de risco de crédito (Árvore de Decisão vs. KNN), exportado
- [x] **Sprint 3 — SQL** — banco SQLite criado e populado
- [x] **Sprint 4 — EDA** — relatório e gráficos gerados a partir dos dados reais
- [x] **Sprint 5 — Dashboard** — planilha Excel com KPIs e gráfico
- [x] **Sprint 6 — Demo interativa** — app Streamlit com KPIs, gráficos e simulador de risco
- [x] **Sprint 7 — Deploy** — Dockerfile e guia de publicação no Google Cloud Run prontos (implantação real fica a critério de quem for rodar, pois depende de conta própria no GCP)

## 🧠 Metodologia

Cada sprint partiu de um problema real de negócio antes de virar código: primeiro o objetivo (o que essa etapa precisa responder para o banco), depois a técnica, depois a aplicação nesta base de código — sempre buscando entregas pequenas e incrementais, no espírito ágil.

## 👤 Autor

Jhonatas Pereira — iniciando carreira em Ciência de Dados, buscando gerar valor real em problemas de negócio através de dados. Este repositório é um exemplo desse processo aplicado a um problema real de crédito bancário: do dado bruto à entrega final.

📫 Contato: *[adicione aqui seu LinkedIn / GitHub / e-mail]*
