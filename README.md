<div align="center">

# 🌾 Execução Orçamentária do MAPA & Impacto Socioeconômico

### Trabalho de Conclusão de Curso — MBA Data Science & Analytics · USP/Esalq

**Modelagem preditiva com XGBoost para avaliar a relação entre a execução orçamentária
do Ministério da Agricultura e indicadores de desenvolvimento regional (IDH e PIB Agro)**

![Python](https://img.shields.io/badge/python-3.13-3776AB?logo=python&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-3.2-FF6F00?logo=xgboost&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.9-F7931E?logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-6.7-3F4F75?logo=plotly&logoColor=white)
![UV](https://img.shields.io/badge/uv-package%20manager-DE5FE9?logo=astral&logoColor=white)
![License](https://img.shields.io/badge/license-academic-lightgrey)

</div>

---

## 📑 Sumário

- [Visão Geral do Projeto](#-visão-geral-do-projeto)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Pré-requisitos](#-pré-requisitos)
- [Configuração do Ambiente com UV](#-configuração-do-ambiente-com-uv)
- [Execução do Pipeline (Scripts Python)](#-execução-do-pipeline-scripts-python)
- [Execução do Notebook (POC_01.ipynb)](#-execução-do-notebook-poc_01ipynb)
- [Descrição dos Steps](#-descrição-dos-steps)
- [Artefatos Gerados](#-artefatos-gerados)
- [Stack Tecnológica](#-stack-tecnológica)

---

## 🎯 Visão Geral do Projeto

Este projeto investiga **como a execução orçamentária do Ministério da Agricultura, Pecuária e Abastecimento (MAPA)** — incluindo órgãos vinculados como EMBRAPA, INCRA, CONAB e SFB — se relaciona com indicadores socioeconômicos municipais e regionais, especificamente:

| Modelo | Variável-Alvo | Features |
|--------|--------------|----------|
| **Modelo IDH** | Índice de Desenvolvimento Humano | 14 variáveis (investimento, PIB, pressão demográfica, assistência técnica, região e unidade orçamentária) |
| **Modelo PIB Agro** | % do PIB oriundo do Agronegócio | 16 variáveis (inclui IDH e amplia cobertura regional e institucional) |

O pipeline é composto por **14 etapas sequenciais** que cobrem desde a carga e auditoria dos dados brutos até a modelagem preditiva com **XGBoost** (otimizado via GridSearchCV) e a geração de visualizações estáticas e interativas 3D.

---

## 📁 Estrutura do Repositório

```
MBA_USP/
│
├── 📄 README.md                  ← Este arquivo
├── 📄 pyproject.toml             ← Configuração do projeto e dependências
├── 📄 .python-version            ← Versão do Python (3.13)
├── 📄 .gitignore                 ← Regras de exclusão do Git
├── 📄 uv.lock                   ← Lock de dependências (reprodutibilidade)
│
├── 📊 Base_Estudo_PIB_IDH.csv    ← Base de dados principal (entrada)
├── 📊 Base_TCC_USP.xlsx          ← Base auxiliar do TCC
├── 📦 acomp_orcamentario_*.zip   ← Dados brutos de acompanhamento orçamentário (2019–2023)
├── 📝 artigo_xgboost_mapa_pt.docx← Artigo acadêmico
│
├── 🔧 step-00.py                ← Orquestrador: executa steps 01→14 em sequência
├── 🔧 step-01.py                ← Carga e auditoria dos dados
├── 🔧 step-02.py                ← Estatística descritiva — variáveis qualitativas
├── 🔧 step-03.py                ← Estatística descritiva — variáveis quantitativas
├── 🔧 step-04.py                ← One-Hot Encoding das categóricas
├── 🔧 step-05-idh.py            ← Matriz de correlação (modelo IDH)
├── 🔧 step-06-idh.py            ← Modelo XGBoost — IDH (features fixas)
├── 🔧 step-07-idh.py            ← Modelo XGBoost — IDH (seleção automática)
├── 🔧 step-08-pib.py            ← Matriz de correlação (modelo PIB Agro)
├── 🔧 step-09-pib.py            ← Modelo XGBoost — PIB Agro
├── 🔧 step-10-viz.py            ← Visualizações de execução orçamentária
├── 🔧 step-11.py                ← Estatística descritiva ampliada
├── 🔧 step-12-viz.py            ← Dispersão 3D interativa (Plotly)
├── 🔧 step-13-viz.py            ← Superfície de resposta 3D (Plotly)
├── 🔧 step-14-viz.py            ← Heatmap de execução orçamentária
│
├── 📓 POC_01.ipynb               ← Notebook exploratório (versão completa)
├── 📓 extract_notebook_py.ipynb  ← Utilitário para extrair scripts do notebook
│
└── 📂 output/                    ← Todos os artefatos gerados (CSVs, PNGs, HTMLs, PKLs)
```

---

## ✅ Pré-requisitos

| Requisito | Versão Mínima | Verificação |
|-----------|--------------|-------------|
| **Python** | 3.13+ | `python --version` |
| **UV** (gerenciador de pacotes) | Qualquer versão recente | `uv --version` |
| **Git** | Qualquer versão recente | `git --version` |

> **💡 Nota:** O UV é um gerenciador de pacotes e ambientes Python ultrarrápido, escrito em Rust. Ele substitui `pip`, `venv`, `pip-tools` e `pyenv` em uma única ferramenta.

---

## 🔧 Configuração do Ambiente com UV

### 1. Instalar o UV

Caso ainda não tenha o UV instalado, execute **um** dos comandos abaixo:

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Após a instalação, **reinicie o terminal** e verifique:

```bash
uv --version
```

### 2. Clonar o Repositório

```bash
git clone https://github.com/Jotta-se/MBA_USP.git
cd MBA_USP
```

### 3. Criar o Ambiente Virtual e Instalar Dependências

O UV lê automaticamente o `pyproject.toml` e o `uv.lock` para garantir reprodutibilidade total:

```bash
uv sync
```

> Este comando:
> - Detecta a versão do Python necessária (3.13) a partir do `.python-version`
> - Cria o ambiente virtual em `.venv/` (se não existir)
> - Instala **todas** as dependências com versões exatas do `uv.lock`

### 4. Verificar a Instalação

```bash
uv run python -c "import xgboost, sklearn, plotly, pandas; print('✅ Ambiente pronto!')"
```

---

## 🚀 Execução do Pipeline (Scripts Python)

O pipeline completo é controlado pelo **orquestrador `step-00.py`**, que executa os 14 steps em sequência, com validação de pré-condições (verifica se os arquivos de entrada existem antes de cada etapa) e medição de tempo.

### Execução Completa (recomendado)

```bash
uv run python step-00.py
```

O orquestrador irá:

1. ✅ Validar se o arquivo de entrada de cada step existe e não está vazio
2. ▶️ Executar cada step sequencialmente (`step-01.py` → `step-14.py`)
3. ⏱️ Cronometrar cada etapa individualmente
4. 🛑 Interromper imediatamente se qualquer step falhar
5. 📊 Exibir o tempo total de execução ao final

**Saída esperada:**

```
Iniciando orquestração dos passos (STEP-01 ao STEP-14)...

==================================================
Iniciando step-01.py...
==================================================
   Originais  Aproveitados Aproveitamento (%)
0       2245          2245              100.0

[SUCESSO] step-01.py concluído em 0.42 segundos.

  (...demais steps...)

==================================================
Todos os scripts foram executados com sucesso!
Tempo total de execução: XXX.XX segundos.
==================================================
```

### Execução Individual

Para executar um step específico (ex: apenas o modelo IDH):

```bash
uv run python step-06-idh.py
```

> **⚠️ Atenção:** cada step depende dos artefatos gerados pelos steps anteriores. Respeite a ordem de dependência indicada na seção [Descrição dos Steps](#-descrição-dos-steps).

---

## 📓 Execução do Notebook (POC_01.ipynb)

O notebook `POC_01.ipynb` contém a **versão exploratória completa** do projeto, incluindo análises visuais inline, comentários explicativos e experimentações adicionais.

### 1. Registrar o Kernel do Ambiente UV

Para que o Jupyter reconheça o ambiente virtual criado pelo UV:

```bash
uv run python -m ipykernel install --user --name=mba-usp --display-name "Python (MBA USP)"
```

### 2. Abrir o Notebook

**Opção A — VS Code (recomendado):**

1. Abra o VS Code na pasta do projeto
2. Abra o arquivo `POC_01.ipynb`
3. No canto superior direito, clique em **"Select Kernel"**
4. Selecione **"Python (MBA USP)"** ou o interpretador em `.venv/`

**Opção B — Jupyter Lab:**

```bash
uv run jupyter lab
```

Em seguida, abra `POC_01.ipynb` no navegador e selecione o kernel **"Python (MBA USP)"**.

### 3. Executar

- **Todas as células:** `Ctrl+Shift+Enter` (VS Code) ou menu *Run → Run All Cells*
- **Célula a célula:** `Shift+Enter` para avançar uma de cada vez

> **💡 Dica:** O notebook e os scripts Python geram os mesmos artefatos na pasta `output/`. Você pode usar qualquer abordagem.

---

## 📋 Descrição dos Steps

| Step | Arquivo | Descrição | Entrada | Saída |
|------|---------|-----------|---------|-------|
| **00** | `step-00.py` | **Orquestrador** — executa steps 01→14 com validação e cronômetro | — | — |
| **01** | `step-01.py` | Carga do CSV bruto, auditoria de nulos, descarte de registros inválidos | `Base_Estudo_PIB_IDH.csv` | `output/base_step_01.csv` |
| **02** | `step-02.py` | Tabela descritiva das variáveis qualitativas (categorias, moda) | `output/base_step_01.csv` | _console_ |
| **03** | `step-03.py` | Tabela descritiva das variáveis quantitativas (min, max, média, quartis) | `output/base_step_01.csv` | _console_ |
| **04** | `step-04.py` | One-Hot Encoding de `tipoacao`, `regiao` e `unidadeorcamentaria` | `output/base_step_01.csv` | `output/base_step_04.csv` |
| **05** | `step-05-idh.py` | Matriz de correlação das 14 features do modelo IDH + diagnóstico de multicolinearidade (limiar \|r\| > 0,7) | `output/base_step_04.csv` | `output/base_step_05_corr_idh.csv` · `.png` |
| **06** | `step-06-idh.py` | **Modelo XGBoost → IDH** com features fixas (hypothesis-driven), pipeline StandardScaler → RFE → XGBoost, otimização GridSearchCV 5-fold | `output/base_step_04.csv` | `output/modelo_idh_step_06.pkl` · `base_step_06_importancia_idh.csv` |
| **07** | `step-07-idh.py` | **Modelo XGBoost → IDH** com seleção automática (poda de multicolinearidade + RFE) para comparação | `output/base_step_04.csv` | `output/modelo_idh_step_07.pkl` · `importancia_idh.csv` |
| **08** | `step-08-pib.py` | Matriz de correlação das 16 features do modelo PIB Agro | `output/base_step_04.csv` | `output/base_step_08_corr_pibagro.csv` · `.png` |
| **09** | `step-09-pib.py` | **Modelo XGBoost → %PIB Agro** com features fixas, mesma arquitetura do step 06 | `output/base_step_04.csv` | `output/modelo_pibagro_step_09.pkl` · `base_step_09_importancia_pibagro.csv` |
| **10** | `step-10-viz.py` | Análise visual de execução orçamentária: barras por ano, por região, gráfico de rosca BR, small multiples e escala log | `output/base_step_04.csv` | 5 gráficos `.png` + 2 tabelas `.csv` |
| **11** | `step-11.py` | Estatística descritiva ampliada: distribuição por região, unidade orçamentária e tipo de ação | `output/base_step_04.csv` | 3 tabelas `.csv` |
| **12** | `step-12-viz.py` | Dispersão 3D interativa (IDH × Orientação Técnica × PIB Agro) colorida por região | `output/base_step_04.csv` | `output/base_step_12_3d_dispersao.html` |
| **13** | `step-13-viz.py` | Superfície de resposta 3D do modelo PIB Agro (variando Orientação Técnica e IDH) | `output/base_step_04.csv` · `modelo_pibagro_step_09.pkl` | `output/base_step_13_3d_superficie.html` |
| **14** | `step-14-viz.py` | Heatmap estilizado de execução orçamentária (região × ano) com gradiente vermelho→verde | `output/base_step_04.csv` | `output/base_step_14_heatmap_execucao.png` |

### Grafo de Dependências

```
Base_Estudo_PIB_IDH.csv
        │
    [step-01] ── Carga & Limpeza
        │
        ├── [step-02] Descritiva qualitativa
        ├── [step-03] Descritiva quantitativa
        │
    [step-04] ── One-Hot Encoding
        │
        ├── [step-05]  Correlação IDH
        ├── [step-06]  Modelo IDH (fixo)
        ├── [step-07]  Modelo IDH (automático)
        ├── [step-08]  Correlação PIB Agro
        ├── [step-09]  Modelo PIB Agro ──────┐
        ├── [step-10]  Visualizações Orçam.  │
        ├── [step-11]  Descritiva Ampliada   │
        ├── [step-12]  Dispersão 3D          │
        ├── [step-13]  Superfície 3D ◄───────┘ (usa modelo do step-09)
        └── [step-14]  Heatmap Execução
```

---

## 📦 Artefatos Gerados

Todos os artefatos são salvos na pasta `output/`:

| Tipo | Arquivos | Descrição |
|------|----------|-----------|
| 📊 **Dados intermediários** | `base_step_01.csv`, `base_step_04.csv` | Bases limpas e com encoding |
| 📈 **Correlações** | `base_step_05_corr_idh.*`, `base_step_08_corr_pibagro.*` | Matrizes de correlação (CSV + heatmap PNG) |
| 🤖 **Modelos treinados** | `modelo_idh_step_06.pkl`, `modelo_idh_step_07.pkl`, `modelo_pibagro_step_09.pkl` | Pipelines XGBoost serializados com pickle |
| 🏆 **Importância** | `base_step_06_importancia_idh.csv`, `importancia_idh.csv`, `base_step_09_importancia_pibagro.csv` | Rankings de feature importance |
| 📊 **Visualizações estáticas** | `base_step_10_*.png`, `base_step_14_*.png` | Gráficos de execução orçamentária e heatmap |
| 🌐 **Visualizações interativas** | `base_step_12_3d_dispersao.html`, `base_step_13_3d_superficie.html` | Gráficos 3D Plotly (abrir no navegador) |
| 📋 **Tabelas descritivas** | `base_step_11_descritiva_*.csv`, `base_step_10_execucao_*.csv` | Resumos estatísticos por recorte |

---

## 🛠️ Stack Tecnológica

| Componente | Tecnologia | Finalidade |
|------------|-----------|------------|
| Linguagem | **Python 3.13** | Desenvolvimento completo |
| Gerenciador de Pacotes | **UV** | Ambientes virtuais e dependências |
| Machine Learning | **XGBoost** + **scikit-learn** | Regressão preditiva, RFE, GridSearchCV, StandardScaler |
| Manipulação de Dados | **Pandas** + **NumPy** | ETL, transformações e estatísticas |
| Visualizações Estáticas | **Matplotlib** + **Seaborn** | Gráficos de barras, heatmaps, rosca |
| Visualizações Interativas | **Plotly** | Dispersão 3D e superfície de resposta |
| Notebook | **Jupyter / IPyKernel** | Exploração interativa |
| Serialização | **Pickle** | Persistência dos modelos treinados |

---

<div align="center">

**MBA Data Science & Analytics — USP/Esalq**

Desenvolvido como parte do Trabalho de Conclusão de Curso <br>
[![ORCID](https://img.shields.io/badge/ORCID-0000--0003--0612--4576-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0000-0003-0612-4576)

</div>
