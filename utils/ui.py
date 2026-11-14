import streamlit as st


def apply_custom_css():

    theme = st.session_state.get("theme", "Light")

    if theme == "Dark":

        st.markdown(
            """
            <style>

            /* =================================================
               DARK THEME - GLOBAL
            ================================================= */

            .stApp {
                background-color: #0f172a !important;
                color: #e5e7eb !important;
            }

            .main .block-container {
                color: #e5e7eb !important;
            }


            /* =================================================
               TEXT
            ================================================= */

            h1,
            h2,
            h3,
            h4,
            h5,
            h6 {
                color: #f3f4f6 !important;
            }

            p,
            label,
            .stCaption {
                color: #aeb7c5 !important;
            }


            /* =================================================
               SIDEBAR
            ================================================= */

            section[data-testid="stSidebar"] {
                background-color: #0b1220 !important;
                border-right: 1px solid #273449 !important;
            }

            section[data-testid="stSidebar"] a {
                color: #d7dde8 !important;
            }

            section[data-testid="stSidebar"] a:hover {
                background-color: #182235 !important;
            }


            /* =================================================
               BUTTONS
            ================================================= */

            .stButton > button,
            .stDownloadButton > button,
            .stFormSubmitButton > button {
                background-color: #1e293b !important;
                color: #e5e7eb !important;
                border: 1px solid #3b475a !important;
                box-shadow: none !important;
            }

            .stButton > button:hover,
            .stDownloadButton > button:hover,
            .stFormSubmitButton > button:hover {
                background-color: #334155 !important;
                border-color: #64748b !important;
                color: #ffffff !important;
            }

            .stButton > button[kind="primary"],
            .stFormSubmitButton > button[kind="primary"] {
                background-color: #315fce !important;
                border-color: #315fce !important;
                color: #ffffff !important;
            }

            .stButton > button[kind="primary"]:hover,
            .stFormSubmitButton > button[kind="primary"]:hover {
                background-color: #3d70df !important;
                border-color: #3d70df !important;
            }


            /* =================================================
               TEXT INPUTS
            ================================================= */

            .stTextInput input,
            .stNumberInput input,
            .stDateInput input {
                background-color: #1e293b !important;
                color: #f3f4f6 !important;
                border: 1px solid #3b475a !important;
            }

            .stTextInput input::placeholder,
            .stNumberInput input::placeholder {
                color: #7f8a9b !important;
            }


            /* =================================================
               DROPDOWNS
            ================================================= */

            .stSelectbox [data-baseweb="select"] > div,
            .stMultiSelect [data-baseweb="select"] > div {
                background-color: #1e293b !important;
                color: #f3f4f6 !important;
                border: 1px solid #3b475a !important;
            }

            .stSelectbox [data-baseweb="select"] *,
            .stMultiSelect [data-baseweb="select"] * {
                color: #f3f4f6 !important;
            }


            /* Dropdown popup */

            div[data-baseweb="popover"] {
                background-color: #1e293b !important;
                border: 1px solid #3b475a !important;
            }

            div[data-baseweb="menu"] {
                background-color: #1e293b !important;
            }

            div[data-baseweb="menu"] li {
                background-color: #1e293b !important;
                color: #f3f4f6 !important;
            }

            div[data-baseweb="menu"] li:hover {
                background-color: #334155 !important;
            }


            /* =================================================
               DATE PICKER
            ================================================= */

            div[data-baseweb="calendar"] {
                background-color: #1e293b !important;
                color: #f3f4f6 !important;
            }


            /* =================================================
               METRIC CARDS
            ================================================= */

            [data-testid="stMetric"] {
                background-color: #1e293b;
                border-color: #334155;
                color: #f3f4f6;
            }

            [data-testid="stMetricLabel"] {
                color: #aeb7c5 !important;
            }

            [data-testid="stMetricValue"] {
                color: #f3f4f6 !important;
            }


            /* =================================================
               DATAFRAME / TABLE
            ================================================= */

            [data-testid="stDataFrame"] {
                background-color: #1e293b !important;
                border: 1px solid #334155 !important;
            }

            [data-testid="stDataEditor"] {
                background-color: #1e293b !important;
                border: 1px solid #334155 !important;
            }


            /* =================================================
               ALERTS
            ================================================= */

            [data-testid="stAlert"] {
                background-color: #1e293b !important;
                color: #e5e7eb !important;
                border-color: #3b475a !important;
            }


            /* =================================================
               EXPANDERS
            ================================================= */

            [data-testid="stExpander"] {
                background-color: #1e293b !important;
                border: 1px solid #334155 !important;
            }


            /* =================================================
               DIVIDERS
            ================================================= */

            hr {
                border-color: #334155 !important;
            }


            /* =================================================
               CHECKBOX
            ================================================= */

            [data-testid="stCheckbox"] label {
                color: #d7dde8 !important;
            }


            /* =================================================
               PLOTLY CONTAINER
            ================================================= */

            .js-plotly-plot {
                background-color: #0f172a !important;
            }


            </style>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <style>

            /* =================================================
               LIGHT THEME - GLOBAL
            ================================================= */

            .stApp {
                background-color: #f7f8fc !important;
                color: #20242d !important;
            }

            h1,
            h2,
            h3,
            h4,
            h5,
            h6 {
                color: #20242d !important;
            }

            p,
            label,
            .stCaption {
                color: #555c69 !important;
            }


            /* Sidebar */

            section[data-testid="stSidebar"] {
                background-color: #ffffff !important;
                border-right: 1px solid #e5e7ed !important;
            }


            /* Buttons */

            .stButton > button,
            .stDownloadButton > button,
            .stFormSubmitButton > button {
                background-color: #ffffff !important;
                color: #303642 !important;
                border: 1px solid #d4d9e2 !important;
            }

            .stButton > button:hover,
            .stDownloadButton > button:hover,
            .stFormSubmitButton > button:hover {
                background-color: #f3f5f8 !important;
                border-color: #9ba4b3 !important;
            }

            .stButton > button[kind="primary"],
            .stFormSubmitButton > button[kind="primary"] {
                background-color: #315fce !important;
                border-color: #315fce !important;
                color: #ffffff !important;
            }


            /* Inputs */

            .stTextInput input,
            .stNumberInput input,
            .stDateInput input {
                background-color: #ffffff !important;
                color: #20242d !important;
                border-color: #d9dde6 !important;
            }


            /* Dropdowns */

            .stSelectbox [data-baseweb="select"] > div,
            .stMultiSelect [data-baseweb="select"] > div {
                background-color: #ffffff !important;
                color: #20242d !important;
                border-color: #d4d9e2 !important;
            }


            /* Tables */

            [data-testid="stDataFrame"],
            [data-testid="stDataEditor"] {
                background-color: #ffffff !important;
                border-color: #e3e6ec !important;
            }


            /* Expanders */

            [data-testid="stExpander"] {
                background-color: #ffffff !important;
                border-color: #e2e5eb !important;
            }


            /* Dividers */

            hr {
                border-color: #e5e7ed !important;
            }

            </style>
            """,
            unsafe_allow_html=True,
        )
