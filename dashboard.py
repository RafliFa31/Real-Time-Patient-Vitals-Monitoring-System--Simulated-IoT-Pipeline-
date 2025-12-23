import streamlit as st
import pandas as pd
import psycopg2
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="ICU Monitor Dashboard",
    page_icon="🏥",
    layout="wide"
)

# --- FUNGSI KONEKSI DATABASE ---
def get_data():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="mysecretpassword"
        )
        # Ambil 50 data terakhir
        query = "SELECT * FROM patient_vitals ORDER BY id DESC LIMIT 50"
        df = pd.read_sql(query, conn)
        conn.close()
        
        # Urutkan kembali berdasarkan waktu (Ascending) untuk grafik
        df = df.sort_values(by='id', ascending=True)
        return df
    except Exception as e:
        return pd.DataFrame()

# --- TAMPILAN DASHBOARD ---
st.title("🏥 Real-Time Patient Vitals Monitor")
st.markdown("### Live Data Ingestion Pipeline (TCP/IP -> Docker -> Dashboard)")

placeholder = st.empty()

while True:
    df = get_data()

    with placeholder.container():
        if not df.empty:
            latest = df.iloc[-1]
            
            # 1. Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("❤️ Heart Rate", f"{latest['heart_rate']} bpm", int(latest['heart_rate'] - 80))
            with col2:
                st.metric("💧 SpO2", f"{latest['oxygen_level']} %", int(latest['oxygen_level'] - 95))
            with col3:
                status = latest['status']
                if status == "CRITICAL ALERT":
                    st.error(f"⚠️ STATUS: {status}")
                else:
                    st.success(f"✅ STATUS: {status}")

            # 2. Charts
            st.markdown("### 📈 Live Trends")
            # Pastikan timestamp dibaca sebagai datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            chart_data = df[['timestamp', 'heart_rate', 'oxygen_level']].set_index('timestamp')
            st.line_chart(chart_data)

            # 3. Data Table
            with st.expander("View Raw Data Log"):
                st.dataframe(df.sort_values(by='id', ascending=False).head(10))
        
        else:
            st.warning("Menunggu data masuk... Pastikan Simulator & Server sudah jalan!")

    time.sleep(1)