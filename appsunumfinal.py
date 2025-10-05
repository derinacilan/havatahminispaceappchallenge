import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Sayfa Ayarları ---
st.set_page_config(page_title="6 Ay Sonrası Hava Tahmini", layout="centered")

# --- Arka Plan ---
page_bg_img = """
<style>
body {
background-image: url("https://images.unsplash.com/photo-1506744038136-46273834b3fb");
background-size: cover;
background-repeat: no-repeat;
background-attachment: fixed;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("6 Ay Sonrası 7 Günlük Hava Tahmini — NASA Verileri (Tahmini)")

# --- Şehir Seçimi (Farklı ülkeler ve Türkiye’den şehirler) ---
CITIES = [
    "Istanbul, Turkey", "Ankara, Turkey", "Antalya, Turkey", "Izmir, Turkey",
    "London, UK", "Manchester, UK",
    "New York, USA", "Los Angeles, USA", "Chicago, USA",
    "Tokyo, Japan", "Osaka, Japan",
    "Sydney, Australia", "Melbourne, Australia",
    "Paris, France", "Lyon, France"
]
city = st.selectbox("Şehir seçin:", CITIES)

# --- Tarih Seçimi ---
user_date = st.date_input("Tahmin başlangıç tarihi:", datetime.today())

# --- Başlangıç tarihi: kullanıcı seçtiği tarihten 6 ay sonrası ---
fixed_start_date = pd.to_datetime(user_date) + pd.DateOffset(months=6)

# --- Tahmini 7 günlük veri üretimi ---
def generate_fixed_week_data(city, start_date):
    rng = np.random.RandomState(42)
    rows = []
    for i in range(7):
        date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        
        # Baz sıcaklıklar şehir bazlı
        base_temp_dict = {
            "Istanbul, Turkey": 20, "Ankara, Turkey": 18, "Antalya, Turkey": 25, "Izmir, Turkey": 23,
            "London, UK": 10, "Manchester, UK": 9,
            "New York, USA": 15, "Los Angeles, USA": 20, "Chicago, USA": 12,
            "Tokyo, Japan": 18, "Osaka, Japan": 19,
            "Sydney, Australia": 22, "Melbourne, Australia": 20,
            "Paris, France": 12, "Lyon, France": 11
        }
        base_temp = base_temp_dict.get(city, 20)
        temp = base_temp + rng.uniform(-2,2)
        max_temp = temp + rng.uniform(0,2)
        min_temp = temp - rng.uniform(0,2)
        humidity = np.clip(60 + rng.uniform(-15,15), 10, 100)
        precip = max(0.0, rng.normal(loc=2.0 if city in ["Istanbul, Turkey","London, UK","Antalya, Turkey"] else 0.5, scale=2.0))
        wind_speed = np.clip(rng.uniform(0,20), 0, 30)
        pressure = np.clip(1010 + rng.uniform(-10,10), 980, 1050)
        uv_index = np.clip(rng.uniform(0,11),0,11)
        sunny_hours = np.clip(rng.uniform(0,12),0,12)
        feels_like = max_temp - (100-humidity)/5 + wind_speed/5
        
        # Hava durumu ikonları ve açıklama
        if precip > 1.0:
            icon = "🌧 Yağmurlu"
        elif max_temp > 25:
            icon = "☀️ Güneşli"
        else:
            icon = "⛅ Bulutlu"

        rows.append({
            "Date": date,
            "City": city,
            "Max Temp": round(max_temp,1),
            "Min Temp": round(min_temp,1),
            "Feels Like": round(feels_like,1),
            "Humidity": round(humidity,1),
            "Precipitation": round(precip,1),
            "Wind Speed": round(wind_speed,1),
            "Pressure": round(pressure,1),
            "UV Index": round(uv_index,1),
            "Sunny Hours": round(sunny_hours,1),
            "Weather": icon,
            "Source": "NASA Verileri"
        })
    return pd.DataFrame(rows)

df = generate_fixed_week_data(city, fixed_start_date)

# --- Renkli tablo ---
def color_temp(val):
    if val >= 25:
        return 'background-color: #FF9999'
    elif val <= 15:
        return 'background-color: #99CCFF'
    else:
        return ''

def color_humidity(val):
    if val >= 80:
        return 'background-color: #99FF99'
    else:
        return ''

st.subheader(f"{city} — 7 Günlük Tahmini Veriler ({fixed_start_date.strftime('%Y-%m-%d')})")
styled_df = df.style.applymap(color_temp, subset=['Max Temp','Min Temp']).applymap(color_humidity, subset=['Humidity'])
st.dataframe(styled_df, height=400)

# --- Özet Kartları ---
st.subheader("Haftalık Özet Kartları")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ortalama Sıcaklık (°C)", f"{df[['Max Temp','Min Temp']].mean().mean():.1f}")
col2.metric("Ortalama Nem (%)", f"{df['Humidity'].mean():.1f}")
col3.metric("Toplam Yağış (mm)", f"{df['Precipitation'].sum():.1f}")
col4.metric("Ortalama UV İndeksi", f"{df['UV Index'].mean():.1f}")

# --- Grafikler ---
st.subheader("Sıcaklık, Nem ve Feels Like")
st.line_chart(df.set_index("Date")[["Max Temp","Min Temp","Humidity","Feels Like"]])

st.subheader("Yağış")
st.bar_chart(df.set_index("Date")[["Precipitation"]])


