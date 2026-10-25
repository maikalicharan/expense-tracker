import json
import os
import streamlit as st

import gspread
from google.oauth2.service_account import Credentials

@st.cache_resource
def get_google_sheet():
    credentials_json = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    credentials_info = json.loads(credentials_json)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = Credentials.from_service_account_info(
        credentials_info,
        scopes=scopes,
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open("Expenses")

    worksheet = spreadsheet.sheet1

    return worksheet
