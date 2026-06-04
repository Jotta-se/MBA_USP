# -------------------------------------------------------------
# STEP 01 - Carga e auditoria das transacoes cruas
# Carga da base, auditoria de nulos e descarte de registros invalidos.
# -------------------------------------------------------------
import pandas as pd
import numpy as np
import os

INPUT_FILE = 'Base_Estudo_PIB_IDH.csv'
os.makedirs('output', exist_ok=True)

df = pd.read_csv(INPUT_FILE, sep=';', decimal=',')

# total antes de limpar
total_original = len(df)

# normaliza strings de nulo para NaN para o dropna agir de fato
df.replace(to_replace=["null", "NULL", ""], value=np.nan, inplace=True)
dados = df.dropna()

# aproveitamento real
total_aproveitados = len(dados)
aproveitamento = (total_aproveitados / total_original) * 100

resultados_df = pd.DataFrame({
    "Originais": [total_original],
    "Aproveitados": [total_aproveitados],
    "Aproveitamento (%)": [f"{aproveitamento:.1f}"]
})

print(resultados_df)

dados.to_csv('output/base_step_01.csv', sep=';', index=False, encoding='utf-8-sig')