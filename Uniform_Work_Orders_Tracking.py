import streamlit as st
import pandas as pd
import openpyxl
import os

# --- Configuration ---
NEW_ORDERS_SHEET = 'New Entries' 
FILE_PATH = "Aramark (Vestis) Uniform Spreadsheet.xlsx"

# Define options
NUM_OPTIONS = list(range(1, 21))
PANTS_SIZE_OPTIONS = [
    '23X30', '26X30', '28X30', '28X32', '30X30', '30X32', '30X34', '30X36', 
    '32X30', '32X32', '32X34', '32X36', '34X28', '34X30', '34X32', '34X34', 
    '34X36', '36X28', '36X30', '36X32', '36X34', '38X28', '38X30', '38X32', 
    '38X34', '38X36', '38X38', '40X28', '40X30', '40X31', '40X32', '40X34', 
    '40X36', '42X28', '42X30', '42X32', '42X33', '42X34', '42X36', '42X40', 
    '44X30', '44X32', '44X34', '44X36', '46X30', '46X32', '46X34', '48X28', 
    '48X30', '48X31', '48X32', '48X34', '50X30', '50X32', '50X34', '52X32', 
    '52X34', '56X32'
]
SHIRT_SIZE_OPTIONS = [
    "SM", "MED", "MEDL", "LG", "LGER", 
    "1XLR", "2XLR", "3XLR", "4XLR", "5XLR", "6XLR", 
    "1XLL", "2XLL", "3XLL", "4XLL", "5XLL", "6XLL"
]

st.set_page_config(page_title="Uniform Entry", layout="wide")
st.title("New Uniform Work Orders")

# --- Input Form ---
with st.form("new_order_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        employee_name = st.text_input("Employee Name")
        date_of_order = st.date_input("Date of Order")
        workorder_number = st.text_input("Workorder Number")
        
    with col2:
        num_pants = st.selectbox("Number of Pants", NUM_OPTIONS, index=None, placeholder="Choose...")
        pants_sizes = st.selectbox("Pants Sizes", PANTS_SIZE_OPTIONS, index=None, placeholder="Choose...")
        num_shirts = st.selectbox("Number of Shirts", NUM_OPTIONS, index=None, placeholder="Choose...")
        shirt_sizes = st.selectbox("Shirt Sizes", SHIRT_SIZE_OPTIONS, index=None, placeholder="Choose...")
    
    comments = st.text_area("Comments")
    submitted = st.form_submit_button("Save New Work Order")

    if submitted:
        if not employee_name or not workorder_number:
            st.error("Employee Name and Workorder Number are required.")
        else:
            new_data = {
                "Employee Name": [employee_name],
                "Date of Order": [date_of_order.strftime('%Y-%m-%d')],
                "Number of Pants": [num_pants],
                "Pants Sizes": [pants_sizes],
                "Number of Shirts": [num_shirts],
                "Shirt Sizes": [shirt_sizes],
                "Workorder Number": [workorder_number],
                "Comments": [comments]
            }
            
            try:
                # Load existing or create new sheet
                if not os.path.exists(FILE_PATH):
                    df_new = pd.DataFrame(new_data)
                else:
                    try:
                        df_new = pd.read_excel(FILE_PATH, sheet_name=NEW_ORDERS_SHEET)
                        df_new = pd.concat([df_new, pd.DataFrame(new_data)], ignore_index=True)
                    except:
                        df_new = pd.DataFrame(new_data)

                # Save to Excel
                with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    df_new.to_excel(writer, sheet_name=NEW_ORDERS_SHEET, index=False)
                
                st.success("Entry saved to 'New Entries' sheet!")
                st.rerun()
            except PermissionError:
                st.error("Permission Denied: Please close the Excel file.")
            except Exception as e:
                st.error(f"Error: {e}")

# --- Display Pending Entries ---
st.divider()
st.subheader("Pending New Orders")

try:
    df_view = pd.read_excel(FILE_PATH, sheet_name=NEW_ORDERS_SHEET)
    
    # Action Buttons
    col_a, col_b = st.columns([1, 5])
    with col_a:
        if st.button("📋 Copy All"):
            # header=False prevents the column names from being copied
            df_view.to_clipboard(index=False, header=False)
            st.success("Data copied to clipboard!")
            
    with col_b:
        if st.button("Clear All Entries"):
            # Overwrites the sheet with an empty dataframe containing only headers
            empty_df = pd.DataFrame(columns=df_view.columns)
            with pd.ExcelWriter(FILE_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                empty_df.to_excel(writer, sheet_name=NEW_ORDERS_SHEET, index=False)
            st.rerun()

    st.dataframe(df_view, use_container_width=True)

except Exception:
    st.info("No new entries pending.")
