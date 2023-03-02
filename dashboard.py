import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Menyiapkan berbagai dataframe
def create_monthly_orders_df(df):
    monthly_orders_df = df.resample(rule='M', on='order_date').agg({
        "order_id": "nunique",
        "total_price": "sum"
    })
    monthly_orders_df.index = monthly_orders_df.index.strftime('%B') #mengubah format order date menjadi Tahun-Bulan
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_id": "order_count",
        "total_price": "revenue"
    }, inplace=True)
    
    return monthly_orders_df

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_name").quantity_x.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_bygeder_df(df):
    bygeder_df = df.groupby(by="gender").customer_id.nunique().reset_index()
    bygeder_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bygeder_df

def create_byage_df(df):
    byage_df = df.groupby(by="age_group").customer_id.nunique().reset_index()
    byage_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    byage_df['age_group'] = pd.Categorical(byage_df['age_group'], ["Youth", "Adults", "Seniors"])
    
    return byage_df

def create_bystate_df(df):
    bystate_df = df.groupby(by="state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bystate_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_date": "max", #mengambil tanggal order terakhir
        "order_id": "nunique",
        "total_price": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_date"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    
    return rfm_df

# Gathering cleaned data
all_df = pd.read_csv("all_data.csv")

datetime_columns = ["order_date", "delivery_date"]

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["order_date"].min()
max_date = all_df["order_date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://dicoding-web-img.sgp1.cdn.digitaloceanspaces.com/original/academy/dos:9d27eba5070ed41d56b8636af3248fb920230220172737.jpeg")
    
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )



