import streamlit as st


def apply_custom_css():

    st.markdown(
        """
        <style>

        /* -------------------------------------------------
           Global
        ------------------------------------------------- */

        .stApp {
            background-color: #f7f8fc;
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }


        /* -------------------------------------------------
           Typography
        ------------------------------------------------- */

        h1 {
            font-size: 2rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px;
        }

        h2 {
            font-size: 1.45rem !important;
            font-weight: 650 !important;
        }

        h3 {
            font-size: 1.15rem !important;
            font-weight: 650 !important;
        }

        p {
            line-height: 1.6;
        }


        /* -------------------------------------------------
           Sidebar
        ------------------------------------------------- */

        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e8eaf0;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1.5rem;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #343741;
        }


        /* -------------------------------------------------
           Navigation
        ------------------------------------------------- */

        [data-testid="stSidebarNav"] {
            padding-top: 0.5rem;
        }

        [data-testid="stSidebarNav"] li {
            margin-bottom: 0.2rem;
        }

        [data-testid="stSidebarNav"] a {
            border-radius: 10px;
            padding: 0.55rem 0.75rem;
            transition: all 0.15s ease;
        }

        [data-testid="stSidebarNav"] a:hover {
            background-color: #f1f3f8;
        }


        /* -------------------------------------------------
           Buttons
        ------------------------------------------------- */

        .stButton > button {
            border-radius: 10px;
            min-height: 2.6rem;
            font-weight: 600;
            border: 1px solid #dfe2e8;
            transition: all 0.15s ease;
        }

        .stButton > button:hover {
            border-color: #b9bec9;
            transform: translateY(-1px);
        }


        /* -------------------------------------------------
           Inputs
        ------------------------------------------------- */

        .stTextInput input,
        .stNumberInput input,
        .stDateInput input {
            border-radius: 9px;
        }

        .stSelectbox [data-baseweb="select"] > div {
            border-radius: 9px;
        }

        textarea {
            border-radius: 9px !important;
        }


        /* -------------------------------------------------
           Metric Cards
        ------------------------------------------------- */

        [data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e8eaf0;
            border-radius: 14px;
            padding: 1rem 1.1rem;
            box-shadow: 0 2px 8px rgba(20, 25, 40, 0.04);
        }

        [data-testid="stMetricLabel"] {
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            font-weight: 700;
        }


        /* -------------------------------------------------
           Dataframes / Tables
        ------------------------------------------------- */

        [data-testid="stDataFrame"] {
            border: 1px solid #e5e7ed;
            border-radius: 12px;
            overflow: hidden;
        }


        /* -------------------------------------------------
           Expanders
        ------------------------------------------------- */

        [data-testid="stExpander"] {
            border: 1px solid #e5e7ed;
            border-radius: 12px;
        }


        /* -------------------------------------------------
           Alerts
        ------------------------------------------------- */

        [data-testid="stAlert"] {
            border-radius: 10px;
        }


        /* -------------------------------------------------
           Dividers
        ------------------------------------------------- */

        hr {
            border-color: #e8eaf0;
        }


        /* -------------------------------------------------
           Download buttons
        ------------------------------------------------- */

        .stDownloadButton > button {
            border-radius: 10px;
            font-weight: 600;
        }


        /* -------------------------------------------------
           Mobile
        ------------------------------------------------- */

        @media (max-width: 768px) {

            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
                padding-top: 1.25rem;
            }

            h1 {
                font-size: 1.6rem !important;
            }

            h2 {
                font-size: 1.25rem !important;
            }

            [data-testid="stMetric"] {
                padding: 0.8rem;
            }

        }

        </style>
        """,
        unsafe_allow_html=True,
    )
