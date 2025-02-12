import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
    return df.dropna(subset=["TEMP", "PRES", "RAIN"])

dingling_df = load_data()

# Sidebar untuk filter data
st.sidebar.header("Filter Data")
pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
selected_pollutant = st.sidebar.selectbox("Pilih Polutan", pollutants)

# Slider untuk rentang suhu dan tekanan
min_temp, max_temp = st.sidebar.slider("Pilih Rentang Suhu (TEMP)", int(dingling_df["TEMP"].min()), int(dingling_df["TEMP"].max()), (int(dingling_df["TEMP"].min()), int(dingling_df["TEMP"].max())))
min_pres, max_pres = st.sidebar.slider("Pilih Rentang Tekanan Udara (PRES)", int(dingling_df["PRES"].min()), int(dingling_df["PRES"].max()), (int(dingling_df["PRES"].min()), int(dingling_df["PRES"].max())))

filtered_df = dingling_df[(dingling_df["TEMP"] >= min_temp) & (dingling_df["TEMP"] <= max_temp) & (dingling_df["PRES"] >= min_pres) & (dingling_df["PRES"] <= max_pres)]

# Hubungan Suhu & Tekanan dengan Polusi
st.subheader("1. Hubungan Suhu & Tekanan dengan Polusi")
fig, ax = plt.subplots()
sns.scatterplot(x=filtered_df["TEMP"], y=filtered_df[selected_pollutant], alpha=0.5, ax=ax)
ax.set_xlabel("Suhu Udara (TEMP)")
ax.set_ylabel(f"Kadar {selected_pollutant}")
ax.set_title("Hubungan Suhu dengan Polusi")
ax.grid(True)
st.pyplot(fig)

fig, ax = plt.subplots()
sns.scatterplot(x=filtered_df["PRES"], y=filtered_df[selected_pollutant], alpha=0.5, ax=ax)
ax.set_xlabel("Tekanan Udara (PRES)")
ax.set_ylabel(f"Kadar {selected_pollutant}")
ax.set_title("Hubungan Tekanan dengan Polusi")
ax.grid(True)
st.pyplot(fig)

# Dampak Curah Hujan terhadap Polusi
st.subheader("2. Dampak Curah Hujan terhadap Polusi")
fig, ax = plt.subplots()
sns.boxplot(x=filtered_df["Rain_Status"], y=filtered_df[selected_pollutant], ax=ax)
ax.set_xlabel("Kondisi Hujan")
ax.set_ylabel(f"Kadar {selected_pollutant}")
ax.set_title(f"Distribusi {selected_pollutant} Berdasarkan Curah Hujan")
ax.grid(True)
st.pyplot(fig)

# Variasi Polusi Berdasarkan Jam
st.subheader("3. Variasi Polusi Berdasarkan Jam dalam Sehari")
hourly_avg = filtered_df.groupby("hour")[pollutants].mean()
fig, ax = plt.subplots()
sns.lineplot(data=hourly_avg, ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Kadar Polusi (Rata-rata)")
ax.set_title("Variasi Tingkat Polusi Udara Berdasarkan Jam dalam Sehari")
ax.grid(True)
st.pyplot(fig)

# Clustering dengan Binning
st.subheader("4. Clustering dengan Binning")
filtered_df["Polusi_Level"] = pd.cut(filtered_df[selected_pollutant], bins=3, labels=["Rendah", "Sedang", "Tinggi"])
st.write("Kategori polusi berdasarkan binning:")
st.dataframe(filtered_df[["datetime", selected_pollutant, "Polusi_Level"].head()])
