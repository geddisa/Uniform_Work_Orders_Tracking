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
    
    cols_to_drop = [c for c in df.columns if "Unnamed" in str(c)]
    df = df.drop(columns=cols_to_drop, errors='ignore')
    
    df = df.dropna(how='all')
    return df

st.title("Uniform Work Order Tracking")

# Define Options
shirt_sizes = ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL", "6XL"]
waists = range(28, 62, 2)
inseams = range(28, 36, 2)
pant_sizes = [f"{w}x{i}" for w in waists for i in inseams]
quantity_options = [0] + list(range(1, 21)) # Added 0 as an option

df = load_and_clean_data()
st.subheader("Current Entries")
st.dataframe(df)

st.subheader("Add New Work Order")

EXCLUDED_FROM_FORM = ['Shirts Order (#)', 'Pants Order (#)']

with st.form("new_entry_form", clear_on_submit=True):
    new_data = {}
    
    # Row 0: Employee Name
    new_data['Employee Name'] = st.text_input("Employee Name")
    
    # Row 1: Date of Order | Workorder Number
    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        new_data['Date of Order'] = st.date_input("Date of Order", value=datetime.now())
    with row1_c2:
        new_data['Workorder Number'] = st.text_input("Workorder Number")
        
    # Row 2: Shirt Size | Pants Size
    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        new_data['Shirt Size'] = st.selectbox("Shirt Size", shirt_sizes, index=None, placeholder="Select Size")
    with row2_c2:
        new_data['Pants Size'] = st.selectbox("Pants Size", pant_sizes, index=None, placeholder="Select Size")
        
    # Row 3: Number of Shirts | Number of Pants
    row3_c1, row3_c2 = st.columns(2)
    with row3_c1:
        # Defaulting to index 0 (which is now "0")
        new_data['Number of Shirts'] = st.selectbox("Number of Shirts", quantity_options, index=0)
    with row3_c2:
        new_data['Number of Pants'] = st.selectbox("Number of Pants", quantity_options, index=0)
        
    # Row 4: Comments
    new_data['Comments'] = st.text_area("Comments")
    
    # Handle remaining columns
    for col in df.columns:
        if col not in new_data and col not in EXCLUDED_FROM_FORM:
            new_data[col] = st.text_input(f"{col}")
    
    submit = st.form_submit_button("Save New Work Order")

if submit:
    # Basic validation: Ensure sizes aren't empty
    if not new_data['Shirt Size'] or not new_data['Pants Size']:
        st.warning("Please select both a Shirt Size and a Pants Size.")
    else:
        new_row = pd.DataFrame([new_data])
        if 'Date of Order' in new_row.columns:
            new_row['Date of Order'] = new_row['Date of Order'].astype(str)
        
        updated_df = pd.concat([df, new_row], ignore_index=True)
        
        with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            updated_df.to_excel(writer, sheet_name='Uniform Work Order Tracking', index=False)
        
        st.success("Entry saved successfully!")
        st.rerun()
