-- ============================================================
-- consultas_referencia.sql
-- Observatório de Negócio — Beaumont Bank
-- Consultas de referência sobre a carteira de empréstimos
-- ============================================================

-- Popula a tabela de empréstimos a partir de uma base já existente,
-- em vez de inserir valores manualmente
INSERT INTO loan (loan_id, account_id, date, amount, duration, payments, status)
SELECT loan_id, account_id, date, amount, duration, payments, status
FROM loan_origem;

-- Relatório: empréstimos de valor médio (entre 50.000 e 150.000),
-- do maior para o menor
SELECT * FROM loan
WHERE amount BETWEEN 50000 AND 150000
ORDER BY amount DESC;

-- Exibe o status do empréstimo com um nome mais descritivo no relatório
SELECT status AS situacao FROM loan;

-- Correção pontual de um registro, solicitada pela área de risco
-- (sempre confirmar a linha certa com um SELECT antes de alterar)
SELECT * FROM loan WHERE loan_id = 5314;
UPDATE loan SET status = 'A' WHERE loan_id = 5314;

-- Exemplo de exclusão segura (não executar sem necessidade real de negócio):
-- SELECT * FROM loan WHERE status = 'cancelado';
-- DELETE FROM loan WHERE status = 'cancelado';
