SELECT 
    ano,
    SUM(valor_producao_arroz) AS total_arroz,
    SUM(valor_producao_cafe) AS total_cafe,
    SUM(valor_producao_milho) AS total_milho,
    SUM(valor_producao_feijao) AS total_feijao,
    SUM(efetivo_bovino) AS total_bovino
FROM tbl_detalhada_culturas_agro_mg
WHERE ano IN (1985, 2000, 2023)
GROUP BY ano
ORDER BY ano ASC;

