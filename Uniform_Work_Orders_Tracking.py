import streamlit as st
import requests

# Configuration
# Note: Since we are using Power Automate, we no longer need the local file path
WEBHOOK_URL = "https://86c709e36af6e04d916240275e24f8.0b.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/7426183ceca2431d81c6a82e6a11dc85/triggers/manual/paths/invoke?api-version=1"

st.set_page_config(page_title="Uniform Work Order Tracking", layout="centered")

# Add your logo
# if os.path.exists("CENX_BIG-c7dd3883.png"):
#     st.logo("CENX_BIG-c7dd3883.png")

st.title("Uniform Work Order Tracking")

# --- Form Section ---
with st.form("new_order_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    # Options
    num_options = list(range(1, 21)) 
    pants_size_options = [
        '23X30', '26X30', '28X30', '28X32', '30X30', '30X32', '30X34', '30X36', 
        '32X30', '32X32', '32X34', '32X36', '34X28', '34X30', '34X32', '34X34', 
        '34X36', '36X28', '36X30', '36X32', '36X34', '38X28', '38X30', '38X32', 
        '38X34', '38X36', '38X38', '40X28', '40X30', '40X31', '40X32', '40X34', 
        '40X36', '42X28', '42X30', '42X32', '42X33', '42X34', '42X36', '42X40', 
        '44X30', '44X32', '44X34', '44X36', '46X30', '46X32', '46X34', '48X28', 
        '48X30', '48X31', '48X32', '48X34', '50X30', '50X32', '50X34', '52X32', 
        '52X34', '56X32'
    ]
    shirt_size_options = [
        "SM", "MED", "MEDL", "LG", "LGER", 
        "1XLR", "2XLR", "3XLR", "4XLR", "5XLR", "6XLR", 
        "1XLL", "2XLL", "3XLL", "4XLL", "5XLL", "6XLL"
    ]

    with col1:
        employee_name = st.text_input("Employee Name")
        date_of_order = st.date_input("Date of Order")
        workorder_number = st.text_input("Workorder Number")
        
    with col2:
        num_pants = st.selectbox("Select Number of Pants", num_options, index=None, placeholder="Choose an option...")
        pants_sizes = st.selectbox("Select Pants Sizes", pants_size_options, index=None, placeholder="Choose an option...")
        num_shirts = st.selectbox("Number of Shirts", num_options, index=None, placeholder="Choose an option...")
        shirt_sizes = st.selectbox("Shirt Sizes", shirt_size_options, index=None, placeholder="Choose an option...")
    
    comments = st.text_area("Comments")
    submitted = st.form_submit_button("Save New Work Order")

    if submitted:
        # Construct the payload
        data = {
            "employee_name": employee_name,
            "date": date_of_order.strftime('%Y-%m-%d'),
            "pants_qty": num_pants,
            "pants_size": pants_sizes,
            "shirt_qty": num_shirts,
            "shirt_size": shirt_sizes,
            "workorder": workorder_number,
            "comments": comments
        }
        
        try:
            # Send the data to your Power Automate flow
            response = requests.post(WEBHOOK_URL, json=data)
            
            if response.status_code in [200, 202]:
                st.success("Work order saved successfully to SharePoint!")
            else:
                st.error(f"Failed to save. Status code: {response.status_code}")
                
        except Exception as e:
            st.error(f"Error connecting to SharePoint: {e}")