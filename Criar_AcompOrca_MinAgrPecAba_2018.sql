-- Passo 1: Criar a tabela [AcompanhamentoOrcamentario].[dbo].[AcompOrca_MinAgrPecAba_2019]
CREATE TABLE [AcompanhamentoOrcamentario].[dbo].[_AcompOrca_MinAgrPecAba_2018] (
    [exercicio] NVARCHAR(255) NULL,
    [tipocaptacao] NVARCHAR(255) NULL,
    [esfera] NVARCHAR(255) NULL,
    [descricaoesfera] NVARCHAR(255) NULL,
    [orgao] NVARCHAR(255) NULL,
    [descricaoorgao] NVARCHAR(255) NULL,
    [unidadeorcamentaria] NVARCHAR(255) NULL,
    [descricaounidadeorcamentaria] NVARCHAR(255) NULL,
    [funcao] NVARCHAR(255) NULL,
    [descricaofuncao] NVARCHAR(255) NULL,
    [subfuncao] NVARCHAR(255) NULL,
    [descricaosubfuncao] NVARCHAR(255) NULL,
    [programa] NVARCHAR(255) NULL,
    [tituloprograma] NVARCHAR(255) NULL,
    [tipoprograma] NVARCHAR(255) NULL,
    [descricaotipoprograma] NVARCHAR(255) NULL,
    [acao] NVARCHAR(255) NULL,
    [tituloacao] NVARCHAR(255) NULL,
    [tipoacao] NVARCHAR(255) NULL,
    [produto] NVARCHAR(255) NULL,
    [descricaoproduto] NVARCHAR(255) NULL,
    [unidademedida] NVARCHAR(255) NULL,
    [descricaounidademedida] NVARCHAR(255) NULL,
    [localizador] NVARCHAR(255) NULL,
    [descricaolocalizador] NVARCHAR(255) NULL,
    [uf] NVARCHAR(255) NULL,
    [regiao] NVARCHAR(255) NULL,
    [estado] NVARCHAR(255) NULL,
    [localizadorpreenchimentoobrigatorio] NVARCHAR(255) NULL,
    [elementosemcaptacao] NVARCHAR(255) NULL,
    [qtdemetaloa] FLOAT NULL,
    [projetolei] FLOAT NULL,
    [dotacaoinicial] FLOAT NULL,
    [autorizado] FLOAT NULL,
    [empenhado] FLOAT NULL,
    [liquidado] FLOAT NULL,
    [reprogramadofisico] FLOAT NULL,
    [reprogramadofinanceiro] FLOAT NULL,
    [realizadoloa] FLOAT NULL,
    [pago] FLOAT NULL,
    [liquidadorap] FLOAT NULL,
    [realizadorap] FLOAT NULL,
    [codigo_po] NVARCHAR(255) NULL,
    [titulo_po] NVARCHAR(255) NULL,
    [produto_po] NVARCHAR(255) NULL,
    [descricaoproduto_po] NVARCHAR(255) NULL,
    [unidademedida_po] NVARCHAR(255) NULL,
    [descricaounidademedida_po] NVARCHAR(255) NULL,
    [metaloaproposta_po] FLOAT NULL,
    [dotacaoinicial_po] FLOAT NULL,
    [autorizado_po] FLOAT NULL,
    [empenhado_po] FLOAT NULL,
    [liquidado_po] FLOAT NULL, 
    [realizado_po] FLOAT NULL,
    [fisicoreprogramado_po] FLOAT NULL,
    [financeiroreprogramado_po] FLOAT NULL,
    [pago_po] FLOAT NULL,
    [liquidadorap_po] FLOAT NULL,
    [qtdemetaatual_po] FLOAT NULL,
    [qtdemetaatual] FLOAT NULL
);

