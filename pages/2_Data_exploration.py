import streamlit as st
from Introduction import sidebar_info, load_data_once
import pandas as pd
import folium
import streamlit_folium as st_folium

st.set_page_config(
    page_title="Data Exploration",
    layout="wide",
    page_icon="📊")

sidebar_info()

data = load_data_once()

st.title("Data Exploration")


