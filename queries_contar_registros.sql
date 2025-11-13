-- ============================================
-- QUERIES PARA CONTAR REGISTROS NO BANCO db_mqtt_teste
-- Execute estas queries no PHPMyAdmin
-- ============================================

-- 1. Contagem por tabela da aplicação (principal)
SELECT 
    'corrente_brunidores' as tabela, 
    COUNT(*) as total_registros 
FROM corrente_brunidores
UNION ALL
SELECT 'corrente_descascadores', COUNT(*) FROM corrente_descascadores
UNION ALL
SELECT 'corrente_polidores', COUNT(*) FROM corrente_polidores
UNION ALL
SELECT 'temperaturas', COUNT(*) FROM temperaturas
UNION ALL
SELECT 'umidades', COUNT(*) FROM umidades
UNION ALL
SELECT 'grandezas_eletricas', COUNT(*) FROM grandezas_eletricas
UNION ALL
SELECT 'dados_agregados', COUNT(*) FROM dados_agregados
ORDER BY tabela;

-- 2. Lista todas as tabelas com contagem aproximada (rápido)
SELECT 
    TABLE_NAME as tabela,
    TABLE_ROWS as registros_aproximados,
    ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024), 2) AS tamanho_mb
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'db_mqtt_teste'
ORDER BY TABLE_NAME;

-- 3. Contagem exata de todas as tabelas (pode ser lento em bancos grandes)
-- Execute esta query para cada tabela individualmente ou use o script Python

-- 4. Estatísticas de agregação (registros agregados vs não agregados)
SELECT 
    'corrente_brunidores' as tabela,
    COUNT(*) as total,
    SUM(CASE WHEN agregado = 1 THEN 1 ELSE 0 END) as agregados,
    SUM(CASE WHEN agregado = 0 THEN 1 ELSE 0 END) as nao_agregados
FROM corrente_brunidores
UNION ALL
SELECT 
    'corrente_descascadores',
    COUNT(*),
    SUM(CASE WHEN agregado = 1 THEN 1 ELSE 0 END),
    SUM(CASE WHEN agregado = 0 THEN 1 ELSE 0 END)
FROM corrente_descascadores
UNION ALL
SELECT 
    'corrente_polidores',
    COUNT(*),
    SUM(CASE WHEN agregado = 1 THEN 1 ELSE 0 END),
    SUM(CASE WHEN agregado = 0 THEN 1 ELSE 0 END)
FROM corrente_polidores
UNION ALL
SELECT 
    'temperaturas',
    COUNT(*),
    SUM(CASE WHEN agregado = 1 THEN 1 ELSE 0 END),
    SUM(CASE WHEN agregado = 0 THEN 1 ELSE 0 END)
FROM temperaturas
UNION ALL
SELECT 
    'umidades',
    COUNT(*),
    SUM(CASE WHEN agregado = 1 THEN 1 ELSE 0 END),
    SUM(CASE WHEN agregado = 0 THEN 1 ELSE 0 END)
FROM umidades
UNION ALL
SELECT 
    'grandezas_eletricas',
    COUNT(*),
    SUM(CASE WHEN agregado = 1 THEN 1 ELSE 0 END),
    SUM(CASE WHEN agregado = 0 THEN 1 ELSE 0 END)
FROM grandezas_eletricas;

-- 5. Contagem exata de cada tabela individual (copie e execute uma por vez)
-- Corrente Brunidores
SELECT COUNT(*) as total FROM corrente_brunidores;

-- Corrente Descascadores
SELECT COUNT(*) as total FROM corrente_descascadores;

-- Corrente Polidores
SELECT COUNT(*) as total FROM corrente_polidores;

-- Temperaturas
SELECT COUNT(*) as total FROM temperaturas;

-- Umidades
SELECT COUNT(*) as total FROM umidades;

-- Grandezas Elétricas
SELECT COUNT(*) as total FROM grandezas_eletricas;

-- Dados Agregados
SELECT COUNT(*) as total FROM dados_agregados;

-- 6. Resumo geral
SELECT 
    (SELECT COUNT(*) FROM corrente_brunidores) +
    (SELECT COUNT(*) FROM corrente_descascadores) +
    (SELECT COUNT(*) FROM corrente_polidores) +
    (SELECT COUNT(*) FROM temperaturas) +
    (SELECT COUNT(*) FROM umidades) +
    (SELECT COUNT(*) FROM grandezas_eletricas) +
    (SELECT COUNT(*) FROM dados_agregados) as total_geral_aplicacao;

