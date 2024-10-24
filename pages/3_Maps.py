import streamlit as st
from Introduction import sidebar_info, load_data_once
import pandas as pd
import folium
import streamlit_folium as st_folium
from folium.plugins import HeatMap
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import datetime

st.set_page_config(
    page_title="Maps",
    layout="wide",
    page_icon="🗺️")

sidebar_info()

data = load_data_once()

st.markdown("### Where do these fires occur? :world_map:") 

min_date = data['Date de première alerte'].min()
max_date = data['Date de première alerte'].max()

min_date = pd.to_datetime(min_date)
max_date = pd.to_datetime(max_date)

selected_dates = st.date_input("Select a date range:", [min_date, min_date], min_value=min_date, max_value=max_date)

col1, col2, col3 = st.columns([2, 1, 2], vertical_alignment="center")

if len(selected_dates) == 2:
    start_date, end_date = selected_dates[0], selected_dates[1]

    filtered_data = data[(pd.to_datetime(data['Date de première alerte']) >= pd.to_datetime(start_date)) &
                         (pd.to_datetime(data['Date de première alerte']) <= pd.to_datetime(end_date))]

    with col1:
        map = folium.Map(location=[46, 1], zoom_start=6)

        for _, row in filtered_data.iterrows():
            if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=f"Incendie à {row['Nom de la commune']} le {row['Date de première alerte']}"
                ).add_to(map)
        st_folium.st_folium(map, width=700, height=650)


    with col2:
        st.markdown("### Global Insights")
        
        total_fires = len(filtered_data)
        st.metric(label="Total Fires", value=total_fires)
        
        total_area = filtered_data['Surface parcourue (m2)'].sum()
        avg_area = total_area / total_fires if total_fires > 0 else 0

        st.metric(label="Total Burned Area (ha)", value=total_area)
        st.metric(label="Average Burned Area (ha)", value=avg_area.__round__(2))

        st.metric(label="Total Burned Area (km²)", value=total_area / 100 if total_fires > 0 else 0)
        
        total_communes = filtered_data['Nom de la commune'].nunique()
        st.metric(label="Unique Communes Affected", value=total_communes)

        style_metric_cards()

        surface_columns = [
            'Surface forêt (m2)', 'Surface maquis garrigues (m2)', 
            'Autres surfaces naturelles hors forêt (m2)', 'Surfaces agricoles (m2)',
            'Autres surfaces (m2)', 'Surface autres terres boisées (m2)'
        ]

        with col3:
            surface_data = filtered_data[surface_columns].sum()
            surface_data = surface_data[surface_data > 0]
        
            if len(surface_data) > 0:
                fig_surface = px.pie(surface_data, values=surface_data.values, names=surface_data.index, title="Types de surface brûlée")
                st.plotly_chart(fig_surface) 
else:
    st.warning("Please select a valid date range.")

st.markdown("---")

st.markdown("### Heatmap of Fires :fire:")


col1, col3, col2 = st.columns([1,0.05, 1])

with col1:
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    selected_month = st.slider(
        "Select a month and a year to display fires :",
        min_value=start_date,
        max_value=end_date,
        value=datetime.date(2022, 1, 1),
        format="MM/YYYY"
    )

    filtered_data = data[
        (pd.to_datetime(data['Date de première alerte']).dt.year == selected_month.year) &
        (pd.to_datetime(data['Date de première alerte']).dt.month == selected_month.month)
    ]
    map = folium.Map(location=[46, 1], zoom_start=6)
    heat_data = [[row['Latitude'], row['Longitude']] for _, row in filtered_data.iterrows() if pd.notna(row['Latitude']) and pd.notna(row['Longitude'])]
    if heat_data:
        HeatMap(heat_data, radius=18).add_to(map)
    st_folium.st_folium(map, width=700, height=700)  

with col2:

    annee_selectionnee = st.selectbox("Select a year :", pd.to_datetime(data['Date de première alerte']).dt.year.unique())

    filtered_data = data[
        (pd.to_datetime(data['Date de première alerte']).dt.year == annee_selectionnee)
    ]
    map = folium.Map(location=[46, 1], zoom_start=6)
    heat_data = [[row['Latitude'], row['Longitude']] for _, row in filtered_data.iterrows() if pd.notna(row['Latitude']) and pd.notna(row['Longitude'])]
    if heat_data:
        HeatMap(heat_data, radius=18).add_to(map)
    st_folium.st_folium(map, width=700, height=700)  