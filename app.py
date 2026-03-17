import streamlit as st
import pandas as pd
import plotly.express as px


# Page Configuration


st.set_page_config(
page_title="Customer Segmentation Dashboard",
page_icon="📊",
layout="wide"
)


# Load Data


df = pd.read_csv("data/customer_segments.csv") 

# Title


st.title("📊 Customer Segmentation Dashboard")

st.write(
"""
This dashboard analyzes customer purchasing behavior using **RFM analysis**
(Recency, Frequency, Monetary) and **K-Means clustering** to identify
different customer segments.
"""
)


# KPI Metrics


st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
"Total Customers",
f"{len(df):,}"
)

col2.metric(
"Average Recency (Days)",
round(df["Recency"].mean(),1)
)

col3.metric(
"Average Spending ($)",
f"{round(df['Monetary'].mean(),2):,}"
)


# Sidebar Filters


st.sidebar.header("Customer Filters")

segment_filter = st.sidebar.multiselect(
"Select Customer Segment",
options=df["Segment"].unique(),
default=df["Segment"].unique()
)

filtered_df = df[df["Segment"].isin(segment_filter)]


# Segment Distribution


st.subheader("Customer Segment Distribution")

segment_counts = filtered_df["Segment"].value_counts().reset_index()
segment_counts.columns = ["Segment","Customers"]

fig1 = px.bar(
segment_counts,
x="Segment",
y="Customers",
color="Segment",
title="Customer Segment Distribution",
color_discrete_sequence=px.colors.qualitative.Set2
)

st.plotly_chart(fig1, use_container_width=True)


# Revenue by Segment


st.subheader("Revenue by Customer Segment")

revenue_segment = filtered_df.groupby("Segment")["Monetary"].sum().reset_index()

fig2 = px.bar(
revenue_segment,
x="Segment",
y="Monetary",
color="Segment",
title="Revenue Contribution by Segment",
color_discrete_sequence=px.colors.qualitative.Bold
)

st.plotly_chart(fig2, use_container_width=True)


# Revenue Share Pie Chart


st.subheader("Revenue Share by Segment")

fig3 = px.pie(
revenue_segment,
values="Monetary",
names="Segment",
title="Revenue Share by Customer Segment",
color_discrete_sequence=px.colors.qualitative.Set3
)

st.plotly_chart(fig3, use_container_width=True)


# Customer Behavior Scatter Plot


st.subheader("Customer Behavior Analysis")

fig4 = px.scatter(
filtered_df,
x="Recency",
y="Monetary",
color="Segment",
size="Frequency",
hover_data=["CustomerID","Frequency"],
title="Customer Behavior (Recency vs Spending)",
color_discrete_sequence=px.colors.qualitative.Bold
)

st.plotly_chart(fig4, use_container_width=True)


# 3D Customer Segmentation


st.subheader("3D Customer Segmentation")

fig5 = px.scatter_3d(
filtered_df,
x="Recency",
y="Frequency",
z="Monetary",
color="Segment",
hover_data=["CustomerID"],
title="3D Customer Segmentation (RFM Analysis)",
color_discrete_sequence=px.colors.qualitative.Bold
)

st.plotly_chart(fig5, use_container_width=True)

st.caption("3D visualization of customer clusters using Recency, Frequency, and Monetary metrics.")


# Top Customers


st.subheader("Top Customers by Spending")

top_customers = filtered_df.sort_values(
by="Monetary",
ascending=False
).head(10)

st.dataframe(top_customers)


# Dataset Preview


st.subheader("Dataset Preview")

st.dataframe(filtered_df.head())


# Download Data


st.download_button(
label="Download Segmented Dataset",
data=filtered_df.to_csv(index=False),
file_name="customer_segments.csv",
mime="text/csv"
)
