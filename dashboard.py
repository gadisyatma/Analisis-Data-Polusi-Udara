import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Judul Dashboard
st.title("📊 Dashboard Analisis Polusi Udara")

# Membaca file CSV secara langsung
dingling_df = pd.read_csv("cleaned.csv")

# Pastikan kolom waktu tersedia
if {'year', 'month', 'day', 'hour'}.issubset(dingling_df.columns):
    dingling_df["datetime"] = pd.to_datetime(dingling_df[['year', 'month', 'day', 'hour']])

st.write("### Preview Data")
st.dataframe(dingling_df.head())

# Sidebar filter
st.sidebar.header("Filter Data")

pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
selected_pollutant = st.sidebar.selectbox("Pilih Polutan", pollutants)

# Hubungan antara TEMP, PRES, dan tingkat polusi
st.subheader("Hubungan Suhu & Tekanan dengan Polusi")
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
sns.scatterplot(x=dingling_df["TEMP"], y=dingling_df[selected_pollutant], alpha=0.5, ax=ax[0])
ax[0].set_xlabel("Suhu Udara (TEMP)")
ax[0].set_ylabel(f"Kadar {selected_pollutant}")
ax[0].set_title("Hubungan Suhu dengan Polusi")

sns.scatterplot(x=dingling_df["PRES"], y=dingling_df[selected_pollutant], alpha=0.5, ax=ax[1])
ax[1].set_xlabel("Tekanan Udara (PRES)")
ax[1].set_ylabel(f"Kadar {selected_pollutant}")
ax[1].set_title("Hubungan Tekanan Udara dengan Polusi")
st.pyplot(fig)

# Dampak curah hujan terhadap polusi
st.subheader("Dampak Curah Hujan terhadap Polusi")
dingling_df["Rain_Status"] = dingling_df["RAIN"].apply(lambda x: "Hujan" if x > 0 else "Tidak Hujan")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(x=dingling_df["Rain_Status"], y=dingling_df[selected_pollutant], ax=ax)
ax.set_xlabel("Kondisi Hujan")
ax.set_ylabel(f"Kadar {selected_pollutant}")
ax.set_title(f"Distribusi {selected_pollutant} Berdasarkan Curah Hujan")
st.pyplot(fig)

# Variasi polusi berdasarkan jam dalam sehari
st.subheader("Variasi Polusi Berdasarkan Jam dalam Sehari")
hourly_avg = dingling_df.groupby("hour")[pollutants].mean()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=hourly_avg, ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Kadar Polusi (Rata-rata)")
ax.set_title("Variasi Tingkat Polusi Udara Berdasarkan Jam dalam Sehari")
st.pyplot(fig)

st.success("Analisis data berhasil ditampilkan! 🚀")
