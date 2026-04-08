import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Page Layout
st.set_page_config(page_title="Vinci Property Payment Scheduler", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏢 Vinci Payment Scheduler Pro")
st.divider()

# Input Columns
col_in1, col_in2, col_in3 = st.columns(3)

with col_in1:
    katha = st.number_input("Total Jomir Poriman (Katha)", min_value=0.1, value=3.0, step=0.1)
    rate = st.number_input("Per Kathar Rate (BDT)", min_value=1000, value=500000, step=1000)

with col_in2:
    booking = st.number_input("Booking Money Paid (BDT)", min_value=0, value=50000)
    duration = st.selectbox("Duration Plan (Years)", [3, 5, 7, 10])

with col_in3:
    start_date = st.date_input("Schedule Start Date", datetime.now())

# --- Logic Section ---
total_price = katha * rate
down_payment_total = total_price * 0.20
rest_amount = total_price - down_payment_total

# Extra Charge Logic (Yearly based)
extra_rates = {3: 25000, 5: 50000, 7: 75000, 10: 100000}
total_extra = extra_rates[duration] * katha
final_payable = rest_amount + total_extra
total_months = duration * 12
monthly_installment = final_payable / total_months

# --- Summary Display ---
st.subheader("📌 Billing Summary")
s_col1, s_col2, s_col3, s_col4 = st.columns(4)

s_col1.metric("Total Price", f"{total_price:,.0f} ৳")
s_col2.metric("Down Payment (20%)", f"{down_payment_total:,.0f} ৳")
s_col3.metric("Extra Charge", f"{total_extra:,.0f} ৳")
s_col4.metric("Monthly Pay", f"{monthly_installment:,.0f} ৳", delta_color="inverse")

st.divider()

# --- Schedule Generation ---
st.subheader("📅 Monthly Payment List")
schedule_data = []

for i in range(1, total_months + 1):
    due_date = start_date + relativedelta(months=i-1)
    schedule_data.append({
        "Installment": f"Month {i}",
        "Due Date": due_date.strftime("%d-%b-%Y"),
        "Amount (BDT)": f"{monthly_installment:,.2f}",
        "Status": "Pending"
    })

df = pd.DataFrame(schedule_data)
st.dataframe(df, use_container_width=True, height=400)

# Export Option
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Schedule as Excel/CSV",
    data=csv,
    file_name=f"Payment_Schedule_{datetime.now().strftime('%Y%m%d')}.csv",
    mime='text/csv',
)