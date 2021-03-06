# -*- coding: utf-8 -*-
"""Questão_1_Prova_2_IA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1E4RTtBKYKDDIvWHsYOSN71zdisghLVOc
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn as sn

from sklearn import preprocessing
from sklearn import utils
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_regression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import KNeighborsClassifier

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import Normalizer

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.decomposition import PCA

from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

import scipy.stats
from scipy.stats import norm
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn import metrics 
from mlxtend.plotting import plot_decision_regions
from sklearn.metrics import roc_auc_score, average_precision_score

# %matplotlib inline
# %pylab inline
plt.style.use('ggplot')

data = pd.read_csv("Churn_Modelling.csv")
data

"""Nessa etapa foram excluídos os atributos irrelevantes para a predição (numero da coluna, sobrenome e Id do cliente), além de realizar a transformação das variáveis categóricas em numéricas."""

# Exclusão dos atributos não utilizados

dataset = data.drop(['RowNumber', 'Surname', 'CustomerId'], axis=1) 

# Transformação de variáveis categóricas 

geography_transform = LabelEncoder()
dataset.iloc[:, 1] =geography_transform.fit_transform(dataset.iloc[:, 1])

gender_transform = LabelEncoder()
dataset.iloc[:, 2] =gender_transform.fit_transform(dataset.iloc[:, 2])

dataset

# Reescala de dados

normalized_dataset = MinMaxScaler().fit_transform(dataset)

"""Em seguida foi realizada a normalização dos dados (não binários), para que não houvessem fortes discrepâncias entre as colunas. """

#Adição de rotulos

dataset_normalize = pd.DataFrame(normalized_dataset, columns=['CreditScore','Geography','Gender','Age','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary', 'Exited']) 
dataset_normalize

"""Os dados da tabela foram divididos em "features" e "target", e foi criada uma nóva variável através do PCA, que calcula a projeção dos dados em algum vetor que maximize a variança dos dados e perca menor quantidade de informação possível. A nova variável foi denominada PC1."""

# Separação dos atributos

array_x = np.array(dataset_normalize.drop('Exited',1))
array_y = np.array(dataset_normalize['Exited'])

# Execução do PCA para 1

x = array_x
y = array_y

pca = PCA(n_components=1)
pca.fit(x)
print(pca.explained_variance_ratio_)
print(pca.singular_values_)

x_1 = pca.transform(x)
data_labels = pd.DataFrame(x_1, columns=['pc1'])

data_labels

dataset_concatenate = np.concatenate((array_x, data_labels), axis=1)

final_dataset = pd.DataFrame(dataset_concatenate, columns=['CreditScore','Geography','Gender','Age','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary', 'pc1']) 
final_dataset

final_y = pd.DataFrame(array_y, columns=['Exited']) 
final_y

"""Foi realizada uma análise de correlação entre as variáveis, assim como o plot de sua matriz. A matriz obtida mede o grau da correlação entre duas variáveis de escala métrica. Quanto maior for o valor absoluto do coeficiente, mais forte é a relação entre as variáveis. Como mostrado na matriz, quando um atributo é comparado com ele mesmo é indicado o valor absoluto 1, indicando uma relação linear perfeita entre as variáveis. Quando é indicado o valor 0, ou valores próximos a isso, é indicado que não há correlação entre os atributos verificados. Como observado na matriz obtida, a maioria das variáveis não apresenta correlação, porém há atributos que se correlacionam."""

# Análise de correlação

correlation = final_dataset.corr()
correlation

# Plot da matriz de correlação

try:
   plot = sn.heatmap(correlation, annot = True, fmt=".1f", linewidths=.6)
   plot
except ValueError:  
    pass

# Junção X e Y

concatenate_dataset_xY = np.concatenate((final_dataset, final_y), axis=1)

final_dataset_XY = pd.DataFrame(concatenate_dataset_xY, columns=['CreditScore','Geography','Gender','Age','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary', 'pc1', 'Exited']) 
final_dataset_XY

"""Como segunda nálise exploratória, foi realizada uma distribuição normal, relacionando a idade dos clientes ao seu estado no banco. Essa distribuição pode ser representada como uma curva em forma de sino, na qual a metade dos resultados cai acima da média e metade cai abaixo. Além disso, na distribuição normal a média = mediana = moda. Analisando os resultados obtidos, é visível que tanto a media de idade quanto o desvio padrão são relativamente semelhantes em ambos os casos, contudo são muito discrepantes entre si. Ademais, o fato do desvio padrão ser relativamente alto gera uma distorção na curva devido a variação, maior dispersão dos dados e outliers de forma que relacionar a saída do banco à idade não agrega muito."""

# Distribuição normal

saiu = final_dataset_XY[final_dataset_XY['Exited'] == 0]
nao_saiu =  final_dataset_XY[final_dataset_XY['Exited'] == 1]
#Idade conta fechada
idade_nao_saiu = nao_saiu.groupby(u'Age')['Exited'].value_counts()
#Idade conta aberta
idade_saiu = saiu.groupby(u'Age')['Exited'].value_counts()

print("Média - Saiu: ", np.mean(idade_saiu), "Desvio Padrão - Saiu: ", np.std(idade_saiu))
print("Média - Não Saiu: ", np.mean(idade_nao_saiu), "Desvio Padrão - Não Saiu: ", np.std(idade_nao_saiu))

pdf = scipy.stats.norm.pdf(idade_saiu, np.mean(idade_saiu), np.std(idade_saiu))
plt.plot(idade_saiu, pdf)

pdf2 = scipy.stats.norm.pdf(idade_nao_saiu, np.mean(idade_nao_saiu), np.std(idade_nao_saiu))
plt.plot(idade_nao_saiu, pdf2)

plt.legend(('Cliente deixou o banco', 'Cliente não deixou o banco'))
plt.show()

"""O primeiro modelo de classificação selecionado para a realização da previsão da base de dados foi o Algoritmo de Naive Bayes, que se baseia na probabilidade de cada evento ocorrer, desconsiderando a correlação entre "features". Esse modelo possui uma parte matemática relativamente simples, além de um bom desempenho, necessitando de poucas observações para ter uma boa acurácia. Através do modelo, foi possível prever que há a probabilidade de 20,58% dos clientes terem deixado o banco e 79,42% não terem deixado. Essa análise atingiu uma revocação de 96%, além de uma precisão superior a 80%, indicando a baixa ocorrência de falsos positivos."""

# Classificação - Naive Bayes

x_train, x_val, y_train, y_val = train_test_split(final_dataset, final_y, test_size=0.5, random_state=35)

gnb = GaussianNB()
used_features =['CreditScore','Geography','Gender','Age','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary', 'pc1']

gnb.fit(
    x_train[used_features].values,
    y_train["Exited"]
)
y_pred = gnb.predict(x_val[used_features])

mean_exited=np.mean(y_train["Exited"])
mean_not_exited=1-mean_exited
print("Probabilidade de ter deixado o banco = {:03.2f}%, Probabilidade de não ter deixado o banco = {:03.2f}%"
      .format(100*mean_exited,100*mean_not_exited))
print("\n")

#Acurácia, precisão e F1
y_pred = gnb.predict(x_val)
targ = ['class 0', 'class 1']
print(classification_report(y_val, y_pred, target_names=targ))
print("\n")

#Matriz de confusão
cm = confusion_matrix(y_val, y_train)
print("Matriz de confusão:")
print(cm)
print("\n")

"""O segundo modelo de classificação adotado foi a Árvore de Decisão, que utiliza um gráfico ou modelo de decisões e suas possíveis consequências, incluindo resultados de eventos acasos, custos de recursos e utilidade. Essa ferramenta cria nós que se ligam através de uma hierarquia, onde o nó mais valoroso é o nós raiz e os resultados apresentados são os nós folhas. O nó raiz é um dos atributos da base de dados e o nó folha é a classe ou valor que será gerado como resposta. Os atributos selecionados para essa análise foram a idade dos usuários, seu salário estimado, sua atividade no banco e a nova variável PC1. Para avaliar os resultados obtidos, foram utilizadas as métricas: Curva ROC e Precisão Média. A primeira mostra o quão bom o modelo criado pode distinguir entre duas coisas, que podem ser 0 ou 1, ou positivo e negativo. Para os hiperparâmetros adotados, o valor da Curva ROC excedeu os 60%, apresentando-se melhor nos primeiros hiperparâmetros adotados. Os valores obtidos para a precisão média, para todos os hiperparâmetros adotados, indica que pode haver a ocorrência de falsos positivos."""

# Classificação - Árvore de decisão (hiperparâmetro 1)

colunas = ['IsActiveMember','Age','EstimatedSalary', 'pc1', 'Exited']
simple_df = final_dataset_XY[colunas]
simple_df.head(2)

Y = simple_df['Exited']
X = simple_df.loc[:, 'IsActiveMember':'pc1']

x_train, x_val, y_train, y_val = train_test_split(X, Y, test_size=0.5, random_state=35)
x_train.shape, x_val.shape, y_train.shape, y_val.shape

y_train.value_counts()

model_dtree = DecisionTreeClassifier(max_depth = 22,
                              min_samples_split = 5,
                              min_samples_leaf = 10,
                              max_features = 2,
                              criterion = 'gini',
                              random_state = 35,
                              class_weight = 'balanced')



model_dtree.fit(x_train,y_train)

pred_dtree = model_dtree.predict(x_val)

print('Curva ROC:', np.round(roc_auc_score(y_val, pred_dtree),4))
print('Precisão Média:', np.round(average_precision_score(y_val, pred_dtree),4))
print("\n")

#Matriz de confusão
cm = confusion_matrix(y_val, y_train)
print("Matriz de confusão:")
print(cm)
print("\n")

# Classificação - Árvore de decisão (hiperparâmetro 2)

colunas = ['IsActiveMember','Age','EstimatedSalary', 'pc1', 'Exited']
simple_df = final_dataset_XY[colunas]
simple_df.head(2)

Y = simple_df['Exited']
X = simple_df.loc[:, 'IsActiveMember':'pc1']

x_train, x_val, y_train, y_val = train_test_split(X, Y, test_size=0.5, random_state=35)
x_train.shape, x_val.shape, y_train.shape, y_val.shape

y_train.value_counts()

model_dtree = DecisionTreeClassifier(max_depth = 20,
                              min_samples_split = 11,
                              min_samples_leaf = 5,
                              max_features = 1,
                              criterion = 'gini',
                              random_state = 35,
                              class_weight = 'balanced')



model_dtree.fit(x_train,y_train)

pred_dtree = model_dtree.predict(x_val)

print('Curva ROC:', np.round(roc_auc_score(y_val, pred_dtree),4))
print('Precisão Média:', np.round(average_precision_score(y_val, pred_dtree),4))
print("\n")

#Matriz de confusão
cm = confusion_matrix(y_val, y_train)
print("Matriz de confusão:")
print(cm)
print("\n")