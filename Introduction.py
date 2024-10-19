import streamlit as st
import streamlit_folium
import webbrowser
import pandas as pd

st.set_page_config(
    page_title="Forest Fires Dashboard",
    layout="wide",
    page_icon="🔥")

@st.cache_data
def load_data(link, sep=";"):
    data = pd.read_csv(link, sep=sep)
    return data

def sidebar_info():    

    st.sidebar.markdown("# **ABOUT ME**")
    # st.sidebar.markdown('<p align="center"><img src="https://via.placeholder.com/150"></p>', unsafe_allow_html=True)
    st.sidebar.image("https://via.placeholder.com/150", use_column_width=True)
    
    st.sidebar.markdown("**Name :** Virgle Martel")
    st.sidebar.markdown("**Contact :** virgile.martel@efrei.net")

    st.sidebar.markdown("---")  
    
    if st.sidebar.button("LinkedIn"):webbrowser.open_new_tab('https://www.linkedin.com/in/martelvirgile/')

    if st.sidebar.button("Github"):webbrowser.open_new_tab('https://github.com/Skrinox')


    
    st.sidebar.markdown("---") 

def main():
    st.title("Forest Fires Dashboard")
    st.markdown("Bienvenue dans cette application de présentation de données.")

    st.markdown("### What does our data look like? :thinking_face:")

    # We load the data
    data = load_data("Incendies.csv")

    # We display the data
    st.write(data)

sidebar_info()
main()

