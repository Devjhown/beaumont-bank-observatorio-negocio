"""
Cria o banco SQLite do projeto a partir do schema (sql/schema.sql)
e popula as tabelas com os dados brutos do dataset Berka.
"""
import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
DB_PATH = os.path.join(BASE_DIR, 'data', 'beaumont_bank.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'sql', 'schema.sql')
ACCOUNT_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'account.asc')
LOAN_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'loan.asc')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

with open(SCHEMA_PATH, encoding='utf-8') as arquivo_schema:
    cursor.executescript(arquivo_schema.read())

account = pd.read_csv(ACCOUNT_PATH, sep=';')
loan = pd.read_csv(LOAN_PATH, sep=';')

account.to_sql('account', conn, if_exists='replace', index=False)
loan.to_sql('loan', conn, if_exists='replace', index=False)

conn.commit()

print(f"account: {cursor.execute('SELECT COUNT(*) FROM account').fetchone()[0]} linhas")
print(f"loan: {cursor.execute('SELECT COUNT(*) FROM loan').fetchone()[0]} linhas")

conn.close()
