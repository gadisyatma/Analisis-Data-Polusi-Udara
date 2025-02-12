import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
from streamlit_folium import folium_static

st.set_page_config(layout="wide")

# Judul Dashboard
st.title("Analisis Polusi Udara di Stasiun Dingling")

# Membaca file CSV
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned.csv")
    if {'year', 'month', 'day', 'hour'}.issubset(df.columns):
        df["datetime"] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df["Rain_Status"] = df["RAIN"].apply(lambda x: "Hujan" if x > 0 else "Tidak Hujan")
    return df

dingling_df = load_data()

# Sidebar untuk filter data
st.sidebar.header("Filter Data")
pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
selected_pollutant = st.sidebar.selectbox("Pilih Polutan", pollutants)

# Hubungan Suhu & Tekanan dengan Polusi
st.subheader("1. Hubungan Suhu & Tekanan dengan Polusi")
fig, ax = plt.subplots()
sns.scatterplot(x=dingling_df["TEMP"], y=dingling_df[selected_pollutant], alpha=0.5, ax=ax)
ax.set_xlabel("Suhu Udara (TEMP)")
ax.set_ylabel(f"Kadar {selected_pollutant}")
ax.set_title("Hubungan Suhu dengan Polusi")
st.pyplot(fig)

fig, ax = plt.subplots()
sns.scatterplot(x=dingling_df["PRES"], y=dingling_df[selected_pollutant], alpha=0.5, ax=ax)
ax.set_xlabel("Tekanan Udara (PRES)")
ax.set_ylabel(f"Kadar {selected_pollutant}")
ax.set_title("Hubungan Tekanan dengan Polusi")
st.pyplot(fig)

# Dampak Curah Hujan terhadap Polusi
st.subheader("2. Dampak Curah Hujan terhadap Polusi")
fig, ax = plt.subplots()
sns.boxplot(x=dingling_df["Rain_Status"], y=dingling_df[selected_pollutant], ax=ax)
ax.set_xlabel("Kondisi Hujan")
ax.set_ylabel(f"Kadar {selected_pollutant}")
ax.set_title(f"Distribusi {selected_pollutant} Berdasarkan Curah Hujan")
st.pyplot(fig)

# Variasi Polusi Berdasarkan Jam
st.subheader("3. Variasi Polusi Berdasarkan Jam dalam Sehari")
hourly_avg = dingling_df.groupby("hour")[pollutants].mean()
fig, ax = plt.subplots()
sns.lineplot(data=hourly_avg, ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Kadar Polusi (Rata-rata)")
ax.set_title("Variasi Tingkat Polusi Udara Berdasarkan Jam dalam Sehari")
st.pyplot(fig)

# RFM Analysis untuk Polusi Udara
st.subheader("4. Analisis RFM untuk Polusi Udara")
rfm_data = dingling_df.groupby("datetime")[selected_pollutant].agg(["max", "count", "mean"])
rfm_data.columns = ["Recency", "Frequency", "Monetary"]
st.dataframe(rfm_data)

# Geospatial Analysis jika ada data lokasi
if "latitude" in dingling_df.columns and "longitude" in dingling_df.columns:
    st.subheader("5. Analisis Geospasial Polusi Udara")
    m = folium.Map(location=[dingling_df["latitude"].mean(), dingling_df["longitude"].mean()], zoom_start=10)
    for _, row in dingling_df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=5,
            color="red" if row[selected_pollutant] > dingling_df[selected_pollutant].median() else "green",
            fill=True,
            fill_color="red" if row[selected_pollutant] > dingling_df[selected_pollutant].median() else "green"
        ).add_to(m)
    folium_static(m)

# Clustering dengan Binning
st.subheader("6. Clustering dengan Binning")
dingling_df["Polusi_Level"] = pd.cut(dingling_df[selected_pollutant], bins=3, labels=["Rendah", "Sedang", "Tinggi"])
st.dataframe(dingling_df[["datetime", selected_pollutant, "Polusi_Level"]].head())
