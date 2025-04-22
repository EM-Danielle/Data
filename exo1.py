import pandas as pd

#EXERCICE 1

#chargement du dataset

df = pd.read_csv("WineQT.csv")
print(df.head())

#nombre de valeurs manquantes

missing = df.isnull().sum()
print("les valeurs manquantes par colonnes:\n", missing)
missing_total = (missing>0).sum()
print("le nombre de colonne possedant au moins une valeur manquante est donc:", missing_total)

#Suppression des lignes avec plus de 30% de valeurs manquantes
missing_pourcenatge = df.isnull().mean(axis=1) #calcul de la moyenne des valeurs manquantes(Nan=true) par ligne
df = df[missing_pourcenatge <= 0.3]

# Imputation des valeurs manquantes restantes avec la moyenne

df = df.fillna(df.mean(numeric_only=True))
print(df.head(30))

#sauvegarde du dataset nettoyé
df.to_csv("WineQT_clean.csv", index=False)
