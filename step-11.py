# -------------------------------------------------------------
# STEP 11 - Estatistica descritiva ampliada
# Le a base do STEP 04, reconstroi regiao, unidade orcamentaria e
# tipo de acao a partir das dummies e gera tabelas com numero de
# registros, soma autorizada e paga em bilhoes, participacao no total
# e taxa de execucao. Salva uma tabela por recorte em output/.
# -------------------------------------------------------------
import pandas as pd

df = pd.read_csv('output/base_step_04.csv', sep=';', decimal=',', encoding='utf-8-sig')

df['Autorizado'] = pd.to_numeric(df['Autorizado'].astype(str).str.replace(',', '.'), errors='coerce')
df['Pago'] = pd.to_numeric(df['Pago'].astype(str).str.replace(',', '.'), errors='coerce')

# reconstruir as categoricas a partir das dummies do STEP 04
regiao_cols = [c for c in df.columns if c.startswith('regiao_')]
df['regiao'] = df[regiao_cols].idxmax(axis=1).str.replace('regiao_', '', regex=False)

unidade_cols = [c for c in df.columns if c.startswith('unidadeorcamentaria_')]
df['unidadeorcamentaria'] = df[unidade_cols].idxmax(axis=1).str.replace('unidadeorcamentaria_', '', regex=False)

tipoacao_cols = [c for c in df.columns if c.startswith('tipoacao_')]
df['tipoacao'] = df[tipoacao_cols].idxmax(axis=1).str.replace('tipoacao_', '', regex=False)

total_autorizado = df['Autorizado'].sum()

# --- distribuicao por regiao ---
tab_regiao = df.groupby('regiao').agg(Registros=('Autorizado', 'size'),
                                      Autorizado=('Autorizado', 'sum'),
                                      Pago=('Pago', 'sum'))
tab_regiao['Autorizado_bi'] = tab_regiao['Autorizado'] / 1e9
tab_regiao['Pago_bi'] = tab_regiao['Pago'] / 1e9
tab_regiao['Participacao_%'] = tab_regiao['Autorizado'] / total_autorizado * 100
tab_regiao['Execucao_%'] = tab_regiao['Pago'] / tab_regiao['Autorizado'] * 100
tab_regiao = tab_regiao[['Registros', 'Autorizado_bi', 'Pago_bi', 'Participacao_%', 'Execucao_%']].sort_values('Autorizado_bi', ascending=False).round(2)
tab_regiao.to_csv('output/base_step_11_descritiva_regiao.csv', sep=';', encoding='utf-8-sig')

# --- distribuicao por unidade orcamentaria ---
tab_unidade = df.groupby('unidadeorcamentaria').agg(Registros=('Autorizado', 'size'),
                                                    Autorizado=('Autorizado', 'sum'),
                                                    Pago=('Pago', 'sum'))
tab_unidade['Autorizado_bi'] = tab_unidade['Autorizado'] / 1e9
tab_unidade['Pago_bi'] = tab_unidade['Pago'] / 1e9
tab_unidade['Participacao_%'] = tab_unidade['Autorizado'] / total_autorizado * 100
tab_unidade['Execucao_%'] = tab_unidade['Pago'] / tab_unidade['Autorizado'] * 100
tab_unidade = tab_unidade[['Registros', 'Autorizado_bi', 'Pago_bi', 'Participacao_%', 'Execucao_%']].sort_values('Autorizado_bi', ascending=False).round(2)
tab_unidade.to_csv('output/base_step_11_descritiva_unidadeorcamentaria.csv', sep=';', encoding='utf-8-sig')

# --- distribuicao por tipo de acao ---
tab_tipoacao = df.groupby('tipoacao').agg(Registros=('Autorizado', 'size'),
                                          Autorizado=('Autorizado', 'sum'),
                                          Pago=('Pago', 'sum'))
tab_tipoacao['Autorizado_bi'] = tab_tipoacao['Autorizado'] / 1e9
tab_tipoacao['Pago_bi'] = tab_tipoacao['Pago'] / 1e9
tab_tipoacao['Participacao_%'] = tab_tipoacao['Autorizado'] / total_autorizado * 100
tab_tipoacao['Execucao_%'] = tab_tipoacao['Pago'] / tab_tipoacao['Autorizado'] * 100
tab_tipoacao = tab_tipoacao[['Registros', 'Autorizado_bi', 'Pago_bi', 'Participacao_%', 'Execucao_%']].sort_values('Autorizado_bi', ascending=False).round(2)
tab_tipoacao.to_csv('output/base_step_11_descritiva_tipoacao.csv', sep=';', encoding='utf-8-sig')

print("DISTRIBUICAO POR REGIAO")
print(tab_regiao.to_string())
print("\nDISTRIBUICAO POR UNIDADE ORCAMENTARIA")
print(tab_unidade.to_string())
print("\nDISTRIBUICAO POR TIPO DE ACAO")
print(tab_tipoacao.to_string())

print("\nSalvo em output/base_step_11_descritiva_regiao.csv, base_step_11_unidadeorcamentaria.csv e base_step_11_tipoacao.csv")