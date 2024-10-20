import streamlit as st
from Introduction import sidebar_info, load_data_once
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Data Exploration",
    layout="wide",
    page_icon="📊")

sidebar_info()

data = load_data_once()

st.title("Data Exploration")

commune_options = data['Nom de la commune'].unique().tolist()
communes = st.multiselect("Select communes", commune_options)

filtered_data = data[data['Nom de la commune'].isin(communes)]
fig = px.bar(filtered_data, x='Nom de la commune', y='Surface parcourue (m2)', color='Nom de la commune', title="Surface Burned by Commune")
st.plotly_chart(fig)

st.markdown("The south of France is the most affected by forest fires. They have a lot of small vegetation with dry ground during summer (scrubland and garrigue) wich made them more sensitive to fire.")

st.markdown("### Number of fires over the year")

annee_selectionnee = st.selectbox("Sélectionnez une année pour afficher les incendies :", pd.to_datetime(data['Date de première alerte']).dt.year.unique())

filtered_data = data[
    (pd.to_datetime(data['Date de première alerte']).dt.year == annee_selectionnee)
]

col1, col2 = st.columns([2, 1])
with col1:
    fig = px.histogram(filtered_data, x='Date de première alerte', title="Number of fires per month")
    st.plotly_chart(fig)

with col2:
    fig2 = px.pie(filtered_data, names="Nature", title="Nature of fires")
    st.plotly_chart(fig2)