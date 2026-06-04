import streamlit as st
import plotly.express as px
import pandas as pd

TABLE_NAME = "only_cars"

st.set_page_config(
    page_title="DCM",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

vanilla_css = """
    <style>
    .stApp, .stApp * {
        color: #000000 !important;
    }
    .stApp {
        background-color: #EDE8D0 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #C9C5B1 !important;
    }
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    button[data-baseweb="tab"] {
        color: #787569 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #000000 !important;
        border-bottom-color: #4F4D46 !important;
    }
    </style>
"""
st.markdown(vanilla_css, unsafe_allow_html=True)


def apply_vanilla_theme(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#000000",
        title_font_color="#4F4D46",
        xaxis=dict(showgrid=True, gridcolor="#C9C5B1", tickfont=dict(color="#000000")),
        yaxis=dict(showgrid=True, gridcolor="#C9C5B1", tickfont=dict(color="#000000")),
        legend=dict(font=dict(color="#000000"))
    )
    return fig


conn = st.connection("sql", type="sql")

st.title("DCM")
st.markdown("---")

tab_fuel, tab_history, tab_regional = st.tabs([
    "Fuel Trends",
    "Historical Snapshots",
    "Regional Breakdown"
])

with tab_fuel:
    st.header("Fuel Types Evolution (2000 - 2020)")
    st.write("The chart displays the share of various fuel types in newly registered vehicles.")

    query_fuel = f"""
        SELECT 
            SUBSTR(data_pierwszej_rej, 1, 4) AS Year,
            rodzaj_paliwa AS Fuel,
            COUNT(*) AS Count
        FROM {TABLE_NAME}
        WHERE SUBSTR(data_pierwszej_rej, 1, 4) BETWEEN '2000' AND '2020'
          AND rodzaj_paliwa IS NOT NULL AND rodzaj_paliwa != ''
        GROUP BY Year, Fuel
        ORDER BY Year ASC
    """
    df_fuel = conn.query(query_fuel)

    if not df_fuel.empty:
        fig_fuel = px.area(
            df_fuel,
            x="Year",
            y="Count",
            color="Fuel",
            color_discrete_sequence=["#4F4D46", "#787569", "#C9C5B1", "#A3A08E", "#EDE8D0"]
        )
        st.plotly_chart(apply_vanilla_theme(fig_fuel), use_container_width=True)
    else:
        st.warning("No fuel data available.")

with tab_history:
    st.header("Vehicle Market Structure Comparison")
    st.write("Select two years to compare the share of the TOP 10 most registered brands.")

    col1, col2 = st.columns(2)
    with col1:
        year_a = st.selectbox("Select base year", list(range(2000, 2021)), index=17)
    with col2:
        year_b = st.selectbox("Select comparison year", list(range(2000, 2021)), index=18)

    query_history = f"""
        SELECT 
            SUBSTR(data_pierwszej_rej, 1, 4) AS Year,
            marka AS Brand,
            COUNT(*) AS Count
        FROM {TABLE_NAME}
        WHERE SUBSTR(data_pierwszej_rej, 1, 4) IN ('{year_a}', '{year_b}')
          AND marka IS NOT NULL AND marka != ''
        GROUP BY Year, Brand
    """
    df_history = conn.query(query_history)

    if not df_history.empty:
        top_brands = df_history.groupby("Brand")["Count"].sum().nlargest(10).index
        df_history_filtered = df_history[df_history["Brand"].isin(top_brands)]

        fig_history = px.bar(
            df_history_filtered,
            x="Brand",
            y="Count",
            color="Year",
            barmode="group",
            color_discrete_sequence=["#787569", "#4F4D46"]
        )
        st.plotly_chart(apply_vanilla_theme(fig_history), use_container_width=True)
    else:
        st.warning("No sufficient data available for comparison.")

with tab_regional:
    st.header("Registrations Analysis by County")

    query_woj = f"""
        SELECT DISTINCT akt_miejsce_rej_wojwe 
        FROM {TABLE_NAME} 
        WHERE akt_miejsce_rej_wojwe IS NOT NULL AND akt_miejsce_rej_wojwe != ''
        ORDER BY akt_miejsce_rej_wojwe ASC
    """
    lista_woj = conn.query(query_woj)

    if not lista_woj.empty:
        wybrane_woj = st.selectbox("Select Voivodeship", lista_woj["akt_miejsce_rej_wojwe"].tolist())

        query_powiaty = f"""
            SELECT 
                akt_miejsce_rej_powiat AS County,
                COUNT(*) AS Count
            FROM {TABLE_NAME}
            WHERE akt_miejsce_rej_wojwe = '{wybrane_woj}'
              AND akt_miejsce_rej_powiat IS NOT NULL AND akt_miejsce_rej_powiat != ''
              AND SUBSTR(data_pierwszej_rej, 1, 4) BETWEEN '2000' AND '2020'
            GROUP BY County
            ORDER BY Count DESC
            LIMIT 15
        """
        df_powiaty = conn.query(query_powiaty)

        if not df_powiaty.empty:
            fig_regional = px.bar(
                df_powiaty,
                x="Count",
                y="County",
                orientation="h",
                title=f"TOP 15 Counties in {wybrane_woj}",
                color_discrete_sequence=["#4F4D46"]
            )
            fig_regional.update_yaxes(autorange="reversed")
            st.plotly_chart(apply_vanilla_theme(fig_regional), use_container_width=True)
        else:
            st.warning("No county data available for the selected voivodeship.")
    else:
        st.warning("No administrative division data available.")