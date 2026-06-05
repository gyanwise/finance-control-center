import streamlit as st
import pandas as pd
from datetime import date
import os

# ==========================================
# PAGE CONFIG & HIGH-TECH UI STYLING
# ==========================================
st.set_page_config(page_title="FINANCIAL CONTROL CENTER", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for a High-Tech / Cyberpunk Corporate Dark Mode
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0b0f19;
        color: #00ffcc;
    }
    /* Headers */
    h1, h2, h3 {
        color: #00ffcc !important;
        font-family: 'Courier New', Courier, monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #00ffcc;
    }
    /* Buttons */
    .stButton>button {
        background-color: #00ffcc;
        color: #0b0f19;
        font-weight: bold;
        border-radius: 4px;
        border: 1px solid #00ffcc;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0b0f19;
        color: #00ffcc;
        border: 1px solid #00ffcc;
        box-shadow: 0 0 10px #00ffcc;
    }
    /* Dataframes/Tables */
    .stDataFrame {
        border: 1px solid #1f2937;
        border-radius: 5px;
    }
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        color: #00ffcc !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# DATA MANAGEMENT FUNCTIONS
# ==========================================
def load_data(file_name, columns):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        return pd.DataFrame(columns=columns)

def save_data(file_name, df):
    df.to_csv(file_name, index=False)

# File Paths
FILES = {
    "reg_pay": "Reg_Payments_DB.csv",
    "reg_exp": "Reg_Expenses_DB.csv",
    "kit_pay": "Kit_Payments_DB.csv",
    "kit_exp": "Kit_Expenses_DB.csv"
}

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2096/2096058.png", width=100) # Placeholder High-Tech Icon
st.sidebar.title("SYSTEM MENU")
menu = st.sidebar.radio("Navigation Engine", [
    "Dashboard Analytics", 
    "Enter Registration Payments", 
    "Enter Registration Expenses", 
    "Enter Kit Payments", 
    "Enter Kit Expenses"
])

st.sidebar.markdown("---")
st.sidebar.info("GST Extraction Architecture v2.0")

# ==========================================
# 1. DASHBOARD ANALYTICS
# ==========================================
if menu == "Dashboard Analytics":
    st.title("💠 Main Financial Control Dashboard")
    st.markdown("Live view of cumulative metrics and transaction data.")
    
    # Load all data to compute metrics
    df_rp = load_data(FILES["reg_pay"], [])
    df_re = load_data(FILES["reg_exp"], [])
    df_kp = load_data(FILES["kit_pay"], [])
    df_ke = load_data(FILES["kit_exp"], [])
    
    # Calculate Metrics safely
    tot_reg_income = df_rp['Net Amount (Excl GST)'].sum() if not df_rp.empty else 0
    tot_kit_income = df_kp['Net Amount (Excl GST)'].sum() if not df_kp.empty else 0
    tot_revenue = tot_reg_income + tot_kit_income
    
    tot_reg_gst = df_rp['GST Amount'].sum() if not df_rp.empty else 0
    tot_kit_gst = df_kp['GST Amount'].sum() if not df_kp.empty else 0
    tot_gst = tot_reg_gst + tot_kit_gst
    
    tot_reg_exp = df_re['Amount Paid'].sum() if not df_re.empty else 0
    tot_kit_exp = df_ke['Grand Total Item Cost'].sum() if not df_ke.empty else 0
    tot_exp = tot_reg_exp + tot_kit_exp
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Net Revenue", f"₹ {tot_revenue:,.2f}")
    col2.metric("Total Collected GST", f"₹ {tot_gst:,.2f}")
    col3.metric("Total Expenses", f"₹ {tot_exp:,.2f}")
    col4.metric("Net Profit/Loss", f"₹ {(tot_revenue - tot_exp):,.2f}")

    st.markdown("---")
    st.subheader("Recent Registrations")
    st.dataframe(df_rp.tail(5) if not df_rp.empty else pd.DataFrame(), use_container_width=True)

# ==========================================
# 2. REGISTRATION PAYMENTS ENTRY
# ==========================================
elif menu == "Enter Registration Payments":
    st.title("📥 Registration Payments Entry")
    cols = ['Date', 'Season Tracking', 'Registration ID', 'Participant Name', 'Registration Type', 
            'Gross Amount Received', 'GST %', 'GST Amount', 'Net Amount (Excl GST)', 'Payment Method', 'Status']
    df = load_data(FILES["reg_pay"], cols)
    
    with st.form("reg_pay_form"):
        col1, col2 = st.columns(2)
        r_date = col1.date_input("Date", date.today())
        r_season = col2.text_input("Season Tracking (e.g., SEASON 12)")
        r_id = col1.text_input("Registration ID")
        r_name = col2.text_input("Participant Name")
        r_type = col1.selectbox("Registration Type", ["Standard", "Premium", "Discounted"])
        r_gross = col2.number_input("Gross Amount Received (₹)", min_value=0.0, step=100.0)
        r_gst_pct = col1.selectbox("GST %", [0.05, 0.12, 0.18], index=0)
        r_method = col2.selectbox("Payment Method", ["Bank Transfer", "UPI", "Credit Card", "Cash"])
        r_status = col1.selectbox("Status", ["Completed", "Pending", "Failed"])
        
        submitted = st.form_submit_button("Submit Transaction")
        if submitted:
            gst_amount = r_gross - (r_gross / (1 + r_gst_pct))
            net_amount = r_gross - gst_amount
            
            new_data = pd.DataFrame([[r_date, r_season, r_id, r_name, r_type, r_gross, r_gst_pct, gst_amount, net_amount, r_method, r_status]], columns=cols)
            df = pd.concat([df, new_data], ignore_index=True)
            save_data(FILES["reg_pay"], df)
            st.success("✅ Transaction Logged Successfully!")

