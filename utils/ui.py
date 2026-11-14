import streamlit as st


def apply_custom_css():

    st.markdown(
        """
        <style>

        /* =================================================
           GLOBAL APP
        ================================================= */

        .stApp {
            background-color: #f7f8fc;
        }

        .main .block-container {
            max-width: 1400px;
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
        }


        /* =================================================
           TYPOGRAPHY
        ================================================= */

        h1 {
            font-size: 1.9rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.4px;
            color: #20242d;
        }

        h2 {
            font-size: 1.35rem !important;
            font-weight: 650 !important;
            color: #252a34;
        }

        h3 {
            font-size: 1.08rem !important;
            font-weight: 650 !important;
            color: #303642;
        }

        p {
            color: #555c69;
        }


        /* =================================================
           SIDEBAR
           ================================================= */

        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e5e7ed;
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1.25rem;
        }

        [data-testid="stSidebarNav"] {
            padding-top: 0.25rem;
        }

        [data-testid="stSidebarNav"] li {
            margin-bottom: 0.1rem;
        }

        [data-testid="stSidebarNav"] a {
            border-radius: 8px;
            padding: 0.42rem 0.65rem;
            min-height: 2.1rem;
            transition: background-color 0.15s ease;
        }

        [data-testid="stSidebarNav"] a:hover {
            background-color: #f1f3f7;
        }


        /* =================================================
           BUTTONS
           ================================================= */

        .stButton > button {
            min-height: 2.15rem;
            height: 2.15rem;
            padding: 0.25rem 0.8rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            border: 1px solid #d8dce5;
            background-color: #ffffff;
            color: #303642;
            box-shadow: none;
            transition: all 0.15s ease;
        }

        .stButton > button:hover {
            border-color: #8b94a5;
            background-color: #f8f9fb;
            transform: translateY(-1px);
        }

        .stButton > button[kind="primary"] {
            background-color: #315fce;
            border-color: #315fce;
            color: #ffffff;
        }

        .stButton > button[kind="primary"]:hover {
            background-color: #284fae;
            border-color: #284fae;
        }


        /* =================================================
           INPUTS
           ================================================= */

        .stTextInput input,
        .stNumberInput input,
        .stDateInput input {
            min-height: 2.25rem;
            border-radius: 8px;
            border: 1px solid #d9dde6;
            background-color: #ffffff;
        }

        .stTextInput input:focus,
        .stNumberInput input:focus,
        .stDateInput input:focus {
            border-color: #6d8fe5;
            box-shadow: 0 0 0 1px #6d8fe5;
        }

        .stSelectbox [data-baseweb="select"] > div {
            min-height: 2.25rem;
            border-radius: 8px;
            border: 1px solid #d9dde6;
            background-color: #ffffff;
        }


        /* =================================================
           METRIC CARDS
           ================================================= */

        [data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e4e7ed;
            border-radius: 12px;
            padding: 0.85rem 1rem;
            box-shadow: 0 2px 8px rgba(20, 25, 40, 0.04);
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.82rem;
            font-weight: 600;
            color: #606776;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.45rem;
            font-weight: 700;
            color: #242934;
        }


        /* =================================================
           DATA TABLES
           ================================================= */

        [data-testid="stDataFrame"] {
            border: 1px solid #e3e6ec;
            border-radius: 10px;
            overflow: hidden;
            background-color: #ffffff;
        }


        /* =================================================
           ALERTS
           ================================================= */

        [data-testid="stAlert"] {
            border-radius: 9px;
        }


        /* =================================================
           EXPANDERS
           ================================================= */

        [data-testid="stExpander"] {
            border: 1px solid #e2e5eb;
            border-radius: 10px;
            background-color: #ffffff;
        }


        /* =================================================
           DIVIDERS
           ================================================= */

        hr {
            border-color: #e5e7ed;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }


        /* =================================================
           DOWNLOAD BUTTONS
           ================================================= */

        .stDownloadButton > button {
            min-height: 2.15rem;
            height: 2.15rem;
            padding: 0.25rem 0.8rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
        }


        /* =================================================
           FORM SUBMIT BUTTONS
           ================================================= */

        .stFormSubmitButton > button {
            min-height: 2.25rem;
            height: 2.25rem;
            padding: 0.3rem 0.9rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
        }


        /* =================================================
           MOBILE
           ================================================= */

        @media (max-width: 768px) {

            .main .block-container {
                padding-left: 0.9rem;
                padding-right: 0.9rem;
                padding-top: 1rem;
            }

            h1 {
                font-size: 1.55rem !important;
            }

            h2 {
                font-size: 1.2rem !important;
            }

            [data-testid="stMetric"] {
                padding: 0.7rem;
            }

            [data-testid="stMetricValue"] {
                font-size: 1.2rem;
            }

            .stButton > button {
                min-height: 2rem;
                height: 2rem;
                font-size: 0.8rem;
            }

        }

        </style>
        """,
        unsafe_allow_html=True,
    )
