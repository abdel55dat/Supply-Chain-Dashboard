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

#SIDEBAR
st.sidebar.title("Filtres")
services = st.sidebar.multiselect(
    "Service", options=sorted(df["service"].unique()), default=sorted(df["service"].unique())
)
df_filtered = df[df["service"].isin(services)]

#HEADER
st.title("Dashboard Ponctualité TGV")
st.markdown("Analyse de la régularité des TGV sur le réseau SNCF")

#KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Circulations prévues", f"{int(df_filtered['nb_train_prevu'].sum()):,}")
col2.metric("Retard moyen départ (min)", f"{df_filtered['retard_moyen_depart'].mean():.1f}")
col3.metric("Retard moyen arrivée (min)", f"{df_filtered['retard_moyen_arrivee'].mean():.1f}")

#GRAPHIQUE 1
st.subheader("Évolution du retard moyen dans le temps")
evolution = df_filtered.groupby("date")["retard_moyen_tous_trains_depart"].mean().reset_index()
fig1 = px.line(evolution, x="date", y="retard_moyen_tous_trains_depart",
               labels={"retard_moyen_tous_trains_depart": "Retard moyen (min)", "date": "Date"})
st.plotly_chart(fig1, use_container_width=True)

#GRAPHIQUE 2
st.subheader("Répartition des causes de retard (%)")
causes = {
    "Externe": df_filtered["prct_cause_externe"].mean(),
    "Infrastructure": df_filtered["prct_cause_infra"].mean(),
    "Trafic": df_filtered["prct_cause_gestion_trafic"].mean(),
    "Matériel": df_filtered["prct_cause_materiel_roulant"].mean(),
    "Gare": df_filtered["prct_cause_gestion_gare"].mean(),
    "Voyageurs": df_filtered["prct_cause_prise_en_charge_voyageurs"].mean(),
}
fig2 = px.bar(x=list(causes.keys()), y=list(causes.values()),
              labels={"x": "Cause", "y": "% moyen"}, color=list(causes.keys()))
st.plotly_chart(fig2, use_container_width=True)

#GRAPHIQUE 3
st.subheader("Top 10 des gares de départ avec le plus de retards")
top_gares = df_filtered.groupby("gare_depart")["retard_moyen_tous_trains_depart"].mean().nlargest(10).reset_index()
fig3 = px.bar(top_gares, x="retard_moyen_tous_trains_depart", y="gare_depart",
              orientation="h", labels={"retard_moyen_tous_trains_depart": "Retard moyen (min)", "gare_depart": "Gare"})
st.plotly_chart(fig3, use_container_width=True)