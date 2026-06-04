# -------------------------------------------------------------
# STEP 08 PIB_AGRO - Matriz de correlacao das features do modelo PIB_Agro
# Le a base com dummies do STEP 04, calcula a correlacao das 16
# features do modelo PIB_Agro, salva a matriz e sinaliza os pares com
# correlacao absoluta acima de 0,7 (criterio de multicolinearidade
# do TCC). Nao remove nada, apenas diagnostica.
# -------------------------------------------------------------
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('output/base_step_04.csv', sep=';', decimal=',', encoding='utf-8-sig')

# 16 features do modelo PIB_Agro
features_pibagro = [
    'IDH',
    'Pago_USD',
    'PIB',
    'Log_Pop_Por_Propriedade',
    '%_Receber_Orientacao_Tecnica',
    'tipoacao_CAPEX',
    'regiao_BR',
    'regiao_Centro-Oeste',
    'regiao_Nordeste',
    'regiao_Norte',
    'regiao_Sudeste',
    'regiao_Sul',
    'unidadeorcamentaria_CONAB',
    'unidadeorcamentaria_EMBRAPA',
    'unidadeorcamentaria_INCRA',
    'unidadeorcamentaria_MAPA'
]

corr = df[features_pibagro].corr()

# salvar a matriz
corr.to_csv('output/base_step_08_corr_pibagro.csv', sep=';', encoding='utf-8-sig')

# sinalizar pares com correlacao absoluta acima de 0,7 (multicolinearidade)
LIMIAR = 0.7
pares_altos = []
for i in range(len(features_pibagro)):
    for j in range(i + 1, len(features_pibagro)):
        valor = corr.iloc[i, j]
        if abs(valor) > LIMIAR:
            pares_altos.append((features_pibagro[i], features_pibagro[j], round(valor, 3)))

print(f"Matriz de correlacao PIB_Agro ({len(features_pibagro)} features)")
if pares_altos:
    print(f"Pares com |correlacao| > {LIMIAR} (potencial multicolinearidade):")
    for a, b, v in pares_altos:
        print(f"  {a} x {b}: {v}")
else:
    print(f"Nenhum par com |correlacao| > {LIMIAR}.")

# plotar
plt.figure(figsize=(12, 10))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
plt.title('Matriz de Correlacao - Features do Modelo PIB_Agro')
plt.tight_layout()
plt.savefig('output/base_step_08_corr_pibagro.png', dpi=150)
plt.show()
plt.close()

print("Salvo em output/base_step_08_corr_pibagro.csv e output/base_step_08_corr_pibagro.png")