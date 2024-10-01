SELECT 
    ip.[ANO],
    per.[UF],
    ip.[Local],
    per.[Região],
    ip.[IDH],
    ip.[Populacao],
    per.[Soma de PIB] AS PIB,
    per.[Soma de PIB_Per_Capita] AS PIB_Per_Capita,
    per.[DataCarga]
INTO 
    [AcompanhamentoOrcamentario].[dbo].[IDH_Populacao_PIB_Estado_Regiao]
FROM 
    [AcompanhamentoOrcamentario].[dbo].[IDH_Populacao] ip
INNER JOIN 
    [AcompanhamentoOrcamentario].[dbo].[PIB_Estado_Regiao] per
ON 
    ip.[ANO] = per.[Ano] AND ip.[Local] = per.[Local];
