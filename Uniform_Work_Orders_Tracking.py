import streamlit as st
import pandas as pd
import os
from datetime import datetime

# File path
FILE_PATH = 'Aramark (Vestis) Uniform Spreadsheet.xlsx'

def load_and_clean_data():
    if not os.path.exists(FILE_PATH):
        st.error(f"File '{FILE_PATH}' not found!")
        return pd.DataFrame()
    
    # Load data
    df = pd.read_excel(FILE_PATH, sheet_name='Uniform Work Order Tracking')
    
    # 1. Remove rows that are entirely empty
    df = df.dropna(how='all')
    
    # 2. Drop the unwanted "Unnamed" columns
    cols_to_drop = [c for c in df.columns if "Unnamed" in str(c)]
    df = df.drop(columns=cols_to_drop)
    
    return df

st.title("Uniform Work Order Tracking")

# Load and display cleaned data
df = load_and_clean_data()
st.subheader("Current Entries")
st.dataframe(df)

# Automate data entry form
st.subheader("Add New Work Order")
with st.form("new_entry_form", clear_on_submit=True):
    new_data = {}
    cols = st.columns(2)
    
    # Generate inputs based on remaining clean columns
    for i, col in enumerate(df.columns):
        with cols[i % 2]:
            if col == 'Date of Order':
                # Calendar Dropdown
                new_data[col] = st.date_input(f"{col}", value=datetime.now())
            elif col == 'Workorder Number':
                # Multi-line comment area
                new_data[col] = st.text_area(f"{col} (Add comments here if needed)")
            else:
                new_data[col] = st.text_input(f"{col}")
    
    submit = st.form_submit_button("Save New Work Order")

if submit:
    new_row = pd.DataFrame([new_data])
    # Ensure the date is formatted as a string for Excel if preferred
    new_row['Date of Order'] = new_row['Date of Order'].astype(str)
    
    updated_df = pd.concat([df, new_row], ignore_index=True)
    
    # Save back to Excel
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        updated_df.to_excel(writer, sheet_name='Uniform Work Order Tracking', index=False)
    
    st.success("Entry saved successfully!")
    st.rerun()