-- Passo 2: Selecionar na tabela "[AcompanhamentoOrcamentario].[dbo].[_LOA_2018]" somente os registros com [descricaoorgao] = 'Minist�rio da Agricultura, Pecu�ria e Abastecimento'
-- Passos 3 a 9: Inserir os dados na tabela [AcompanhamentoOrcamentario].[dbo].[AcompOrca_MinAgrPecAba_2018] com as condi��es especificadas
INSERT INTO [AcompanhamentoOrcamentario].[dbo].[_AcompOrca_MinAgrPecAba_2018]
SELECT 
    CAST(LOA.[exercicio] AS NVARCHAR(255)) AS [exercicio],
    CAST(LOA.[tipocaptacao] AS NVARCHAR(255)) AS [tipocaptacao],
    CAST(LOA.[esfera] AS NVARCHAR(255)) AS [esfera],
    CAST(DE.[descricaoesfera] AS NVARCHAR(255)) AS [descricaoesfera],
    CAST(LOA.[orgao] AS NVARCHAR(255)) AS [orgao],
    CAST(LOA.[descricaoorgao] AS NVARCHAR(255)) AS [descricaoorgao],
    CAST(LOA.[unidadeorcamentaria] AS NVARCHAR(255)) AS [unidadeorcamentaria],
    CAST(LOA.[descricaounidadeorcamentaria] AS NVARCHAR(255)) AS [descricaounidadeorcamentaria],
    CAST(LOA.[funcao] AS NVARCHAR(255)) AS [funcao],
    CAST(LOA.[descricaofuncao] AS NVARCHAR(255)) AS [descricaofuncao],
    CAST(LOA.[subfuncao] AS NVARCHAR(255)) AS [subfuncao],
    CAST(LOA.[descricaosubfuncao] AS NVARCHAR(255)) AS [descricaosubfuncao],
    CAST(LOA.[programa] AS NVARCHAR(255)) AS [programa],
    CAST(LOA.[tituloprograma] AS NVARCHAR(255)) AS [tituloprograma],
    CAST(TP.[tipoprograma] AS NVARCHAR(255)) AS [tipoprograma],
    CAST(TP.[descricaotipoprograma] AS NVARCHAR(255)) AS [descricaotipoprograma],
    CAST(LOA.[acao] AS NVARCHAR(255)) AS [acao],
    CAST(LOA.[tituloacao] AS NVARCHAR(255)) AS [tituloacao],
    CAST(TA.[TipoAcao] AS NVARCHAR(255)) AS [tipoacao],
    CAST(LOA.[produto] AS NVARCHAR(255)) AS [produto],
    CAST(LOA.[descricaoproduto] AS NVARCHAR(255)) AS [descricaoproduto],
    CAST(LOA.[unidademedida] AS NVARCHAR(255)) AS [unidademedida],
    CAST(LOA.[descricaounidademedida] AS NVARCHAR(255)) AS [descricaounidademedida],
    CAST(LOA.[localizador] AS NVARCHAR(255)) AS [localizador],
    CAST(LOA.[descricaolocalizador] AS NVARCHAR(255)) AS [descricaolocalizador],
    CAST(L.[uf] AS NVARCHAR(255)) AS [uf],
    CAST(L.[regiao] AS NVARCHAR(255)) AS [regiao],
    CAST(L.[estado] AS NVARCHAR(255)) AS [estado],
    CAST(LOA.[localizadorpreenchimentoobrigatorio] AS NVARCHAR(255)) AS [localizadorpreenchimentoobrigatorio],
    CAST(LOA.[elementosemcaptacao] AS NVARCHAR(255)) AS [elementosemcaptacao],
    CAST(LOA.[qtdemetaloa] AS FLOAT) AS [qtdemetaloa],
    CAST(NULL AS FLOAT) AS [projetolei],
    CAST(LOA.[dotacaoinicial] AS FLOAT) AS [dotacaoinicial],
    CAST(LOA.[dotacaoatual] AS FLOAT) AS [autorizado],
    CAST(LOA.[empenhado] AS FLOAT) AS [empenhado],
    CAST(LOA.[liquidado] AS FLOAT) AS [liquidado],
    CAST(LOA.[reprogramadofisico] AS FLOAT) AS [reprogramadofisico],
    CAST(LOA.[reprogramadofinanceiro] AS FLOAT) AS [reprogramadofinanceiro],
    CAST(LOA.[realizadoloa] AS FLOAT) AS [realizadoloa],
    CAST(LOA.[pago] AS FLOAT) AS [pago],
    CAST(LOA.[liquidadorap] AS FLOAT) AS [liquidadorap],
    CAST(LOA.[realizadorap] AS FLOAT) AS [realizadorap],
    CAST(LOA.[codigo_po] AS NVARCHAR(255)) AS [codigo_po],
    CAST(LOA.[titulo_po] AS NVARCHAR(255)) AS [titulo_po],
    CAST(LOA.[produto_po] AS NVARCHAR(255)) AS [produto_po],
    CAST(LOA.[descricaoproduto_po] AS NVARCHAR(255)) AS [descricaoproduto_po],
    CAST(LOA.[unidademedida_po] AS NVARCHAR(255)) AS [unidademedida_po],
    CAST(LOA.[descricaounidademedida_po] AS NVARCHAR(255)) AS [descricaounidademedida_po],
    CAST(LOA.[metaloaproposta_po] AS FLOAT) AS [metaloaproposta_po],
    CAST(LOA.[dotacaoinicial_po] AS FLOAT) AS [dotacaoinicial_po],
    CAST(NULL AS FLOAT) AS [autorizado_po],
    CAST(LOA.[empenhado_po] AS FLOAT) AS [empenhado_po],
    CAST(LOA.[liquidado_po] AS FLOAT) AS [liquidado_po],
    CAST(LOA.[realizado_po] AS FLOAT) AS [realizado_po],
    CAST(NULL AS FLOAT) AS [fisicoreprogramado_po],
    CAST(NULL AS FLOAT) AS [financeiroreprogramado_po],
    CAST(LOA.[pago_po] AS FLOAT) AS [pago_po],
    CAST(LOA.[liquidadorap_po] AS FLOAT) AS [liquidadorap_po],
    CAST(LOA.[qtdemetaatual_po] AS FLOAT) AS [qtdemetaatual_po], 
    CAST(LOA.[qtdemetaatual] AS FLOAT) AS [qtdemetaatual]
FROM
    [AcompanhamentoOrcamentario].[dbo].[_LOA_2018] LOA
    LEFT JOIN [AcompanhamentoOrcamentario].[dbo].[Localizador_UF_Regiao] L ON CAST(LOA.[descricaolocalizador] AS NVARCHAR(255)) = CAST(L.[descricaolocalizador] AS NVARCHAR(255))  
    LEFT JOIN [AcompanhamentoOrcamentario].[dbo].[TipoAcaoLoa] TA ON LEFT(CAST(LOA.[acao] AS NVARCHAR(255)), 1) = CAST(TA.[IDAcao] AS NVARCHAR(255))
    LEFT JOIN [AcompanhamentoOrcamentario].[dbo].[Tipo_Programa] TP ON CAST(LOA.[programa] AS NVARCHAR(255)) = CAST(TP.[programa] AS NVARCHAR(255))
    LEFT JOIN [AcompanhamentoOrcamentario].[dbo].[Descricao_Esfera] DE ON CAST(LOA.[esfera] AS NVARCHAR(255)) = CAST(DE.[esfera] AS NVARCHAR(255))
WHERE
    CAST(LOA.[descricaoorgao] AS NVARCHAR(255)) = CAST('Minist�rio da Agricultura, Pecu�ria e Abastecimento' AS NVARCHAR(255));