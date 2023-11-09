# -*- coding: utf-8 -*-
"""train.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wOvZpRYAO1_dDLBujwWmUS1yCFEGQZzZ

# **Cultura e Práticas em DataOps e MLOps**
**Autor**: Renan Santos Mendes

**Email**: renansantosmendes@gmail.com

**Descrição**: Este notebook apresenta um exemplo de uma rede neural profunda com mais de uma camada para um problema de classificação.


# **Saúde Fetal**

As Cardiotocografias (CTGs) são opções simples e de baixo custo para avaliar a saúde fetal, permitindo que os profissionais de saúde atuem na prevenção da mortalidade infantil e materna. O próprio equipamento funciona enviando pulsos de ultrassom e lendo sua resposta, lançando luz sobre a frequência cardíaca fetal (FCF), movimentos fetais, contrações uterinas e muito mais.

Este conjunto de dados contém 2126 registros de características extraídas de exames de Cardiotocografias, que foram então classificados por três obstetras especialistas em 3 classes:

- Normal
- Suspeito
- Patológico

# Instalando pacotes
"""

"""# 1 - Importando os módulos necessários"""


import os
import random
import numpy as np
import random as python_random
import tensorflow
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, InputLayer
from keras.utils import to_categorical

import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

"""# Definindo funções adicionais"""

def reset_seeds():
   os.environ['PYTHONHASHSEED']=str(42)
   tf.random.set_seed(42)
   np.random.seed(42)
   random.seed(42)

"""# 2 - Fazendo a leitura do dataset e atribuindo às respectivas variáveis"""

data = pd.read_csv('https://raw.githubusercontent.com/renansantosmendes/lectures-cdas-2023/master/fetal_health_reduced.csv')

"""# Dando uma leve olhada nos dados"""

data.head()

"""# 3 - Preparando o dado antes de iniciar o treino do modelo"""

X=data.drop(["fetal_health"], axis=1)
y=data["fetal_health"]

columns_names = list(X.columns)
scaler = preprocessing.StandardScaler()
X_df = scaler.fit_transform(X)
X_df = pd.DataFrame(X_df, columns=columns_names)

X_train, X_test, y_train, y_test = train_test_split(X_df,
                                                    y,
                                                    test_size=0.3,
                                                    random_state=42)

y_train = y_train -1
y_test = y_test - 1

"""# 4 - Criando o modelo e adicionando as camadas"""

reset_seeds()
model = Sequential()
model.add(InputLayer(input_shape=(X_train.shape[1], )))
model.add(Dense(10, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(3, activation='softmax'))

"""# 5 - Compilando o modelo

"""

model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

import mlflow

MLFLOW_TRACKING_URI = 'https://dagshub.com/renansantosmendes/mlops-puc-o4.mlflow'
MLFLOW_TRACKING_USERNAME = 'renansantosmendes'
MLFLOW_TRACKING_PASSWORD = 'aa92514300daf70112ef5ac798ee86b9c8c5857e'
os.environ['MLFLOW_TRACKING_USERNAME'] = MLFLOW_TRACKING_USERNAME
os.environ['MLFLOW_TRACKING_PASSWORD'] = MLFLOW_TRACKING_PASSWORD

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

mlflow.tensorflow.autolog(log_models=True,
                          log_input_examples=True,
                          log_model_signatures=True)

"""# 6 - Executando o treino do modelo"""

with mlflow.start_run(run_name='experiment_01') as run:
    model.fit(X_train,
            y_train,
            epochs=70,
            validation_split=0.2,
            verbose=3)