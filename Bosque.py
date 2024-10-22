from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, mean_squared_error, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.tree import export_text

from imblearn.over_sampling import RandomOverSampler

import statsmodels.api as sm
import seaborn as sns

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("")#insertar dataset

columns_to_scale = ['Promedionoches', 'EDAD']

# Escalador 
scaler = RobustScaler()
scaled_columns = scaler.fit_transform(df[columns_to_scale])
scaled_df = pd.DataFrame(scaled_columns, columns=columns_to_scale)
result_df = pd.concat([scaled_df, df.drop(columns=columns_to_scale)], axis=1)

X = result_df.drop(columns=['Porcenta', 'Ulceras'])
Y = result_df['Ulceras']

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=45)

# Sobremuestreo
ros = RandomOverSampler(sampling_strategy=0.3, random_state=45)
X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)
print("Distribución de clases después del sobremuestreo aleatorio:")
print(y_train_resampled.value_counts())

#Encontrar hiperparametros
reg = RandomForestClassifier()

from sklearn.model_selection import GridSearchCV

parameters = {"criterion": ("gini",),
              "max_depth": (10,11), "random_state":(42,43),
              "n_estimators": (141,143), "max_features":(0.1,0.2),
              }
rejilla = GridSearchCV(reg,parameters,scoring="r2")

rejilla.fit(X_train_resampled, y_train_resampled)
sorted(rejilla.cv_results_.keys())

print(rejilla.best_score_)
print(rejilla.best_params_)

#Entrenar el mejor arbol, con los hiperparametros escogidos y hacer predicciones
mejor_bosque = rejilla.best_estimator_
y_pred = mejor_bosque.predict(X_test)

#Desempeño del modelo
print(classification_report(y_test, y_pred))

# Matriz de confusión
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=mejor_bosque.classes_)
disp.plot(cmap=plt.cm.Blues)
plt.title('Matriz de Confusión')
plt.show()

#obtener caracteristicas de un arbol
tree = mejor_bosque.estimators_[0]
tree_rules = export_text(tree,feature_names=['EDAD','ECV',"SOLO_BRADEN_MALTA",'OBESIDAD2','Promedionoches'])
print(tree_rules)
