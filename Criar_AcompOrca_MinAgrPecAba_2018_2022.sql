SELECT *
INTO [dbo].[_AcompOrca_MinAgrPecAba_USP]
FROM (
    SELECT *
    FROM [dbo].[_AcompOrca_MinAgrPecAba_2018]

    UNION ALL

    SELECT *
    FROM [dbo].[_AcompOrca_MinAgrPecAba_2019]

    UNION ALL

    SELECT *
    FROM [dbo].[_AcompOrca_MinAgrPecAba_2020]

    UNION ALL

    SELECT *
    FROM [dbo].[_AcompOrca_MinAgrPecAba_2021]

    UNION ALL

    SELECT *
    FROM [dbo].[_AcompOrca_MinAgrPecAba_2022]
) AS SourceTables;