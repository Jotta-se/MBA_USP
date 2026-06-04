# -------------------------------------------------------------
# STEP 05 IDH - Matriz de correlacao das features do modelo IDH
# Le a base com dummies do STEP 04, calcula a correlacao das 14
# features do modelo IDH, salva a matriz e sinaliza os pares com
# correlacao absoluta acima de 0,7 (criterio de multicolinearidade
# do TCC). Nao remove nada, apenas diagnostica.
# -------------------------------------------------------------
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('output/base_step_04.csv', sep=';', decimal=',', encoding='utf-8-sig')

# 14 features do modelo IDH
features_idh = [
    'Pago_USD',
    'PIB',
    'Log_Pop_Por_Propriedade',
    '%_Receber_Orientacao_Tecnica',
    'tipoacao_CAPEX',
    'regiao_BR',
    'regiao_Centro-Oeste',
    'regiao_Norte',
    'regiao_Sudeste',
    'regiao_Sul',
    'unidadeorcamentaria_EMBRAPA',
    'unidadeorcamentaria_INCRA',
    'unidadeorcamentaria_MAPA',
    'unidadeorcamentaria_SFB'
]

corr = df[features_idh].corr()

# salvar a matriz
corr.to_csv('output/base_step_05_corr_idh.csv', sep=';', encoding='utf-8-sig')

# sinalizar pares com correlacao absoluta acima de 0,7 (multicolinearidade)
LIMIAR = 0.7
pares_altos = []
for i in range(len(features_idh)):
    for j in range(i + 1, len(features_idh)):
        valor = corr.iloc[i, j]
        if abs(valor) > LIMIAR:
            pares_altos.append((features_idh[i], features_idh[j], round(valor, 3)))

print(f"Matriz de correlacao IDH ({len(features_idh)} features)")
if pares_altos:
    print(f"Pares com |correlacao| > {LIMIAR} (potencial multicolinearidade):")
    for a, b, v in pares_altos:
        print(f"  {a} x {b}: {v}")
else:
    print(f"Nenhum par com |correlacao| > {LIMIAR}.")

# plotar
plt.figure(figsize=(12, 10))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
plt.title('Matriz de Correlacao - Features do Modelo IDH')
plt.tight_layout()
plt.savefig('output/base_step_05_corr_idh.png', dpi=150)
plt.show()
plt.close()

print("Salvo em output/base_step_05_corr_idh.csv e output/base_step_05_corr_idh.png")