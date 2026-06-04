# -------------------------------------------------------------
# STEP 02 - Tabela descritiva das variaveis qualitativas
# Le a saida do STEP 01 e gera a tabela: Variavel, Categorias, Moda.
# Qualitativa = coluna que nao converte para numero em nenhum valor.
# -------------------------------------------------------------
import pandas as pd

dados = pd.read_csv('output/base_step_01.csv', sep=';', decimal=',', encoding='utf-8-sig')

def eh_qualitativa(serie):
    numerico = pd.to_numeric(serie.dropna().astype(str).str.replace(',', '.'), errors='coerce')
    return numerico.notna().sum() == 0

qualitativas = [c for c in dados.columns if eh_qualitativa(dados[c])]

linhas = []
for col in qualitativas:
    categorias = ', '.join(sorted(dados[col].dropna().unique().astype(str)))
    moda = dados[col].mode().iloc[0]
    linhas.append({'Variavel': col, 'Categorias': categorias, 'Moda': moda})

tabela = pd.DataFrame(linhas, columns=['Variavel', 'Categorias', 'Moda'])

print(tabela.to_string(index=False))