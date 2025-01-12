import json
from io import BytesIO

import pandas as pd
import streamlit as st
from streamlit_tags import st_tags_sidebar

from scrapper import scrape_and_clean

st.set_page_config(page_title="Universal Web Scraper", page_icon="🦑")

st.markdown(
    """
    <h1 style='text-align: center;'>Universal Web Scraper 
        <span style='display: inline-block; transform: rotate(45deg);'>🦑</span>
    </h1>
    """,
    unsafe_allow_html=True,
)
st.sidebar.header("Web Scraper Settings")

model = st.sidebar.selectbox("Select Model", ("Gemini 1.5 Flash"))

url = st.sidebar.text_input("Enter URL", "")
keyword = st_tags_sidebar(
    label="Enter Fields to Extract:",
    text="Press enter to add more",
    value=[],
    suggestions=[],
    maxtags=8,
)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

scrape_button = st.sidebar.button("Scrape")

if scrape_button:
    with st.spinner("Scraping data... Please wait."):
        result = scrape_and_clean(url, keyword)
        if isinstance(result, str):
            try:
                result_dict = json.loads(result)
            except:

                last_occurrence_index = result.rfind("}")

                result = result[: last_occurrence_index + 1] + "]}"
                result_dict = json.loads(result)

    st.session_state.df = pd.DataFrame(result_dict["listings"])
    st.session_state.csv = st.session_state.df.to_csv(index=False).encode("utf-8")
    st.session_state.json = st.session_state.df.to_json(orient="records").encode(
        "utf-8"
    )
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        st.session_state.df.to_excel(writer, index=False, sheet_name="Sheet1")
    excel_buffer.seek(0)
    st.session_state.excel_buffer = excel_buffer

if "df" in st.session_state:
    st.dataframe(st.session_state.df)
    st.title("Download Options:")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            label="Download as CSV",
            data=st.session_state.csv,
            file_name="Output_data.csv",
            mime="text/csv",
        )

    with col2:
        st.download_button(
            label="Download as JSON",
            data=st.session_state.json,
            file_name="Output_data.json",
            mime="application/json",
        )

    with col3:
        st.download_button(
            label="Download as Excel",
            data=st.session_state.excel_buffer,
            file_name="Output_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
