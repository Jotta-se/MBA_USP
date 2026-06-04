# -------------------------------------------------------------
# STEP 14 VIZ - Heatmap de execucao orcamentaria (regiao x ano)
# Estilo: celulas arredondadas, tag de status, gradiente RdYlGn,
# texto adaptativo (claro/escuro), colorbar horizontal inferior.
# -------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import rcParams

# ── Fonte e estilo base ───────────────────────────────────────
rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams.update({'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.spines.left': False, 'axes.spines.bottom': False})

# ── Dados ─────────────────────────────────────────────────────
df = pd.read_csv('output/base_step_04.csv', sep=';', decimal=',', encoding='utf-8-sig')
df['Autorizado'] = pd.to_numeric(df['Autorizado'].astype(str).str.replace(',', '.'), errors='coerce')
df['Pago']       = pd.to_numeric(df['Pago'].astype(str).str.replace(',', '.'), errors='coerce')

regiao_cols = [c for c in df.columns if c.startswith('regiao_')]
df['regiao']  = df[regiao_cols].idxmax(axis=1).str.replace('regiao_', '', regex=False)

aut   = df.pivot_table(index='regiao', columns='exerciciofiscal', values='Autorizado', aggfunc='sum', fill_value=0)
pago  = df.pivot_table(index='regiao', columns='exerciciofiscal', values='Pago',       aggfunc='sum', fill_value=0)
execucao = (pago / aut.replace(0, np.nan) * 100)

regioes = list(execucao.index)
anos    = list(execucao.columns)
Z       = execucao.values
n_reg, n_ano = len(regioes), len(anos)

# ── Colormap customizado (espelha o gradiente do HTML) ────────
colors_custom = [
    (0.00, '#8B1a1a'),
    (0.10, '#cc3300'),
    (0.20, '#e85a00'),
    (0.30, '#f0a000'),
    (0.45, '#e8d44d'),
    (0.55, '#a8cc50'),
    (0.70, '#4a9040'),
    (1.00, '#1e6428'),
]
from matplotlib.colors import to_rgb
cmap_custom = LinearSegmentedColormap.from_list(
    'execucao',
    [(p, to_rgb(c)) for p, c in colors_custom]
)
norm = plt.Normalize(vmin=0, vmax=100)

# ── Helper: tag de status ─────────────────────────────────────
def status_tag(v):
    if np.isnan(v): return '— N/D'
    if v >= 40: return 'Alta'
    if v >= 15: return 'Media'
    if v >=  5: return 'Baixa'
    return 'Critica'

def status_emoji(v):
    if np.isnan(v): return '○'
    if v >= 40: return '●'   # verde
    if v >= 15: return '●'   # amarelo
    if v >=  5: return '●'   # laranja
    return '●'               # vermelho

# ── Helper: luminância → cor do texto ────────────────────────
def text_color(rgba):
    r, g, b = rgba[:3]
    lum = 0.299*r*255 + 0.587*g*255 + 0.114*b*255
    return '#1a1a1a' if lum > 120 else '#f5f5f5'

# ── Figura ────────────────────────────────────────────────────
CELL_W  = 1.0          # unidade de largura por coluna
CELL_H  = 0.85         # unidade de altura por linha
PAD     = 0.08         # gap entre células (em unidades de dados)
RADIUS  = 0.12         # raio do arredondamento (FancyBboxPatch)

fig_w = n_ano  * (CELL_W + PAD) + 1.6   # 1.6 para rótulos das regiões
fig_h = n_reg  * (CELL_H + PAD) + 1.8   # 1.8 para título + colorbar

fig, ax = plt.subplots(figsize=(fig_w, fig_h))
ax.set_xlim(-0.5, n_ano  * (CELL_W + PAD) - PAD + 0.5)
ax.set_ylim(-0.5, n_reg  * (CELL_H + PAD) - PAD + 0.5)
ax.set_aspect('equal')
ax.axis('off')

fig.patch.set_facecolor('#f8f9fa')
ax.set_facecolor('#f8f9fa')

# ── Desenha células ───────────────────────────────────────────
for i, reg in enumerate(regioes):
    row = n_reg - 1 - i          # inverte: primeira região no topo
    y0  = row * (CELL_H + PAD)

    # rótulo da região (à esquerda)
    ax.text(-0.35, y0 + CELL_H/2, reg,
            ha='right', va='center', fontsize=10, fontweight='500',
            color='#555555')

    for j, ano in enumerate(anos):
        x0 = j * (CELL_W + PAD)
        v  = Z[i, j]

        rgba = cmap_custom(norm(v) if not np.isnan(v) else 0.5)
        fg   = text_color(rgba)

        # célula arredondada
        fancy = mpatches.FancyBboxPatch(
            (x0, y0), CELL_W, CELL_H,
            boxstyle=f"round,pad=0,rounding_size={RADIUS}",
            linewidth=0,
            facecolor=rgba,
            zorder=2
        )
        ax.add_patch(fancy)

        # percentual (grande, centro-topo)
        txt_pct = f'{v:.0f}%' if not np.isnan(v) else 'N/D'
        ax.text(x0 + CELL_W/2, y0 + CELL_H*0.58, txt_pct,
                ha='center', va='center', fontsize=13, fontweight='600',
                color=fg, zorder=3)

        # tag de status (menor, centro-baixo)
        ax.text(x0 + CELL_W/2, y0 + CELL_H*0.22, status_tag(v),
                ha='center', va='center', fontsize=8, fontweight='400',
                color=fg, alpha=0.88, zorder=3)

# ── Cabeçalho dos anos ────────────────────────────────────────
for j, ano in enumerate(anos):
    x0 = j * (CELL_W + PAD)
    ax.text(x0 + CELL_W/2,
            n_reg * (CELL_H + PAD) - PAD + 0.18,
            str(ano),
            ha='center', va='bottom', fontsize=10, fontweight='500',
            color='#555555')

# ── Título ────────────────────────────────────────────────────
fig.text(0.5, 0.97,
         'Taxa de Execução Orçamentária  —  Região × Ano Fiscal',
         ha='center', va='top', fontsize=13, fontweight='600',
         color='#1a1a1a')
fig.text(0.5, 0.93,
         'Pago ÷ Autorizado × 100   |   cor: vermelho (0%) → verde (100%)',
         ha='center', va='top', fontsize=9, color='#777777')

# ── Colorbar horizontal (embaixo) ────────────────────────────
cax = fig.add_axes([0.18, 0.04, 0.64, 0.022])
sm  = plt.cm.ScalarMappable(cmap=cmap_custom, norm=norm)
sm.set_array([])
cb  = fig.colorbar(sm, cax=cax, orientation='horizontal')
cb.set_label('Execução (%)', fontsize=9, color='#555555', labelpad=4)
cb.set_ticks([0, 25, 50, 75, 100])
cb.ax.tick_params(labelsize=8, color='#aaaaaa')
for spine in cb.ax.spines.values():
    spine.set_visible(False)

plt.subplots_adjust(left=0.14, right=0.97, top=0.91, bottom=0.12)
plt.savefig('output/base_step_14_heatmap_execucao.png',
            dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
plt.show()
print("Salvo em output/base_step_14_heatmap_execucao.png")