import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="whitegrid")

# =========================
# CONFIG UI
# =========================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("all_data.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

df.rename(columns={
    "cnt": "total_rentals",
    "weathersit": "weather"
}, inplace=True)

# =========================
# FILTER SIDEBAR
# =========================
min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.title("🔍 Filter Data")

    start_date, end_date = st.date_input(
        "Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df["dteday"] >= pd.to_datetime(start_date)) &
             (df["dteday"] <= pd.to_datetime(end_date))]

if main_df.empty:
    st.error("Data kosong setelah filter!")
    st.stop()

# =========================
# HERO SECTION
# =========================
st.markdown("""
# 🚲 Bike Sharing Analytics Dashboard  
### Insight peminjaman sepeda berdasarkan cuaca, musim, dan waktu
""")

st.divider()

# =========================
# KPI SECTION (MODERN STYLE)
# =========================
st.subheader("📌 Key Performance Indicator")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Rentals", f"{main_df['total_rentals'].sum():,.0f}")

with col2:
    st.metric("Avg Daily", f"{main_df['total_rentals'].mean():.2f}")

with col3:
    st.metric("Max Daily", f"{main_df['total_rentals'].max():,.0f}")

with col4:
    st.metric("Data Points", len(main_df))

st.divider()

# =========================
# TREND SECTION
# =========================
st.subheader("📈 Daily Rental Trend")

daily = main_df.groupby("dteday")["total_rentals"].sum().reset_index()

fig, ax = plt.subplots(figsize=(14,5))
ax.plot(daily["dteday"], daily["total_rentals"], color="#1f77b4", linewidth=2)
ax.set_title("Bike Rentals Over Time")
ax.set_xlabel("")
ax.set_ylabel("Total Rentals")

st.pyplot(fig)

st.divider()

# =========================
# INSIGHT GRID (2 KOLOM)
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌦 Weather Impact")

    weather_df = main_df.groupby("weather")["total_rentals"].mean().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(data=weather_df, x="weather", y="total_rentals", ax=ax)
    ax.set_title("Average Rentals by Weather")
    ax.set_xlabel("")
    ax.set_ylabel("")
    st.pyplot(fig)

with col2:
    st.subheader("🍂 Season Impact")

    season_df = main_df.groupby("season")["total_rentals"].mean().reset_index()

    fig, ax = plt.subplots()
    sns.barplot(data=season_df, x="season", y="total_rentals", ax=ax)
    ax.set_title("Average Rentals by Season")
    ax.set_xlabel("")
    ax.set_ylabel("")
    st.pyplot(fig)

st.divider()

# =========================
# WORKING DAY
# =========================
st.subheader("🏢 Working Day vs Holiday")

work_df = main_df.groupby("workingday")["total_rentals"].mean().reset_index()
work_df["workingday"] = work_df["workingday"].map({
    0: "Holiday",
    1: "Working Day"
})

fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(data=work_df, x="workingday", y="total_rentals", ax=ax)
ax.set_title("Usage Pattern")
st.pyplot(fig)

st.divider()

# =========================
# INSIGHT SECTION
# =========================
st.subheader("💡 Key Insights")

st.info("""
- Cuaca cerah meningkatkan jumlah peminjaman sepeda secara signifikan  
- Musim Summer & Fall adalah periode dengan demand tertinggi  
- Hari kerja menunjukkan pola penggunaan sebagai transportasi utama  
- Faktor lingkungan sangat mempengaruhi keputusan pengguna  
""")

# =========================
# FOOTER
# =========================
st.caption("🚲 Bike Sharing Dashboard | Built with Streamlit")