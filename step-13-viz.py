# -------------------------------------------------------------
# STEP 13 VIZ - Grafico 3D interativo: superficie de resposta PIB_Agro
# Carrega o modelo do STEP 09 e plota como o %_PIB_Agronegocio previsto
# varia em funcao de %_Receber_Orientacao_Tecnica e IDH, com as demais
# features fixadas na media. Salva HTML interativo e renderiza na celula.
# -------------------------------------------------------------
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go

df = pd.read_csv('output/base_step_04.csv', sep=';', decimal=',', encoding='utf-8-sig')

with open('output/modelo_pibagro_step_09.pkl', 'rb') as f:
    modelo = pickle.load(f)

features = [
    'Pago_USD', 'IDH', 'PIB', 'Log_Pop_Por_Propriedade',
    '%_Receber_Orientacao_Tecnica', 'tipoacao_CAPEX', 'regiao_BR',
    'regiao_Centro-Oeste', 'regiao_Nordeste', 'regiao_Norte',
    'regiao_Sudeste', 'regiao_Sul', 'unidadeorcamentaria_CONAB',
    'unidadeorcamentaria_EMBRAPA', 'unidadeorcamentaria_INCRA',
    'unidadeorcamentaria_MAPA'
]
for c in features:
    df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.'), errors='coerce')

eixo_x = '%_Receber_Orientacao_Tecnica'
eixo_y = 'IDH'
gx = np.linspace(df[eixo_x].min(), df[eixo_x].max(), 30)
gy = np.linspace(df[eixo_y].min(), df[eixo_y].max(), 30)
GX, GY = np.meshgrid(gx, gy)

medias = df[features].mean()
grade = pd.DataFrame(np.tile(medias.values, (GX.size, 1)), columns=features)
grade[eixo_x] = GX.ravel()
grade[eixo_y] = GY.ravel()
Z = modelo.predict(grade).reshape(GX.shape)

fig = go.Figure(data=[go.Surface(x=GX, y=GY, z=Z, colorscale='Viridis')])
fig.update_layout(
    title='Superficie de Resposta do Modelo PIB_Agro (STEP 09)',
    template='plotly_white',
    scene=dict(xaxis_title='% Receber Orientacao Tecnica', yaxis_title='IDH',
               zaxis_title='% PIB Agronegocio previsto'), height=750)

fig.write_html('output/base_step_13_3d_superficie.html', include_plotlyjs='cdn')
fig.show()
print("Salvo em output/base_step_13_3d_superficie.html")