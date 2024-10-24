import folium
import streamlit as st
import streamlit_folium as st_folium
import webbrowser
import pandas as pd
import requests


st.set_page_config(
    page_title="Forest Fires Dashboard",
    layout="wide",
    page_icon="🔥")

 
@st.cache_data
def load_data(link, sep=";"):
    data = pd.read_csv(link, sep=sep)
    data['Date de la première alerte'] = pd.to_datetime(data['Date de première alerte'], format='%Y-%m-%d %H:%M:%S')

    data['Latitude'] = None
    data['Longitude'] = None

    for idx, row in data.iterrows():
        lat, lon = get_coordinates_from_insee(row['Code INSEE'])
        if lat and lon:
            data.at[idx, 'Latitude'] = lat
            data.at[idx, 'Longitude'] = lon
    
    st.balloons()
    return data

def load_data_once():
    """Vérifie si les données sont déjà chargées dans session_state, sinon on les charge"""
    if 'data' not in st.session_state:
        st.session_state['data'] = load_data("Incendies.csv", sep=";")
    return st.session_state['data']

@st.cache_data
def get_coordinates_from_insee(code_insee):

    url = f"https://geo.api.gouv.fr/communes/{code_insee}?fields=centre&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['centre']['coordinates'][1], data['centre']['coordinates'][0]  # latitude, longitude
    else:
        return None, None


def sidebar_info():    

    st.sidebar.markdown("# **ABOUT ME**")
    st.sidebar.image("img/photoCV.png", use_column_width=True)
    
    st.sidebar.markdown("**Name :** Virgle Martel")
    st.sidebar.markdown("**Contact :** virgile.martel@efrei.net")

    st.sidebar.markdown("---")  
    
    if st.sidebar.button("LinkedIn"):webbrowser.open_new_tab('https://www.linkedin.com/in/martelvirgile/')

    if st.sidebar.button("Github"):webbrowser.open_new_tab('https://github.com/Skrinox')


    
    st.sidebar.markdown("---") 

def main():
    st.title("Forest Fires Dashboard")

    data = load_data_once()

    st.markdown('### Why the forest fires? :fire:')
    st.markdown("The forest fires are a major environmental issue. They are responsible for the destruction of thousands of hectares of forest every year. They also have a significant impact on the environment and biodiversity. In addition, they can have serious consequences for human health and the economy.")
    st.markdown('It is interesting to study the location of these fires forest and there number as well as the period when they occur. It is also a great way to understand the impact of climate change on the environment.')
    
    st.markdown("### The dataset :bar_chart:")
    st.markdown("The dataset contains information about forest fires in France. The extracted data dates from the beginning of 2022 to the end of 2023. The data comes from the official French government application: [Database on Forest Fires in France](https://bdiff.agriculture.gouv.fr/) (BDIFF). This can also be found from this [link](https://www.data.gouv.fr/fr/datasets/base-de-donnees-sur-les-incendies-de-forets-en-france-bdiff/).")
    st.markdown("Since 2006, the BDIFF has been centralizing data on forest fires in France and making them available to the public and government departments. The data is aggregated at municipal level and covers the whole of France.")

    st.markdown("### What does our data look like? :thinking_face:")
    st.write(data)
    st.markdown("The last two columns, Latitude and Longitude, as been added by querying the API of the French government: [geo.api.gouv.fr](https://geo.api.gouv.fr/decoupage-administratif/communes#geo). This API allows us to get the coordinates of a municipality based on its INSEE code. This will allow us to display the location of the fires on a map.")

    
sidebar_info()
main()

