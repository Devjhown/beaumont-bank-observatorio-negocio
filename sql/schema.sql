-- ============================================================
-- schema.sql
-- Observatório de Negócio — Beaumont Bank
-- Estrutura relacional do banco de dados (dataset Berka)
-- ============================================================

-- Conta bancária: unidade central do relacionamento com o cliente
CREATE TABLE account (
  account_id INT PRIMARY KEY,
  district_id INT,
  frequency TEXT,
  date DATE
);

-- Empréstimo: vinculado a uma conta existente (account_id como chave estrangeira)
CREATE TABLE loan (
  loan_id INT PRIMARY KEY,
  account_id INT,
  date DATE,
  amount DECIMAL,
  duration INT,
  payments DECIMAL,
  status TEXT,
  FOREIGN KEY (account_id) REFERENCES account(account_id)
);
