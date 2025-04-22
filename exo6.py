import pandas as pd
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('creditcard_2023.csv')
print(df.head())
# Sélectionner les colonnes numériques
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
print("Colonnes numériques : ", numerical_columns)

# L'échelle d'une variable est l'intervalle dans lequel ses valeurs se situent. Par exemple, si les valeurs vont de 0 à 1000, l'échelle est grande. Si elles vont de 0 à 1, l'échelle est plus petite.

#Normaliser les données permet de les ramener dans une échelle commune, ce qui aide à éviter que certaines variables dominent le modèle à cause de leurs valeurs plus grandes.

# Initialiser le MinMaxScaler
scaler = MinMaxScaler()
# Appliquer la normalisation Min-Max sur les colonnes numériques
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

# Afficher le DataFrame après normalisation
print(df.head())