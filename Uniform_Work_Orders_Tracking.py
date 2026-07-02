import streamlit as st
import pandas as pd
import os

# Configuration
FILE_PATH = 'Aramark (Vestis) Uniform Spreadsheet.xlsx'
SHEET_NAME = 'Uniform Work Order Tracking' # Ensure this matches your tab name

st.set_page_config(page_title="Uniform Tracker", layout="wide")

st.title("Uniform Work Order Management")

# Load data
@st.cache_data
def load_data():
    return pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)

df = load_data()

# Interactive Editor
st.subheader("Edit Work Orders")
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# Save Button
if st.button("Save Changes"):
    try:
        # Write back to Excel
        with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            edited_df.to_excel(writer, sheet_name=SHEET_NAME, index=False)
        st.success("Data updated successfully!")
    except Exception as e:
        st.error(f"Error saving data: {e}")