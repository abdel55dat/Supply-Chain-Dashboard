import pandas as pd
from src.clean_data import load_data, clean_data

df = load_data("data/raw/regularite-mensuelle-tgv-aqst.csv")
df = clean_data(df)

print("=== SHAPE ===")
print(df.shape)

print("\n=== VALEURS MANQUANTES ===")
print(df.isnull().sum())

print("\n=== TYPES DES COLONNES ===")
print(df.dtypes)

print("\n=== STATISTIQUES DE BASE ===")
print(df.describe())

print("\n=== DOUBLONS ===")
print(f"Nombre de doublons : {df.duplicated().sum()}")

print("\n=== APERÇU DES DONNÉES ===")
print(df.head(10))