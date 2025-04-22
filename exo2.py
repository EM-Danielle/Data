import pandas as pd

df = pd.read_csv('sales_data_sample.csv', encoding='latin1')
print(df.head())
print("Nombre de lignes et colonnes : ", df.shape)

# Identification des valeurs aberrantes avec la méthode IQR

Q1 = df['PRICEEACH'].quantile(0.25)
Q3 = df['PRICEEACH'].quantile(0.75)
IQR = Q3 - Q1
b_inf = Q1 - 1.5*IQR
b_sup = Q3 + 1.5*IQR
print("Borne inférieure : ", b_inf)
print("Borne supérieure : ", b_sup)

valeurs_aberrantes = df[(df['PRICEEACH']<b_inf)|(df['PRICEEACH']>b_sup)]
print("Valeurs aberrantes :\n", valeurs_aberrantes['PRICEEACH'])
print("Nombre de valeurs aberrantes :", len(valeurs_aberrantes))

# suppression des valeurs aberrantes
df_clean = df[(df['PRICEEACH']>=b_inf)&(df['PRICEEACH']<=b_sup)]
print( df_clean.shape)

df_clean.to_csv('sales_data_clean.csv', index=True)