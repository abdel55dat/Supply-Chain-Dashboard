# Supply Chain Dashboard — Ponctualité TGV

Dashboard interactif d'analyse de la régularité des TGV sur le réseau SNCF (2018-2025).

## Demo live
> Lien à ajouter après déploiement Streamlit

##  Fonctionnalités
- KPIs : circulations prévues, retard moyen départ et arrivée
- Évolution temporelle des retards (2018-2025)
- Répartition des causes de retard (infrastructure, trafic, matériel…)
- Top 10 des gares avec le plus de retards
- Filtres interactifs par type de service

##  Structure du projet
```
supply-chain-dashboard/
├── data/raw/          # Dataset SNCF (non versionné)
├── notebooks/         # Exploration et analyse des données
├── src/
│   └── clean_data.py  # Chargement et nettoyage des données
├── app.py             # Dashboard Streamlit
└── README.md
```

## Installation
```bash
git clone https://github.com/abdel55dat/Supply-Chain-Dashboard.git
cd Supply-Chain-Dashboard
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Télécharger le dataset sur [Open Data SNCF](https://ressources.data.sncf.com/explore/dataset/regularite-mensuelle-tgv-aqst) et le placer dans `data/raw/`.
```bash
streamlit run app.py
```

## Stack technique
- Python, Pandas
- Streamlit, Plotly
- Données : Open Data SNCF

## Source des données
[Régularité mensuelle TGV — Open Data SNCF](https://ressources.data.sncf.com/explore/dataset/regularite-mensuelle-tgv-aqst)