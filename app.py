import streamlit as st
import pandas as pd
import plotly.express as px
from src.clean_data import load_data, clean_data

st.set_page_config(page_title="Dashboard Ponctualité TGV", layout="wide")

@st.cache_data
def get_data():
    df = load_data()
    df = clean_data(df)
    return df

df = get_data()

# ---- SIDEBAR ----
st.sidebar.title("Filtres")
services = st.sidebar.multiselect(
    "Service", options=sorted(df["service"].unique()), default=sorted(df["service"].unique())
)
df_filtered = df[df["service"].isin(services)]

# ---- HEADER ----
st.title("Dashboard Ponctualité TGV")
st.markdown("Analyse de la régularité des TGV sur le réseau SNCF")

# ---- KPIs ----
col1, col2, col3 = st.columns(3)
col1.metric("Circulations prévues", f"{int(df_filtered['nombre_de_circulations_prévues'].sum()):,}")
col2.metric("Retard moyen départ (min)", f"{df_filtered['retard_moyen_des_trains_en_retard_au_départ'].mean():.1f}")
col_arrivee = [c for c in df_filtered.columns if 'retard_moyen_des_trains_en_retard' in c and 'arrivee' in c.replace('é','e').replace('è','e').replace('ê','e')][0]
col3.metric("Retard moyen arrivée (min)", f"{df_filtered[col_arrivee].mean():.1f}")

# ---- GRAPHIQUE 1 : évolution des retards ----
st.subheader("Évolution du retard moyen dans le temps")
evolution = df_filtered.groupby("date")["retard_moyen_de_tous_les_trains_au_départ"].mean().reset_index()
fig1 = px.line(evolution, x="date", y="retard_moyen_de_tous_les_trains_au_départ",
               labels={"retard_moyen_de_tous_les_trains_au_départ": "Retard moyen (min)", "date": "Date"})
st.plotly_chart(fig1, use_container_width=True)

# ---- GRAPHIQUE 2 : causes des retards ----
st.subheader("Répartition des causes de retard (%)")
causes = {
    "Externe": df_filtered["prct_retard_pour_causes_externes"].mean(),
    "Infrastructure": df_filtered["prct_retard_pour_cause_infrastructure"].mean(),
    "Trafic": df_filtered["prct_retard_pour_cause_gestion_trafic"].mean(),
    "Matériel": df_filtered["prct_retard_pour_cause_matériel_roulant"].mean(),
    "Gare": df_filtered["prct_retard_pour_cause_gestion_en_gare_et_réutilisation_de_matériel"].mean(),
    "Voyageurs": df_filtered["prct_retard_pour_cause_prise_en_compte_voyageurs_(affluence,_gestions_psh,_correspondances)"].mean(),
}
fig2 = px.bar(x=list(causes.keys()), y=list(causes.values()),
              labels={"x": "Cause", "y": "% moyen"}, color=list(causes.keys()))
st.plotly_chart(fig2, use_container_width=True)

# ---- GRAPHIQUE 3 : top gares avec le plus de retards ----
st.subheader("Top 10 des gares de départ avec le plus de retards")
top_gares = df_filtered.groupby("gare_de_départ")["retard_moyen_de_tous_les_trains_au_départ"].mean().nlargest(10).reset_index()
fig3 = px.bar(top_gares, x="retard_moyen_de_tous_les_trains_au_départ", y="gare_de_départ",
              orientation="h", labels={"retard_moyen_de_tous_les_trains_au_départ": "Retard moyen (min)", "gare_de_départ": "Gare"})
st.plotly_chart(fig3, use_container_width=True)