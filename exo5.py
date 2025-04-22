#EXO5 : Traitement complet des donnees aberrantes , manquantes, doublons 

import pandas as pd

df = pd.read_csv("imdb_top_1000.csv")
print(df.head())
print(df.shape)

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

df["Gross"] = df["Gross"].str.replace(",", "").astype(float)
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
    valeurs_aberantes = df[(df[col]<b_inf)|(df[col]>b_sup)]
    if len(valeurs_aberantes) > 0:
        print("valeurs aberrantes :\n", valeurs_aberantes[col])
        #suppression de la ligne contenant la(les) valeur(s) aberante(s)
        df = df[(df[col] >= b_inf) & (df[col] <= b_sup)]
    else:
        print("pas de valeurs aberrantes")  
          
    print("\n")
print( df.shape)

#detection des valeurs abérantes  pour toutes les colonnes categorielle
#exclusion des colonnes nons pertinentes pour la detection des valeurs aberrantes categorielles(cotient des valeurs uniques)

colonnes_exclues = ['Poster_Link', 'Overview', 'Series_Title', 'Director', 'Star1', 'Star2', 'Star3', 'Star4']

def detecter_valeurs_aberrantes_categorielle(df, colonnes_categorielle, colonnes_exclues, seuil=0.01):
    for col in colonnes_categorielle:
        if col not in colonnes_exclues:
            total = len(df)
            freq = df[col].value_counts(normalize=True)
            rares = freq[freq < seuil]
            if not rares.empty:
                print(f"\nValeurs rares dans '{col}' (fréquence < {seuil*100:.0f}%) :")
                print(rares)

detecter_valeurs_aberrantes_categorielle(df, colonnes_categorielle, colonnes_exclues)
df = df[df['Released_Year'] != 'PG']

            
#sauvegarde du dataset nettoyé
df.to_csv("imdb_top_1000_clean.csv", index=True)
