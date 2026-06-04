# -------------------------------------------------------------
# STEP 04 - Encoding categorico completo
# Le a base limpa do STEP 01, aplica one-hot em tipoacao, regiao e
# unidadeorcamentaria, e salva a base preparada com todas as dummies.
# Nao filtra features aqui. Cada o modelo seleciona as suas
# nos steps seguintes, pois usam conjuntos diferentes.
# -------------------------------------------------------------
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

dados = pd.read_csv('output/base_step_01.csv', sep=';', decimal=',', encoding='utf-8-sig')

# one-hot encoding dos atributos categoricos
categoricas = ['tipoacao', 'regiao', 'unidadeorcamentaria']  # Selecao realizada por decisao de negocio
encoder = OneHotEncoder(sparse_output=False)
encoded_data = encoder.fit_transform(dados[categoricas])
encoded_columns = encoder.get_feature_names_out(categoricas)
df_encoded = pd.DataFrame(encoded_data, columns=encoded_columns, index=dados.index)

df = pd.concat([dados, df_encoded], axis=1)
df = df.drop(columns=categoricas)

df.to_csv('output/base_step_04.csv', sep=';', index=False, encoding='utf-8-sig')

print(f"Base preparada: {df.shape[0]} linhas, {df.shape[1]} colunas")
print(f"Dummies geradas ({len(encoded_columns)}):")
for c in encoded_columns:
    print(f"  {c}")
print("Salvo em output/base_step_04.csv")