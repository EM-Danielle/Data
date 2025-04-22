import pandas as pd

df = pd.read_csv('marketing_campaign.csv',sep='\t')
print(df.head())

#recherche des doublons

doublons = df.duplicated()
print("les doublons:\n", doublons)
print("le nombre de doublons:", doublons.sum())

#suppression des doublons

df = df.drop_duplicates()

df.to_csv('marketing_campaign_clean.csv', index=True)
