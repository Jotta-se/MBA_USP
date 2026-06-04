# -------------------------------------------------------------
# STEP 06 IDH - Modelo (XGBoost)
# Le a base com dummies do STEP 04, treina XGBoost para prever IDH.
# As features sao definidas teoricamente (lista fixa). O RFE permanece
# no pipeline por consistencia de mecanica, mas nao reduz o conjunto.
# Otimizacao de hiperparametros via GridSearchCV.
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

# Fonte correta: a base com dummies do STEP 04, nao a matriz de correlacao
df = pd.read_csv('output/base_step_04.csv', sep=';', decimal=',', encoding='utf-8-sig')

# -------------------------------------------------------------
# Selecao teorica das 14 features (hypothesis-driven), nao automatica.
# Cada variavel tem um fundamento de negocio para estar no modelo (deliberado por consenso).
#   - capacidade de investimento: Pago_USD, tipoacao_CAPEX
#   - riqueza regional: PIB
#   - pressao demografica sobre a terra: Log_Pop_Por_Propriedade
#   - acesso a assistencia tecnica: %_Receber_Orientacao_Tecnica
#   - controles estruturais: blocos de regiao e unidade orcamentaria
# Conjunto fixo garante interpretabilidade e comparabilidade entre os
# modelos do pipeline (coeficientes e importancias estaveis e lado a lado).
# Evita a correlacao espuria que a selecao automatica costuma gerar,
# tratando ruido como se fosse poder explicativo.
# -------------------------------------------------------------

ALVO = 'IDH'
N_FEATURES = 14
features = [
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

# Garante tipo numerico nas colunas usadas (o CSV vem com virgula decimal,
# entao colunas com texto residual poderiam ficar como object)
colunas = features + [ALVO]
for c in colunas:
    df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.'), errors='coerce')
df = df.dropna(subset=colunas)

X = df[features]
y = df[ALVO]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# pipeline: normalizacao -> selecao RFE -> XGBoost
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('rfe', RFE(LinearRegression(), n_features_to_select=N_FEATURES, step=1)),
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

print("=" * 55)
print(f"MODELO {ALVO} - DESEMPENHO")
print("=" * 55)
print(f"R2 Score : {r2:.18f}")
print(f"RMSE     : {rmse:.18f}")
print(f"MAE      : {mae:.18f}")
print(f"MSE      : {mse:.18e}")
hp = {k.replace('xgb__', ''): v for k, v in grid_search.best_params_.items()}
print(f"Hiperparametros: {hp}")

# --- importancia das features (resultado secundario) ---
sel = X_train.columns[best.named_steps['rfe'].support_]
importancia = pd.DataFrame({
    'Feature': sel,
    'Importancia': best.named_steps['xgb'].feature_importances_
}).sort_values('Importancia', ascending=False).reset_index(drop=True)

print("\nIMPORTANCIA DAS FEATURES")
for _, r in importancia.iterrows():
    print(f"  {r['Feature']:<35}{r['Importancia']:.6f}")

# --- persistencia ---
importancia.to_csv('output/base_step_06_importancia_idh.csv', sep=';', index=False, encoding='utf-8-sig')
with open('output/modelo_idh_step_06.pkl', 'wb') as f:
    pickle.dump(best, f)

print("\nSalvo: output/modelo_idh_step_06.pkl, output/base_step_06_importancia_idh.csv")