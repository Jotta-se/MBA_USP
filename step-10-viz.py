# -------------------------------------------------------------
# STEP 10 VIZ - Analise de execucao orcamentaria
# Le a base do STEP 04 e calcula a taxa de execucao (Pago/Autorizado)
# por ano fiscal e por regiao. A taxa e sempre soma(Pago)/soma(Autorizado)
# do recorte, nao media de razoes linha a linha (linhas com Autorizado
# zero distorceriam a media). Salva as tabelas e plota a evolucao.
# Inclui Alt 1 (small multiples por regiao) e Alt 3 (barras log).
# -------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np

df = pd.read_csv('output/base_step_04.csv', sep=';', decimal=',', encoding='utf-8-sig')
for c in ['Autorizado', 'Pago']:
    df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.'), errors='coerce')

regiao_cols = [c for c in df.columns if c.startswith('regiao_')]
df['regiao'] = df[regiao_cols].idxmax(axis=1).str.replace('regiao_', '', regex=False)

def taxa(grupo):
    aut = grupo['Autorizado'].sum()
    pago = grupo['Pago'].sum()
    return pd.Series({
        'Autorizado_bi': aut / 1e9,
        'Pago_bi': pago / 1e9,
        'Execucao_%': (pago / aut * 100) if aut > 0 else 0
    })

por_ano = df.groupby('exerciciofiscal').apply(taxa, include_groups=False).round(2)
por_ano.to_csv('output/base_step_10_execucao_ano.csv', sep=';', encoding='utf-8-sig')

por_regiao = df.groupby('regiao').apply(taxa, include_groups=False).round(2)
por_regiao = por_regiao.sort_values('Execucao_%', ascending=False)
por_regiao.to_csv('output/base_step_10_execucao_regiao.csv', sep=';', encoding='utf-8-sig')

print("=" * 55)
print("EXECUCAO ORCAMENTARIA POR ANO FISCAL")
print("=" * 55)
print(por_ano.to_string())
print("\n" + "=" * 55)
print("EXECUCAO ORCAMENTARIA POR REGIAO")
print("=" * 55)
print(por_regiao.to_string())

HATCHES     = ['////', 'xxxx']
COR_HACHURA = '#5B9BD5'
GRID_COLOR  = '#D9D9D9'
TITLE_COLOR = '#404040'
TABLE_FS    = 8.5
BW          = 0.35

def estilo_eixo(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID_COLOR)
    ax.spines['bottom'].set_color(GRID_COLOR)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_facecolor('white')

