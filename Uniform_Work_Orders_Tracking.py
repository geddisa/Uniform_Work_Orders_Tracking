import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime

# File path
FILE_PATH = 'Aramark (Vestis) Uniform Spreadsheet.xlsx'

def migrate_old_data(df):
    """Parses old columns and populates new ones."""
    # Migrate Pants: Expects format like "34x32 (5)"
    if "Pants Order(#)" in df.columns:
        def parse_pants(val):
            val = str(val)
            size_match = re.search(r'(\d+x\d+)', val, re.IGNORECASE)
            num_match = re.search(r'\((\d+)\)', val)
            size = size_match.group(1) if size_match else ""
            num = num_match.group(1) if num_match else 1
            return size, num
        
        parsed = df["Pants Order(#)"].apply(lambda x: pd.Series(parse_pants(x)))
        df['Pants Size'] = parsed[0]
        df['Number of Pants'] = parsed[1]

    # Migrate Shirts: Expects format like "XL (2)"
    if "Shirts Order (#)" in df.columns:
        def parse_shirts(val):
            val = str(val)
            size_match = re.search(r'^([A-Za-z0-9]+)', val)
            num_match = re.search(r'\((\d+)\)', val)
            size = size_match.group(1) if size_match else ""
            num = num_match.group(1) if num_match else 1
            return size, num
        
        parsed = df["Shirts Order (#)"].apply(lambda x: pd.Series(parse_shirts(x)))
        df['Shirt Size'] = parsed[0]
        df['Number of Shirts'] = parsed[1]

    return df

def load_and_clean_data():
    if not os.path.exists(FILE_PATH):
        st.error(f"File '{FILE_PATH}' not found!")
        return pd.DataFrame()
    
    df = pd.read_excel(FILE_PATH, sheet_name='Uniform Work Order Tracking')
    
    # 1. Run migration if old columns exist
    df = migrate_old_data(df)
    
    # 2. Drop the old columns and "Unnamed" columns
    cols_to_drop = [c for c in df.columns if "Unnamed" in str(c) or "Order(#)" in str(c) or "Order (#)" in str(c)]
    df = df.drop(columns=cols_to_drop, errors='ignore')
    
    # 3. Ensure necessary columns exist for the form
    for col in ['Comments', 'Number of Pants', 'Number of Shirts', 'Shirt Size', 'Pants Size']:
        if col not in df.columns:
            df[col] = ""
            
    df = df.dropna(how='all')
    return df

st.title("Uniform Work Order Tracking")

# Define Options
shirt_sizes = ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL", "6XL"]
waists = range(28, 62, 2)
inseams = range(28, 36, 2)
pant_sizes = [f"{w}x{i}" for w in waists for i in inseams]
quantity_options = list(range(1, 21))

df = load_and_clean_data()
st.subheader("Current Entries")
st.dataframe(df)

# Automate data entry form
st.subheader("Add New Work Order")
with st.form("new_entry_form", clear_on_submit=True):
    new_data = {}
    cols = st.columns(2)
    
    for i, col in enumerate(df.columns):
        with cols[i % 2]:
            if col == 'Date of Order':
                new_data[col] = st.date_input(f"{col}", value=datetime.now())
            elif col == 'Comments':
                new_data[col] = st.text_area("Comments")
            elif col == 'Shirt Size':
                new_data[col] = st.selectbox("Shirt Size", shirt_sizes)
            elif col == 'Pants Size':
                new_data[col] = st.selectbox("Pants Size", pant_sizes)
            elif col == 'Number of Shirts':
                new_data[col] = st.selectbox("Number of Shirts", quantity_options)
            elif col == 'Number of Pants':
                new_data[col] = st.selectbox("Number of Pants", quantity_options)
            else:
                new_data[col] = st.text_input(f"{col}")
    
    submit = st.form_submit_button("Save New Work Order")

if submit:
    new_row = pd.DataFrame([new_data])
    new_row['Date of Order'] = new_row['Date of Order'].astype(str)
    
    updated_df = pd.concat([df, new_row], ignore_index=True)
    
    # Save back to Excel
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        updated_df.to_excel(writer, sheet_name='Uniform Work Order Tracking', index=False)
    
    st.success("Entry saved successfully!")
    st.rerun()
