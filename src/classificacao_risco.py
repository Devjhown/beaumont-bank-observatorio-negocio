import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler

import os

CAMINHO_LOAN = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'loan.asc')
loan = pd.read_csv(CAMINHO_LOAN, sep=';')

y = loan['status']
x = loan.drop('status', axis=1)

x_treino, x_teste, y_treino, y_teste = train_test_split(
    x, y, stratify=y, random_state=5
)

arvore = DecisionTreeClassifier(random_state=5, max_depth=5)
arvore.fit(x_treino, y_treino)

print("Árvore - Treino:", arvore.score(x_treino, y_treino))
print("Árvore - Teste:", arvore.score(x_teste, y_teste))

scaler = MinMaxScaler()
x_treino_norm = scaler.fit_transform(x_treino)
x_teste_norm = scaler.transform(x_teste)

knn = KNeighborsClassifier()
knn.fit(x_treino_norm, y_treino)
print("KNN - Teste:", knn.score(x_teste_norm, y_teste))

CAMINHO_MODELO = os.path.join(os.path.dirname(__file__), '..', 'models', 'modelo_arvore.pkl')
with open(CAMINHO_MODELO, 'wb') as arquivo:
    pickle.dump(arvore, arquivo)