def montar_tabela(ax, col_labels, row_data):
    tbl = ax.table(
        cellText=row_data,
        rowLabels=['Autorizado', 'Pago', 'Execucao %'],
        colLabels=col_labels,
        cellLoc='center', rowLoc='center',
        bbox=[0, -0.30, 1, 0.22]
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(TABLE_FS)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor(GRID_COLOR)
        cell.set_linewidth(0.6)
        if r == 0:
            cell.set_facecolor('#D6E4F0')
            cell.set_text_props(color=TITLE_COLOR, fontweight='bold')
        elif c == -1:
            cell.set_facecolor('#F2F2F2')
            cell.set_text_props(color=TITLE_COLOR)
        else:
            cell.set_facecolor('white')

leg_patches = [
    mpatches.Patch(facecolor='white', hatch=HATCHES[0],
                   edgecolor=COR_HACHURA, label='Autorizado'),
    mpatches.Patch(facecolor='white', hatch=HATCHES[1],
                   edgecolor=COR_HACHURA, label='Pago'),
]
leg_line = Line2D([0], [0], color='#404040', marker='o', linewidth=2, label='Execucao (%)')

# =============================================================
# GRAFICO 1: taxa de execucao por ANO FISCAL
# =============================================================
anos = por_ano.index.astype(str).tolist()
x = np.arange(len(por_ano))

fig, ax1 = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor('white')
estilo_eixo(ax1)

ax1.bar(x - BW/2, por_ano['Autorizado_bi'], BW,
        facecolor='white', hatch=HATCHES[0],
        edgecolor=COR_HACHURA, linewidth=0.8, zorder=3)
ax1.bar(x + BW/2, por_ano['Pago_bi'], BW,
        facecolor='white', hatch=HATCHES[1],
        edgecolor=COR_HACHURA, linewidth=0.8, zorder=3)

ax1.set_xticks(x)
ax1.set_xticklabels(anos, fontsize=10, color=TITLE_COLOR)
ax1.set_ylabel('Valores em R$ (Bilhoes)', fontsize=10, color=TITLE_COLOR)
ax1.tick_params(axis='y', colors=TITLE_COLOR)

ax2 = ax1.twinx()
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_color(GRID_COLOR)
ax2.plot(x, por_ano['Execucao_%'], color=TITLE_COLOR,
         marker='o', linewidth=2, markersize=6, zorder=4)
ax2.set_ylabel('Taxa de Execucao (%)', fontsize=10, color=TITLE_COLOR)
ax2.set_ylim(0, 110)
ax2.tick_params(axis='y', colors=TITLE_COLOR)

ax1.legend(handles=leg_patches + [leg_line], loc='upper left', frameon=False, fontsize=9)
plt.title('Execucao Orcamentaria por Ano Fiscal (2018-2022)',
          fontsize=13, color=TITLE_COLOR, fontweight='normal', pad=14)

plt.subplots_adjust(bottom=0.22)
montar_tabela(ax1, anos, [
    [f"{v:.2f}" for v in por_ano['Autorizado_bi']],
    [f"{v:.2f}" for v in por_ano['Pago_bi']],
    [f"{v:.1f}%" for v in por_ano['Execucao_%']],
])

plt.savefig('output/base_step_10_execucao_ano.png', dpi=150, bbox_inches='tight')
plt.show()
plt.close()

# =============================================================
# GRAFICO 2: taxa de execucao por REGIAO (sem BR)
# =============================================================
por_regiao_sem_br = por_regiao[por_regiao.index != 'BR']
regioes = por_regiao_sem_br.index.astype(str).tolist()
x2 = np.arange(len(por_regiao_sem_br))

fig, ax1 = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor('white')
estilo_eixo(ax1)

ax1.bar(x2 - BW/2, por_regiao_sem_br['Autorizado_bi'], BW,
        facecolor='white', hatch=HATCHES[0],
        edgecolor=COR_HACHURA, linewidth=0.8, zorder=3)
ax1.bar(x2 + BW/2, por_regiao_sem_br['Pago_bi'], BW,
        facecolor='white', hatch=HATCHES[1],
        edgecolor=COR_HACHURA, linewidth=0.8, zorder=3)

ax1.set_xticks(x2)
ax1.set_xticklabels(regioes, rotation=0, ha='right', fontsize=10, color=TITLE_COLOR)
ax1.set_ylabel('Valores em R$ (Bilhoes)', fontsize=10, color=TITLE_COLOR)
ax1.tick_params(axis='y', colors=TITLE_COLOR)

ax2 = ax1.twinx()
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_color(GRID_COLOR)
ax2.plot(x2, por_regiao_sem_br['Execucao_%'], color=TITLE_COLOR,
         marker='o', linewidth=2, markersize=6, zorder=4)
ax2.set_ylabel('Taxa de Execucao (%)', fontsize=10, color=TITLE_COLOR)
ax2.set_ylim(0, 110)
ax2.tick_params(axis='y', colors=TITLE_COLOR)

ax1.legend(handles=leg_patches + [leg_line], loc='upper right', frameon=False, fontsize=9)
plt.title('Execucao Orcamentaria por Regiao (sem BR)',
          fontsize=13, color=TITLE_COLOR, fontweight='normal', pad=14)

plt.subplots_adjust(bottom=0.22)
montar_tabela(ax1, regioes, [
    [f"{v:.2f}" for v in por_regiao_sem_br['Autorizado_bi']],
    [f"{v:.2f}" for v in por_regiao_sem_br['Pago_bi']],
    [f"{v:.1f}%" for v in por_regiao_sem_br['Execucao_%']],
])

plt.savefig('output/base_step_10_execucao_regiao.png', dpi=150, bbox_inches='tight')
plt.show()
plt.close()

# =============================================================
# GRAFICO 3: rosca BR — Autorizado vs Pago
# =============================================================
br = por_regiao.loc['BR']
valores = [br['Pago_bi'], br['Autorizado_bi'] - br['Pago_bi']]
rotulos = [
    f"Pago\nR$ {br['Pago_bi']:.1f} bi\n{valores[0]/sum(valores)*100:.1f}%",
    f"Nao Executado\nR$ {(br['Autorizado_bi'] - br['Pago_bi']):.1f} bi\n{valores[1]/sum(valores)*100:.1f}%"
]
cores = ['#90CAF9', '#CFD8DC']

fig, ax = plt.subplots(figsize=(7, 7))
fig.patch.set_facecolor('white')
wedges, texts = ax.pie(
    valores,
    labels=rotulos,
    colors=cores,
    startangle=90,
    wedgeprops=dict(width=0.5),
    textprops=dict(fontsize=12)
)

ax.set_title(
    f"BR — Execucao Orcamentaria\n"
    f"Autorizado: R$ {br['Autorizado_bi']:.1f} bi  |  Execucao: {br['Execucao_%']:.1f}%",
    fontsize=13, fontweight='normal', color=TITLE_COLOR
)
plt.tight_layout()
plt.savefig('output/base_step_10_execucao_br_rosca.png', dpi=150, bbox_inches='tight')
plt.show()
plt.close()

# =============================================================
# GRAFICO 4: Small multiples - um painel de barras por regiao
# =============================================================
aut  = df.pivot_table(index='regiao', columns='exerciciofiscal',
                      values='Autorizado', aggfunc='sum', fill_value=0) / 1e9
pago = df.pivot_table(index='regiao', columns='exerciciofiscal',
                      values='Pago',        aggfunc='sum', fill_value=0) / 1e9

regioes_alt1 = list(aut.index)
anos_alt1    = list(aut.columns)
x_alt1       = np.arange(len(anos_alt1))

ncols = 3
nrows = int(np.ceil(len(regioes_alt1) / ncols))
fig, axes = plt.subplots(nrows, ncols, figsize=(16, 5 * nrows))
fig.patch.set_facecolor('white')
axes = axes.ravel()

for k, reg in enumerate(regioes_alt1):
    ax = axes[k]
    estilo_eixo(ax)
    ax.bar(x_alt1 - BW/2, aut.loc[reg], BW,
           facecolor='white', hatch=HATCHES[0],
           edgecolor=COR_HACHURA, linewidth=0.8, zorder=3)
    ax.bar(x_alt1 + BW/2, pago.loc[reg], BW,
           facecolor='white', hatch=HATCHES[1],
           edgecolor=COR_HACHURA, linewidth=0.8, zorder=3)
    ax.set_xlabel(reg, fontsize=12, fontweight='bold', color=TITLE_COLOR, labelpad=8)
    ax.set_xticks(x_alt1)
    ax.set_xticklabels([str(a) for a in anos_alt1], fontsize=8, color=TITLE_COLOR)
    ax.set_ylabel('R$ Bilhoes', fontsize=9, color=TITLE_COLOR)
    ax.tick_params(axis='y', colors=TITLE_COLOR)
    if k == 0:
        ax.legend(handles=leg_patches, frameon=False, fontsize=8,
                  loc='upper left')

for k in range(len(regioes_alt1), len(axes)):
    axes[k].axis('off')

plt.suptitle('Autorizado x Pago por Regiao e Ano (escala propria por painel)',
             fontsize=14, color=TITLE_COLOR, fontweight='normal', y=1.01)
plt.tight_layout()
plt.savefig('output/base_step_10_small_multiples.png', dpi=150,
            bbox_inches='tight', facecolor='white')
plt.show()
plt.close()

# =============================================================
# GRAFICO 5: Barras agrupadas 2D com eixo Y logaritmico
# =============================================================
resumo  = df.groupby('regiao')[['Autorizado', 'Pago']].sum() / 1e9
resumo  = resumo.sort_values('Autorizado', ascending=False)
regioes_alt3 = list(resumo.index)
x_alt3       = np.arange(len(regioes_alt3))

fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor('white')
estilo_eixo(ax)
ax.yaxis.grid(False)
ax.set_yscale('log')
ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8, zorder=0, which='both')

