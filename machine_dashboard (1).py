import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os

DATA_DIR = "uploaded_data"
os.makedirs(DATA_DIR, exist_ok=True)

st.title("📊 Machine Cost Dashboard")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
if uploaded_file:
    file_path = os.path.join(DATA_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Uploaded and saved: {uploaded_file.name}")

excel_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".xlsx")]
all_data = pd.DataFrame()

for file in excel_files:
    file_path = os.path.join(DATA_DIR, file)
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        df["Source File"] = file
        all_data = pd.concat([all_data, df], ignore_index=True)
    except Exception as e:
        st.error(f"Error reading {file}: {e}")

if not all_data.empty:
    st.subheader("📄 Raw Data")
    st.dataframe(all_data)

    if "Supplier" in all_data.columns and "Cost" in all_data.columns:
        st.subheader("💰 Total Cost per Supplier")
        supplier_costs = all_data.groupby("Supplier")["Cost"].sum().sort_values()
        st.bar_chart(supplier_costs)

    if "Machine" in all_data.columns and "Cost" in all_data.columns:
        st.subheader("⚙️ Average Cost per Machine")
        machine_avg_cost = all_data.groupby("Machine")["Cost"].mean().sort_values()
        st.bar_chart(machine_avg_cost)

    if "Date" in all_data.columns and "Cost" in all_data.columns:
        st.subheader("📅 Cost Over Time")
        all_data["Date"] = pd.to_datetime(all_data["Date"], errors="coerce")
        time_series = all_data.groupby("Date")["Cost"].sum().dropna()
        st.line_chart(time_series)
