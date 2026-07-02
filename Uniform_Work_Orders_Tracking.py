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
    
    # 1. CLEANING FOR DISPLAY: 
    # Drop unwanted "Unnamed" columns AND the old Order columns so they don't appear in the table
    cols_to_drop = [c for c in df.columns if "Unnamed" in str(c) or c == 'Pants Order (#)']
    display_df = df.drop(columns=cols_to_drop, errors='ignore')
    
    # Drop rows that are entirely empty
    display_df = display_df.dropna(how='all')
    
    return df, display_df

st.title("Uniform Work Order Tracking")

# Define Options for new entries
shirt_sizes = ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL", "6XL"]
waists = range(28, 62, 2)
inseams = range(28, 36, 2)
pant_sizes = [f"{w}x{i}" for w in waists for i in inseams]
quantity_options = list(range(1, 21))

# Get both the full dataframe (for saving) and the clean display version
full_df, display_df = load_and_clean_data()

st.subheader("Current Entries")
st.dataframe(display_df)

# Automate data entry form
st.subheader("Add New Work Order")

# List of old columns we want to HIDE from the entry form
EXCLUDED_FROM_FORM = ['Shirts Order (#)', 'Pants Order (#)']

with st.form("new_entry_form", clear_on_submit=True):
    new_data = {}
    cols = st.columns(2)
    
    # 1. Define the specific fields we WANT to see in the form
    form_fields = [
        'Date of Order', 'Shirt Size', 'Pants Size', 
        'Number of Shirts', 'Number of Pants', 'Comments'
    ]
    
    # 2. Add any other existing columns (excluding the old ones we want to hide)
    for col in full_df.columns:
        if col not in form_fields and col not in EXCLUDED_FROM_FORM:
            form_fields.append(col)

    # 3. Create the form inputs
    for i, col in enumerate(form_fields):
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
    if 'Date of Order' in new_row.columns:
        new_row['Date of Order'] = new_row['Date of Order'].astype(str)
    
    updated_df = pd.concat([full_df, new_row], ignore_index=True)
    
    # Save back to Excel
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        updated_df.to_excel(writer, sheet_name='Uniform Work Order Tracking', index=False)
    
    st.success("Entry saved successfully!")
    st.rerun()
