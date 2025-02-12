import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Membaca file CSV
dingling_df = pd.read_csv("cleaned.csv")
if {'year', 'month', 'day', 'hour'}.issubset(dingling_df.columns):
    dingling_df["datetime"] = pd.to_datetime(dingling_df[['year', 'month', 'day', 'hour']])
dingling_df["Rain_Status"] = dingling_df["RAIN"].apply(lambda x: "Hujan" if x > 0 else "Tidak Hujan")
dingling_df = dingling_df.dropna(subset=["TEMP", "PRES", "RAIN"])

st.title("Analisis Polusi Udara di Stasiun Dingling")

st.header("1. Hubungan Suhu & Tekanan dengan Polusi")

fig, ax = plt.subplots()
sns.scatterplot(x=dingling_df["TEMP"], y=dingling_df["PM2.5"], alpha=0.5, ax=ax)
ax.set_xlabel("Suhu Udara (TEMP)")
ax.set_ylabel("Kadar PM2.5")
ax.set_title("Hubungan Suhu dengan PM2.5")
st.pyplot(fig)

st.subheader("Heatmap Korelasi")
fig, ax = plt.subplots()
corr = dingling_df[["TEMP", "PRES", "PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.write("Dari scatter plot dan heatmap, terlihat hubungan antara suhu, tekanan, dan polusi udara.")

st.header("2. Dampak Curah Hujan terhadap Polusi")

fig, ax = plt.subplots()
sns.boxplot(x=dingling_df["Rain_Status"], y=dingling_df["PM2.5"], ax=ax)
ax.set_xlabel("Kondisi Hujan")
ax.set_ylabel("Kadar PM2.5")
ax.set_title("Distribusi PM2.5 Berdasarkan Curah Hujan")
st.pyplot(fig)

st.header("3. Variasi Polusi Berdasarkan Jam dalam Sehari")

dingling_hourly_avg = dingling_df.groupby("hour")[["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]].mean()
fig, ax = plt.subplots()
sns.lineplot(data=dingling_hourly_avg, ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Kadar Polusi (Rata-rata)")
ax.set_title("Variasi Tingkat Polusi Udara Berdasarkan Jam dalam Sehari")
st.pyplot(fig)
