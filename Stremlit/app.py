import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="OLA Ride Analytics",
    layout="wide"
)

# Load Data

@st.cache_data
def load_data():
    df = pd.read_csv("ola_rides_cleaned.csv")
    df["booking_datetime"] = pd.to_datetime(df["booking_datetime"])
    return df

df = load_data()

# Header

st.title(" OLA Ride Analytics – Business Insights Dashboard")
st.caption("Data-driven insights using SQL, Power BI, and Streamlit")
st.divider()

# Filters (Sidebar)

st.sidebar.header("🔍 Filters")

# Date filter
start_date = st.sidebar.date_input(
    "Start Date",
    df["booking_datetime"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["booking_datetime"].max().date()
)

# Vehicle filter
vehicle_types = st.sidebar.multiselect(
    "Vehicle Type",
    options=df["vehicle_type"].unique(),
    default=df["vehicle_type"].unique()
)

# Apply filters
filtered_df = df[
    (df["booking_datetime"].dt.date >= start_date) &
    (df["booking_datetime"].dt.date <= end_date) &
    (df["vehicle_type"].isin(vehicle_types))
]

# KPI Section
st.subheader(" Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Rides", len(filtered_df))

with col2:
    st.metric("Total Revenue (₹)", f"{filtered_df['booking_value'].sum():,.0f}")

with col3:
    st.metric("Avg Distance (km)", f"{filtered_df['ride_distance'].mean():.2f}")

with col4:
    st.metric("Avg Rating", f"{filtered_df['customer_rating'].mean():.2f}")

st.divider()

# SQL Output Table

st.subheader(" SQL Output (Filtered Data)")
st.dataframe(filtered_df.head(50), use_container_width=True)

st.divider()

# Power BI Dashboards (Images)

st.subheader(" Power BI Dashboard Insights")

col1, col2 = st.columns(2)

with col1:
    st.image("assets/overview.png", caption="Overall Ride Performance", width=400)
    st.image("assets/vehicle.png", caption="Vehicle Type Analysis", width=400)

with col2:
    st.image("assets/revenue.png", caption="Revenue Insights", width=400)
    st.image("assets/ratings.png", caption="Ratings & Feedback", width=400)

st.divider()

# Time Analysis

st.subheader(" Time-Based Analysis")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("assets/time.png", caption="Hourly / Day-wise Ride Trends", width=600)
st.divider()

# Footer

st.caption(" Built as a presentation layer — SQL for logic, Power BI for visuals, Streamlit for interaction")


# Feedback

st.divider()
st.subheader("Feedback & Suggestions")

with st.form("feedback_form"):
    name = st.text_input("Your Name (optional)")
    feedback = st.text_area("Share your feedback or suggestions")

    submitted = st.form_submit_button("Submit")

    if submitted:
        st.success("Thank you for your feedback! 🙌")