# -------------------------------------------------------------
# STEP 03 - Tabela descritiva das variaveis quantitativas
# Le a saida do STEP 01 e gera a tabela com:
# Variavel, Min., Max., Media, 1o quartil, Mediana, 3o quartil.
# Quantitativa = coluna que converte integralmente para numero.
# -------------------------------------------------------------
import pandas as pd

dados = pd.read_csv('output/base_step_01.csv', sep=';', decimal=',', encoding='utf-8-sig')

def como_numero(serie):
    return pd.to_numeric(serie.dropna().astype(str).str.replace(',', '.'), errors='coerce')

quantitativas = [c for c in dados.columns
                 if not dados[c].dropna().empty
                 and como_numero(dados[c]).notna().sum() == len(dados[c].dropna())]

linhas = []
for col in quantitativas:
    s = como_numero(dados[col])
    linhas.append({
        'Variavel': col,
        'Min.': s.min(),
        'Max.': s.max(),
        'Media': s.mean(),
        '1o quartil': s.quantile(0.25),
        'Mediana': s.median(),
        '3o quartil': s.quantile(0.75)
    })

tabela = pd.DataFrame(linhas, columns=['Variavel', 'Min.', 'Max.', 'Media',
                                       '1o quartil', 'Mediana', '3o quartil'])

# formatacao legivel: separador de milhar e 2 casas decimais
pd.options.display.float_format = lambda x: f'{x:,.2f}'

print(tabela.to_string(index=False))