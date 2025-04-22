import pandas as pd

df = pd.read_csv('diabetes.csv')
print(df.head())

missing = df.isnull().sum()
print("les valeurs manquantes par colonnes:\n", missing)
df = df.fillna(df.median(numeric_only=True))
df.to_csv('diabetes_clean.csv', index=True)
#pas de colonne(s) categorielle(s)
