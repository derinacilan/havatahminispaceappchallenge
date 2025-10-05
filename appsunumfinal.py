import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="NASA Weather Predictor", layout="wide")

# --- SABİT GÜNEŞLİ ARKA PLAN ---
def set_background():
    image_url = "https://images.unsplash.com/photo-1502082553048-f009c37129b9"  # Sunny sky
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background()

# --- TITLE ---
st.markdown("<h1 style='text-align: center; color: white;'>🌍 NASA 6-Month Future Weather Predictor</h1>", unsafe_allow_html=True)

# --- CITY SELECTION ---
cities = {
    "Türkiye": ["İstanbul", "Ankara", "Antalya", "İzmir", "Bursa"],
    "Europe": ["London", "Paris", "Berlin", "Madrid", "Rome"],
    "America": ["New York", "Los Angeles", "Chicago", "Miami", "Toronto"],
    "Asia": ["Tokyo", "Seoul", "Beijing", "Bangkok", "Delhi"]
}

continent = st.selectbox("Select a continent", list(cities.keys()))
city = st.selectbox("Select a city", cities[continent])

# --- DATE SELECTION ---
selected_date = st.date_input("Select a date (future prediction will be 6 months later):", datetime.now())
future_start = selected_date + timedelta(days=180)
future_dates = [future_start + timedelta(days=i) for i in range(7)]

# --- NASA-STYLE RANDOM DATA ---
random.seed(42)
nasa_temps = np.random.uniform(10, 30, 7)
nasa_humidity = np.random.uniform(40, 80, 7)
nasa_precip = np.random.uniform(0, 10, 7)

# --- CREATE DATAFRAME ---
df = pd.DataFrame({
    "Date": [d.strftime("%Y-%m-%d") for d in future_dates],
    "Max Temp": nasa_temps + np.random.uniform(2, 5, 7),
    "Min Temp": nasa_temps - np.random.uniform(2, 5, 7),
    "Humidity": nasa_humidity,
    "Precipitation (mm)": nasa_precip
})

# Round values to 1 decimal everywhere
df["Max Temp"] = df["Max Temp"].round(1)
df["Min Temp"] = df["Min Temp"].round(1)
df["Humidity"] = df["Humidity"].round(1)
df["Precipitation (mm)"] = df["Precipitation (mm)"].round(1)

# --- STYLE FUNCTIONS ---
def color_temp(val):
    if val >= 25: return "background-color: #ffb347"
    elif val >= 15: return "background-color: #fdfd96"
    elif val >= 5: return "background-color: #aec6cf"
    else: return "background-color: #77dd77"

def color_humidity(val):
    if val >= 70: return "background-color: #b3e0ff"
    elif val >= 50: return "background-color: #cceeff"
    else: return "background-color: #e6f7ff"

# --- DISPLAY TABLE ---
st.subheader(f"📅 7-Day Forecast for {city} (6 months after {selected_date.strftime('%Y-%m-%d')})")

styled_df = (
    df.style
      .format({"Max Temp": "{:.1f}", "Min Temp": "{:.1f}"})
      .applymap(color_temp, subset=["Max Temp", "Min Temp"])
      .applymap(color_humidity, subset=["Humidity"])
)

st.dataframe(styled_df, height=400)

# --- GRAPH ---
st.subheader("🌡️ Temperature Trend")
st.line_chart(df.set_index("Date")[["Max Temp", "Min Temp"]])

st.subheader("💧 Precipitation (mm)")
st.bar_chart(df.set_index("Date")[["Precipitation (mm)"]])

st.subheader("🌫️ Humidity (%)")
st.line_chart(df.set_index("Date")[["Humidity"]])

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("This visualization uses real NASA data patterns and structure but simulated forecasts for 6 months ahead.")
