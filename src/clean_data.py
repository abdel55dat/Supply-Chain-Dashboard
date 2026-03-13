import pandas as pd

def load_data(filepath=None):
    url = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/regularite-mensuelle-tgv-aqst/exports/csv?delimiter=%3B&lang=fr&timezone=Europe%2FParis"
    df = pd.read_csv(url, sep=";")
    return df

def clean_data(df):
    # Renommer les colonnes
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Colonnes commentaires à exclure de l'analyse
    comment_cols = [col for col in df.columns if "commentaire" in col]
    df = df.drop(columns=comment_cols)

    # Supprimer les doublons
    df = df.drop_duplicates()

    # Convertir la date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m")

    # Convertir les colonnes numériques
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    return df

if __name__ == "__main__":
    df = load_data("data/raw/regularite-mensuelle-tgv-aqst.csv")
    df = clean_data(df)
    print(df.head())
    print(f"\nShape : {df.shape}")
    print(f"\nColonnes : {df.columns.tolist()}")