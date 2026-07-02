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
    
    df = pd.read_excel(FILE_PATH, sheet_name='Uniform Work Order Tracking')
    df = df.dropna(how='all')
    cols_to_drop = [c for c in df.columns if "Unnamed" in str(c)]
    df = df.drop(columns=cols_to_drop, errors='ignore')
    
    if 'Comments' not in df.columns:
        df['Comments'] = ""
    return df

st.title("Uniform Work Order Tracking")

# Define Size Ranges
shirt_sizes = ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL", "6XL"]
pant_sizes = [str(i) for i in range(26, 63)] # 26 to 62

df = load_and_clean_data()
st.subheader("Current Entries")
st.dataframe(df)

st.subheader("Add New Work Order")
with st.form("new_entry_form", clear_on_submit=True):
    new_data = {}
    cols = st.columns(2)
    
    # Standard Fields
    for i, col in enumerate(df.columns):
        with cols[i % 2]:
            if col == 'Date of Order':
                new_data[col] = st.date_input(f"{col}", value=datetime.now())
            elif col == 'Comments':
                new_data[col] = st.text_area("Comments")
            # Injecting dropdowns for specific columns
            elif col == 'Shirt Size':
                new_data[col] = st.selectbox("Shirt Size", shirt_sizes)
            elif col == 'Pants Size':
                new_data[col] = st.selectbox("Pants Size", pant_sizes)
            else:
                new_data[col] = st.text_input(f"{col}")
    
    submit = st.form_submit_button("Save New Work Order")

if submit:
    new_row = pd.DataFrame([new_data])
    new_row['Date of Order'] = new_row['Date of Order'].astype(str)
    
    updated_df = pd.concat([df, new_row], ignore_index=True)
    
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        updated_df.to_excel(writer, sheet_name='Uniform Work Order Tracking', index=False)
    
    st.success("Entry saved successfully!")
    st.rerun()