# ==========================================
# 3. REGISTRATION EXPENSES ENTRY
# ==========================================
elif menu == "Enter Registration Expenses":
    st.title("📤 Registration Expenses Log")
    cols = ['Date', 'Season Tracking', 'Expense ID', 'Vendor Name', 'Category', 'Description', 'Amount Paid', 'Payment Method']
    df = load_data(FILES["reg_exp"], cols)
    
    with st.form("reg_exp_form"):
        col1, col2 = st.columns(2)
        e_date = col1.date_input("Date", date.today())
        e_season = col2.text_input("Season Tracking")
        e_id = col1.text_input("Expense ID")
        e_vendor = col2.text_input("Vendor Name (e.g., Meta Ads)")
        e_cat = col1.selectbox("Category", ["Marketing", "Operations", "Software", "Misc"])
        e_desc = col2.text_input("Description")
        e_amount = col1.number_input("Amount Paid (₹)", min_value=0.0)
        e_method = col2.selectbox("Payment Method", ["UPI", "Bank Transfer", "Card"])
        
        submitted = st.form_submit_button("Log Expense")
        if submitted:
            new_data = pd.DataFrame([[e_date, e_season, e_id, e_vendor, e_cat, e_desc, e_amount, e_method]], columns=cols)
            df = pd.concat([df, new_data], ignore_index=True)
            save_data(FILES["reg_exp"], df)
            st.success("✅ Expense Logged Successfully!")

# ==========================================
# 4. KIT PAYMENTS ENTRY
# ==========================================
elif menu == "Enter Kit Payments":
    st.title("📦 Kit Payments Inflow")
    cols = ['Date', 'Season Tracking', 'Order ID', 'Buyer Name', 'Kit Type', 'Quantity', 'Price Per Kit', 
            'Total Amount Received', 'GST %', 'GST Amount', 'Net Amount (Excl GST)', 'Status']
    df = load_data(FILES["kit_pay"], cols)
    
    with st.form("kit_pay_form"):
        col1, col2 = st.columns(2)
        k_date = col1.date_input("Date", date.today())
        k_season = col2.text_input("Season Tracking")
        k_order = col1.text_input("Order ID")
        k_buyer = col2.text_input("Buyer Name")
        k_type = col1.text_input("Kit Type")
        k_qty = col2.number_input("Quantity", min_value=1, step=1)
        k_price = col1.number_input("Price Per Kit (₹)", min_value=0.0)
        k_gst_pct = col2.selectbox("GST %", [0.05, 0.12, 0.18], index=0)
        k_status = col1.selectbox("Status", ["Delivered", "Processing", "Shipped"])
        
        submitted = st.form_submit_button("Submit Kit Payment")
        if submitted:
            total_gross = k_qty * k_price
            gst_amount = total_gross - (total_gross / (1 + k_gst_pct))
            net_amount = total_gross - gst_amount
            
            new_data = pd.DataFrame([[k_date, k_season, k_order, k_buyer, k_type, k_qty, k_price, total_gross, k_gst_pct, gst_amount, net_amount, k_status]], columns=cols)
            df = pd.concat([df, new_data], ignore_index=True)
            save_data(FILES["kit_pay"], df)
            st.success("✅ Kit Payment Logged Successfully!")

# ==========================================
# 5. KIT EXPENSES ENTRY
# ==========================================
elif menu == "Enter Kit Expenses":
    st.title("🏭 Kit Expenses Log")
    cols = ['Date', 'Season Tracking', 'Item Name', 'Supplier Name', 'Quantity Purchased', 'Unit Cost', 'Total Raw Cost', 'Shipping / Surcharges', 'Grand Total Item Cost']
    df = load_data(FILES["kit_exp"], cols)
    
    with st.form("kit_exp_form"):
        col1, col2 = st.columns(2)
        ke_date = col1.date_input("Date", date.today())
        ke_season = col2.text_input("Season Tracking")
        ke_item = col1.text_input("Item Name")
        ke_supplier = col2.text_input("Supplier Name")
        ke_qty = col1.number_input("Quantity Purchased", min_value=1)
        ke_cost = col2.number_input("Unit Cost (₹)", min_value=0.0)
        ke_shipping = col1.number_input("Shipping / Surcharges (₹)", min_value=0.0)
        
        submitted = st.form_submit_button("Log Kit Expense")
        if submitted:
            raw_cost = ke_qty * ke_cost
            grand_total = raw_cost + ke_shipping
            
            new_data = pd.DataFrame([[ke_date, ke_season, ke_item, ke_supplier, ke_qty, ke_cost, raw_cost, ke_shipping, grand_total]], columns=cols)
            df = pd.concat([df, new_data], ignore_index=True)
            save_data(FILES["kit_exp"], df)
            st.success("✅ Kit Expense Logged Successfully!")