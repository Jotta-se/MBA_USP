# -------------------------------------------------------------
# STEP 09 PIB_AGRO - Modelo (XGBoost)
# Le a base com dummies do STEP 04, treina XGBoost para prever
# %_PIB_Agronegocio. Features definidas teoricamente (lista fixa,
# mesmo conjunto do modelo original). O RFE permanece no pipeline
# por consistencia de mecanica. Otimizacao via GridSearchCV.
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

ALVO = '%_PIB_Agronegocio'
N_FEATURES = 16
features = [
    'Pago_USD',
    'IDH',
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

colunas = features + [ALVO]
for c in colunas:
    df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.'), errors='coerce')
df = df.dropna(subset=colunas)

X = df[features]
y = df[ALVO]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

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

sel = X_train.columns[best.named_steps['rfe'].support_]
importancia = pd.DataFrame({
    'Feature': sel,
    'Importancia': best.named_steps['xgb'].feature_importances_
}).sort_values('Importancia', ascending=False).reset_index(drop=True)

print("\nIMPORTANCIA DAS FEATURES")
for _, r in importancia.iterrows():
    print(f"  {r['Feature']:<35}{r['Importancia']:.6f}")

importancia.to_csv('output/base_step_09_importancia_pibagro.csv', sep=';', index=False, encoding='utf-8-sig')
with open('output/modelo_pibagro_step_09.pkl', 'wb') as f:
    pickle.dump(best, f)

print("\nSalvo: output/modelo_pibagro_step_09.pkl, output/base_step_09_importancia_pibagro.csv")