import streamlit as st

st.set_page_config(
    page_title="DCM",
    page_icon="📰",
    layout="centered"
)
enforce_theme_css = """
    <style>
    .stApp, .stApp * {
        color: #000000 !important;
    }

    div[data-baseweb="input"] {
        border-color: #787569 !important;
    }

    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(enforce_theme_css, unsafe_allow_html=True)


st.title("DCM")
st.write(
    "A comprehensive analysis of vehicle registration data in Poland based on the CEPIK API."
)
