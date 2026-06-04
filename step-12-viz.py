# -------------------------------------------------------------
# STEP 12 VIZ - Grafico 3D interativo: IDH x Orientacao Tecnica x PIB_Agro
# Le a base do STEP 04, reconstroi a regiao a partir das dummies e
# plota a dispersao 3D interativa (rotacao nos tres eixos) com pontos
# coloridos por regiao. Salva HTML interativo e renderiza na celula.
# -------------------------------------------------------------
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('output/base_step_04.csv', sep=';', decimal=',', encoding='utf-8-sig')

for c in ['IDH', '%_Receber_Orientacao_Tecnica', '%_PIB_Agronegocio']:
    df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.'), errors='coerce')

regiao_cols = [c for c in df.columns if c.startswith('regiao_')]
df['regiao'] = df[regiao_cols].idxmax(axis=1).str.replace('regiao_', '', regex=False)

_palette = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3', '#937860']
categorias = sorted(df['regiao'].unique())
cores_hex = {cat: _palette[i % len(_palette)] for i, cat in enumerate(categorias)}

fig = go.Figure()
for cat in categorias:
    m = (df['regiao'] == cat).values
    fig.add_trace(go.Scatter3d(
        x=df['IDH'][m], y=df['%_Receber_Orientacao_Tecnica'][m], z=df['%_PIB_Agronegocio'][m],
        mode='markers', name=cat,
        marker=dict(size=4, color=cores_hex[cat], opacity=0.7)))

fig.update_layout(
    title='Dispersao 3D - IDH x Orientacao Tecnica x PIB Agro',
    template='plotly_white',
    scene=dict(xaxis_title='IDH', yaxis_title='% Receber Orientacao Tecnica',
               zaxis_title='% PIB Agronegocio'),
    legend=dict(title='Regiao'), height=750)

fig.write_html('output/base_step_12_3d_dispersao.html', include_plotlyjs='cdn')
fig.show()
print("Salvo em output/base_step_12_3d_dispersao.html")