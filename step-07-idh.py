# -------------------------------------------------------------
# STEP 07 IDH - Modelo (XGBoost) com selecao automatica de features
# Le a base com dummies do STEP 04 e preve IDH.
#
# Selecao em duas camadas, ambas sem vazamento:
#   1. Poda de multicolinearidade (|corr| > 0.7) calculada SO no treino.
#      Entre dois features colineares, remove o mais redundante
#      (maior correlacao media com os demais).
#   2. RFE dentro do Pipeline, com o numero de features varrido pelo
#      GridSearchCV. A validacao cruzada escolhe quantas features e
#      quais hiperparametros, reescalando dentro de cada fold.
#
# Resultado principal: R2 e metricas de erro.
# Resultado secundario: features sobreviventes e importancia.
# -------------------------------------------------------------
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from xgboost import XGBRegressor

df = pd.read_csv('output/base_step_04.csv', sep=';', decimal=',', encoding='utf-8-sig')

ALVO = 'IDH'
# colunas que nunca entram como feature (identificadores e nao numericas)
EXCLUIR = [ALVO, 'exerciciofiscal', 'uf', 'subfuncao']
LIMIAR_CORR = 0.7

# candidatas = tudo menos alvo e excluidas, convertidas pra numero
candidatas = [c for c in df.columns if c not in EXCLUIR]
for c in candidatas + [ALVO]:
    df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.'), errors='coerce')

# descarta candidatas que nao viraram numero de fato (viraram tudo NaN)
candidatas = [c for c in candidatas if df[c].notna().any()]
df = df.dropna(subset=candidatas + [ALVO])

X = df[candidatas]
y = df[ALVO]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# --- Camada 1: poda de multicolinearidade, so no treino ---
def podar_colineares(X_tr, limiar):
    corr = X_tr.corr().abs()
    descartadas = []
    cols = list(X_tr.columns)
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            a, b = cols[i], cols[j]
            if a in descartadas or b in descartadas:
                continue
            if corr.loc[a, b] > limiar:
                # remove o mais redundante: maior correlacao media com os demais
                red_a = corr[a].drop(a).mean()
                red_b = corr[b].drop(b).mean()
                descartadas.append(a if red_a >= red_b else b)
    mantidas = [c for c in cols if c not in descartadas]
    return mantidas, descartadas


mantidas, descartadas = podar_colineares(X_train, LIMIAR_CORR)
X_train = X_train[mantidas]
X_test = X_test[mantidas]

print("=" * 55)
print(f"SELECAO DE FEATURES - ALVO {ALVO}")
print("=" * 55)
print(f"Candidatas iniciais : {len(candidatas)}")
print(f"Podadas por |corr|>{LIMIAR_CORR} : {len(descartadas)}")
for d in descartadas:
    print(f"  - {d}")
print(f"Apos poda           : {len(mantidas)}")


# --- Camada 2: RFE seleciona quais 14 features manter ---
# Alvo de 14 features. Se a poda deixou menos que isso, o RFE usa o que tem.
N_FEATURES = 14
n_disp = len(mantidas)
n_rfe = min(N_FEATURES, n_disp)

pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('rfe', RFE(LinearRegression(), n_features_to_select=n_rfe, step=1)),
    ('xgb', XGBRegressor(random_state=42))
])

param_grid = {
    'xgb__n_estimators': [100, 200, 300],
    'xgb__max_depth': [3, 5, 7],
    'xgb__learning_rate': [0.01, 0.1, 0.2],
    'xgb__reg_alpha': [0, 0.1, 0.5],
    'xgb__reg_lambda': [0, 0.1, 0.5]
}

grid_search = GridSearchCV(pipe, param_grid, scoring='neg_mean_squared_error', cv=5)
grid_search.fit(X_train, y_train)
best = grid_search.best_estimator_

# --- avaliacao (resultado principal) ---
y_pred = best.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n" + "=" * 55)
print(f"MODELO {ALVO} - DESEMPENHO")
print("=" * 55)
print(f"R2 Score : {r2:.18f}")
print(f"RMSE     : {rmse:.18f}")
print(f"MAE      : {mae:.18f}")
print(f"MSE      : {mse:.18e}")
hp = {k.replace('xgb__', ''): v for k, v in grid_search.best_params_.items()}
print(f"Features RFE: {n_rfe} (de {n_disp} apos poda)")
print(f"Hiperparametros: {hp}")

# --- importancia das features selecionadas (resultado secundario) ---
sel = X_train.columns[best.named_steps['rfe'].support_]
importancia = pd.DataFrame({
    'Feature': sel,
    'Importancia': best.named_steps['xgb'].feature_importances_
}).sort_values('Importancia', ascending=False).reset_index(drop=True)

print(f"\nIMPORTANCIA DAS FEATURES (RFE manteve {len(sel)} de {len(mantidas)})")
for _, r in importancia.iterrows():
    print(f"  {r['Feature']:<35}{r['Importancia']:.6f}")

# --- persistencia ---
importancia.to_csv('output/importancia_idh.csv', sep=';', index=False, encoding='utf-8-sig')
with open('output/modelo_idh_step_07.pkl', 'wb') as f:
    pickle.dump(best, f)

print("\nSalvo: output/modelo_idh_step_07.pkl, output/importancia_idh.csv")