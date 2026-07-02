import streamlit as st
import pandas as pd
import os

# File path
FILE_PATH = 'Aramark (Vestis) Uniform Spreadsheet.xlsx'

# Function to clean and load data
def load_and_clean_data():
    if not os.path.exists(FILE_PATH):
        st.error(f"File '{FILE_PATH}' not found! Ensure it is in the same folder.")
        return pd.DataFrame()
    
    # Load data specifically from 'Uniform Work Order Tracking'
    df = pd.read_excel(FILE_PATH, sheet_name='Uniform Work Order Tracking')
    
    # Remove rows where all elements are NaN (the blank spaces)
    df = df.dropna(how='all')
    
    return df

st.title("Uniform Work Order Tracking")

# Load and display cleaned data
df = load_and_clean_data()
st.subheader("Current Entries")
st.dataframe(df)

# Automate data entry form
st.subheader("Add New Work Order")
with st.form("new_entry_form", clear_on_submit=True):
    # Dynamically create input fields based on the columns in your sheet
    new_data = {}
    cols = st.columns(2)
    for i, col in enumerate(df.columns):
        with cols[i % 2]:
            new_data[col] = st.text_input(f"{col}")
    
    submit = st.form_submit_button("Save New Work Order")

if submit:
    new_row = pd.DataFrame([new_data])
    updated_df = pd.concat([df, new_row], ignore_index=True)
    
    # Save back to Excel
    # Using openpyxl to replace the sheet with the cleaned, updated version
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        updated_df.to_excel(writer, sheet_name='Uniform Work Order Tracking', index=False)
    
    st.success("Entry saved successfully!")
    st.rerun()
