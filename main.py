import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Binarizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data.csv")
print(df.head())
print(df.shape)
print(df.dtypes)


#recherche des doublons

doublons = df.duplicated()
print("\n les doublons:\n", doublons)
print("le nombre de doublons:", doublons.sum())

#suppression des doublons

df = df.drop_duplicates()
#nombre de valeurs manquantes

missing = df.isnull().sum()
print("\n les valeurs manquantes par colonnes:\n", missing)
missing_total = (missing>0).sum()
print("le nombre de colonne possedant au moins une valeur manquante est donc:", missing_total)
print("\n")

#Suppression des lignes avec plus de 50% de valeurs manquantes
missing_pourcenatge = df.isnull().mean(axis=1) #calcul de la moyenne des valeurs manquantes(Nan=true) par ligne
df = df[missing_pourcenatge <= 0.5]

# Imputation des valeurs numeriques manquantes restantes avec la moyenne

df = df.fillna(df.mean(numeric_only=True))

# Imputation des valeurs categorielles manquantes  restantes avec le mode

colonnes_categorielle = df.select_dtypes(include='object').columns

for col in colonnes_categorielle:
    mode = df[col].mode()[0]  # Le mode est une série, donc on prend [0]
    df[col] = df[col].fillna(mode)
    
#detection des valeurs abérantes  pour toutes les colonnes numeriques

aberrantes = df.select_dtypes(include='number').columns
print("il y'a ", len(aberrantes), "colonnes numeriques dans le dataset")
for col in aberrantes:
    print("pour la colonne",col)
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    b_inf = Q1 - 1.5 * IQR
    b_sup = Q3 + 1.5 * IQR
    print("Borne inférieure : ", b_inf)
    print("Borne supérieure : ", b_sup)
    valeurs_aberantes = df[(df[col]<b_inf)|(df[col]>b_sup)|(df[col]<=0)]
    if len(valeurs_aberantes) > 0:
        print("valeurs aberrantes :\n", valeurs_aberantes[col])
        #suppression de la ligne contenant la(les) valeur(s) aberante(s)
        df = df[(df[col] >= b_inf) & (df[col] <= b_sup)]
    else:
        print("pas de valeurs aberrantes")  
          
    print("\n")    
    
#valeurs abérantes pour la colonne genre

df['genre'] = df['genre'].apply( lambda x: 'homme' if x in ['HOMME'] else x)
df = df[~df['genre'].isin(['inconnu', 'other'])]
valeurs = df['genre'].value_counts()
print(valeurs)

data = df.copy()
data = data.drop(columns=['nom'])
# Calcul de la matrice de corrélation
correlation_matrix = data.corr(numeric_only=True)

# Affichage de la heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Matrice de corrélation')
#plt.show()

#standardisation âge et revenu:

scaler = StandardScaler()
scaler = StandardScaler() 
data[['revenu', 'age']]=scaler.fit_transform(data[['revenu', 'age']])
print(data.head())


#encodage d'achat et genre:
encoder = LabelEncoder()
data['genre'] = encoder.fit_transform(data['genre'])
data['achat'] = encoder.fit_transform(data['achat'])
print(data.head())

#encodage de profession:
# One-hot encoding
data = pd.get_dummies(data, columns=['profession'], drop_first=False)
print(data.head())
data.to_csv("data-clean.csv", index=True)

#binarisation de revenu:

# binarizer = Binarizer(threshold=3000)
# data['revenu_binaire'] = binarizer.fit_transform(data[['revenu']])