ax.bar(x_alt3 - BW/2, resumo['Autorizado'], BW,
       facecolor='white', hatch=HATCHES[0],
       edgecolor=COR_HACHURA, linewidth=0.8, zorder=3)
ax.bar(x_alt3 + BW/2, resumo['Pago'], BW,
       facecolor='white', hatch=HATCHES[1],
       edgecolor=COR_HACHURA, linewidth=0.8, zorder=3)

ax.set_xticks(x_alt3)
ax.set_xticklabels(regioes_alt3, fontsize=10, color=TITLE_COLOR)
ax.set_xlabel('Regiao', fontsize=10, color=TITLE_COLOR)
ax.set_ylabel('R$ Bilhoes (escala log)', fontsize=10, color=TITLE_COLOR)
ax.tick_params(axis='both', colors=TITLE_COLOR)

for i, reg in enumerate(regioes_alt3):
    val_aut  = resumo['Autorizado'].iloc[i]
    val_pago = resumo['Pago'].iloc[i]
    ax.text(i - BW/2, val_aut  * 1.08, f"{val_aut:.2f}",
            ha='center', va='bottom', fontsize=8, color=TITLE_COLOR)
    ax.text(i + BW/2, val_pago * 1.08, f"{val_pago:.2f}",
            ha='center', va='bottom', fontsize=8, color=TITLE_COLOR)

ax.legend(handles=leg_patches, frameon=False, fontsize=9, loc='upper right')
plt.title('Autorizado x Pago por Regiao — total 2018-2022 (eixo Y log)',
          fontsize=13, color=TITLE_COLOR, fontweight='normal', pad=14)
plt.tight_layout()
plt.savefig('output/base_step_10_barras_log_2d.png', dpi=150,
            bbox_inches='tight', facecolor='white')
plt.show()
plt.close()

print("\nSalvo: output/base_step_10_execucao_ano.csv,base_step_10_regiao.csv, "
      "base_step_10_execucao_ano.png, base_step_10_execucao_regiao.png, base_step_10_execucao_br_rosca.png, "
      "base_step_10_small_multiples.png, base_step_10_barras_log_2d.png")