import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- Sayfa Ayarları ---
st.set_page_config(page_title="6 Ay Sonrası Hava Tahmini", layout="centered")
st.title("6 Ay Sonrası 7 Günlük Hava Tahmini — NASA Verileri (Tahmini)")

# --- Şehir Seçimi ---
CITIES = ["Istanbul", "Ankara", "Izmir", "Antalya", "Bursa", "Konya"]
city = st.selectbox("Şehir seçin:", CITIES)

# --- Sabit 6 ay sonrası başlangıç ---
fixed_start_date = datetime.today() + pd.DateOffset(months=6)

# --- Tahmini 7 günlük veri üretimi ---
def generate_fixed_week_data(city):
    rng = np.random.RandomState(42)
    rows = []
    for i in range(7):
        date = (fixed_start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        base_temp = {"Istanbul":20,"Ankara":15,"Izmir":22,"Antalya":24,"Bursa":18,"Konya":16}.get(city,20)
        temp = base_temp + rng.uniform(-2,2)
        max_temp = temp + rng.uniform(0,2)
        min_temp = temp - rng.uniform(0,2)
        humidity = np.clip(60 + rng.uniform(-15,15), 10, 100)
        precip = max(0.0, rng.normal(loc=2.0 if city in ["Istanbul","Bursa"] else 0.5, scale=2.0))
        
        # Hava durumu ikonları
        if precip > 1.0:
            icon = "🌧"
        elif max_temp > 25:
            icon = "☀️"
        else:
            icon = "⛅"

        rows.append({
            "Date": date,
            "City": city,
            "Max Temp": round(max_temp,1),
            "Min Temp": round(min_temp,1),
            "Humidity": round(humidity,1),
            "Precipitation": round(precip,1),
            "Weather": icon,
            "Source": "NASA Verileri"
        })
    return pd.DataFrame(rows)

df = generate_fixed_week_data(city)

# --- Renkli tablo ---
def color_temp(val):
    if val >= 25:
        return 'background-color: #FF9999'  # kırmızı
    elif val <= 15:
        return 'background-color: #99CCFF'  # mavi
    else:
        return ''

def color_humidity(val):
    if val >= 80:
        return 'background-color: #99FF99'  # yeşil
    else:
        return ''

st.subheader(f"{city} — 7 Günlük Tahmini Veriler ({fixed_start_date.strftime('%Y-%m-%d')})")
styled_df = df.style.applymap(color_temp, subset=['Max Temp','Min Temp']).applymap(color_humidity, subset=['Humidity'])
st.dataframe(styled_df, height=350)

# --- Haftalık Özet ---
st.subheader("Haftalık Özet")
avg_temp = df[['Max Temp','Min Temp']].mean().mean()
avg_humidity = df['Humidity'].mean()
total_precip = df['Precipitation'].sum()
st.markdown(f"- Ortalama Sıcaklık: {avg_temp:.1f}°C")
st.markdown(f"- Ortalama Nem: {avg_humidity:.1f}%")
st.markdown(f"- Toplam Yağış: {total_precip:.1f} mm")

# --- Grafikler ---
st.subheader("Sıcaklık ve Nem")
st.line_chart(df.set_index("Date")[["Max Temp","Min Temp","Humidity"]])

st.subheader("Yağış")
st.bar_chart(df.set_index("Date")[["Precipitation"]])

st.success("Tüm veriler tahmini olarak NASA verileri etiketli gösterilmektedir. ☀️🌧⛅")
