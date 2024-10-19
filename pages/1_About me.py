import streamlit as st
from Introduction import sidebar_info
import time
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="About me 📚",
    page_icon="📚",
    layout="wide"
    )

st.title("About me")

date_naissance_timestamp = 1048201200  # 21 mars 2003 à 1h du matin en timestamp
current_timestamp = time.time()  # Timestamp actuel

# Fonction pour calculer l'âge en fonction du timestamp
def calculer_age(timestamp_naissance, timestamp_actuel):
    age_en_secondes = timestamp_actuel - timestamp_naissance
    
    years = age_en_secondes // (365 * 24 * 3600)
    age_en_secondes %= (365 * 24 * 3600)
    
    months = age_en_secondes // (30 * 24 * 3600)
    age_en_secondes %= (30 * 24 * 3600)

    days = age_en_secondes // (24 * 3600)
    age_en_secondes %= (24 * 3600)
    
    hours = age_en_secondes // 3600
    age_en_secondes %= 3600
    
    minutes = age_en_secondes // 60
    seconds = age_en_secondes % 60

    return int(years), int(months), int(days), int(hours), int(minutes), int(seconds)

col1, col2 = st.columns([1, 3], vertical_alignment="center")

with col1:
    st.image("img\photoCV.png", width=300)

with col2:
    st_autorefresh(1000)
    photo_side = st.container(border=True)
    photo_side.markdown("**Name :** Virgile Martel")
    current_timestamp = time.time()
    years, months, days, hours, minutes, seconds = calculer_age(date_naissance_timestamp, current_timestamp)
    photo_side.write(f"**Age :** {years} years, {months} months, {days} days, {hours}h{minutes}:{int(seconds)}")
    photo_side.markdown("**Contact :** virgile.martel@efrei.net")

    photo_side.markdown(" As a 2nd year engineering student (M1) at Efrei. I'm enthusiastic about actively contributing to a dynamic team and applying my skills and knowledge to new challenges. Curious, I regularly inform myself about technological advances and what they can bring to our daily lives. As a sportsman, I've taken part in various activities including indoor soccer, English boxing and CrossFit, which enable me to develop not only my physical fitness, but also the skills of discipline, perseverance and teamwork. At the same time, I am an avid fan of video games, particularly sandbox games, platformers and team-based FPSs.")

with st.expander("My Academic Projects"):
    st.markdown("#### **Explain** - AI patent data classification - ***July 2024***")
    st.markdown("Programming language : Python - Group of 5 students")
    st.markdown("BERT and FastText AI models for patent classification using the classification system: Cooperative Patent Classification (CPC)")
    st.markdown("Explanation of prediction in graphical and highlighted text form with SHAP (for BERT) and Lime (for FastText).")

with st.expander("My experiences"):
    st.markdown(" ")