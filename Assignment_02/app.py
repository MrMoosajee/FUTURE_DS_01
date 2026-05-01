import streamlit as st
from analysis import load_and_clean_data, get_churn_metrics, plot_churn_by_contract, plot_tenure_vs_churn, plot_payment_method_churn

# Page Config
st.set_page_config(page_title="Customer Retention Dashboard", layout="wide")

# Load Data
try:
    df = load_and_clean_data('WA_Fn-UseC_-Telco-Customer-Churn.csv')
except FileNotFoundError:
    st.error("Dataset not found. Please ensure the CSV is in the folder.")
    st.stop()

# Sidebar Filters
st.sidebar.header("Filter Data")
gender = st.sidebar.multiselect("Gender", options=df['gender'].unique(), default=df['gender'].unique())
contract = st.sidebar.multiselect("Contract Type", options=df['Contract'].unique(), default=df['Contract'].unique())

filtered_df = df[(df['gender'].isin(gender)) & (df['Contract'].isin(contract))]

# Dashboard Header
st.title("📊 Customer Retention & Churn Analysis")
st.markdown("Developed for Future Interns Data Science Internship - Task 2")

# High Level Metrics
total_cust, churn_count, churn_rate = get_churn_metrics(filtered_df)

col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{total_cust}")
col2.metric("Churned Customers", f"{churn_count}")
col3.metric("Churn Rate", f"{churn_rate:.2f}%")

st.divider()

# Visualization Row 1
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.plotly_chart(plot_churn_by_contract(filtered_df), use_container_width=True)

with row1_col2:
    st.plotly_chart(plot_tenure_vs_churn(filtered_df), use_container_width=True)

# Visualization Row 2
st.plotly_chart(plot_payment_method_churn(filtered_df), use_container_width=True)

# Business Insights Section
st.divider()
st.header("💡 Business Insights & Recommendations")

with st.expander("See Key Findings"):
    st.write("""
    1. **Contract Risk:** Customers on **Month-to-month** contracts have the highest churn rate. Incentivizing annual plans could improve retention.
    2. **Tenure Patterns:** Churn is highest in the first 6 months. A dedicated 'Onboarding' retention program is recommended.
    3. **Payment Friction:** Electronic checks show a higher correlation with churn compared to automatic credit card payments.
    """)

st.success("Analysis Complete.")
