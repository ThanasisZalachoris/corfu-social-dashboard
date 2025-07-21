import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Corfu Social Dashboard", layout="wide")

# Sidebar - User interaction
with st.sidebar:
    st.markdown("### 📌 Παρατηρήσεις")
    indicator = st.selectbox(
        "Επίλεξε Δείκτη για Ανάλυση",
        ["TSI (Τουριστικός Κορεσμός)", "PFI (Πληθυσμιακή Ροή)", "DRI (Ψηφιακή Ετοιμότητα)"]
    )
    if indicator == "TSI (Τουριστικός Κορεσμός)":
        st.info("📈 Ο δείκτης TSI αγγίζει το 1350% τον Αύγουστο, υποδεικνύοντας υπερκορεσμό κυρίως στις κεντρικές περιοχές. Ενδείκνυται ανάγκη για ανακατανομή ροών.")
    elif indicator == "PFI (Πληθυσμιακή Ροή)":
        st.info("👥 Η πληθυσμιακή αύξηση κατά 212% σχετίζεται με εποχικούς εργαζόμενους και τουριστική αιχμή. Πιθανά προβλήματα στην κυκλοφορία και τις υποδομές.")
    elif indicator == "DRI (Ψηφιακή Ετοιμότητα)":
        st.info("🌐 Ο δείκτης DRI παραμένει σταθερός, αλλά με υστέρηση σε αγροτικές περιοχές (π.χ. Αχαράβη). Ευκαιρία για στοχευμένες επενδύσεις.")

# Tabs for dashboard
tab1, tab2, tab3, tab4 = st.tabs(["📊 Τουρισμός", "🚗 Κυκλοφορία", "🌐 Ψηφιακή Πρόσβαση", "📡 Καιρός Live (API)"])

with tab1:
    st.markdown("""
        <h2>📈 Δείκτες Τουριστικής Κίνησης</h2>
        <p style='color:gray;'>Στοιχεία επιβατικής κίνησης στο Αεροδρόμιο Κέρκυρας (demo δεδομένα)</p>
    """, unsafe_allow_html=True)

    data = {
        "Μήνας": ["April", "May", "June", "July", "August", "September", "October"],
        "Αφίξεις": [45000, 65000, 98000, 130000, 145000, 85000, 32000]
    }
    df = pd.DataFrame(data)
    fig = px.line(df, x="Μήνας", y="Αφίξεις", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("TSI (Tourism Saturation Index)", "1350%", "+150% σε σχέση με πέρυσι")
    col2.metric("PFI (Population Flow Index)", "212%", "+45% από τον προηγούμενο μήνα")
    col3.metric("DRI (Digital Readiness Index)", "68.2 / 100", "σταθερή αύξηση")

with tab2:
    st.markdown("""
        <h2>🚦 Κυκλοφοριακή Πίεση ανά Περιοχή & Ώρα</h2>
        <p style='color:gray;'>Demo δεδομένα για τις κύριες τουριστικές περιοχές</p>
    """, unsafe_allow_html=True)

    traffic_data = {
        "Περιοχή": ["Κέντρο", "Αεροδρόμιο", "Παλαιοκαστρίτσα", "Σιδάρι"],
        "08:00": [85, 70, 60, 50],
        "10:00": [90, 75, 63, 55],
        "12:00": [95, 78, 67, 54],
        "14:00": [93, 76, 62, 59],
        "16:00": [87, 72, 62, 52],
        "18:00": [80, 68, 60, 52],
    }
    traffic_df = pd.DataFrame(traffic_data).set_index("Περιοχή")
    st.dataframe(traffic_df.style.background_gradient(cmap="Reds"), use_container_width=True)

with tab3:
    st.markdown("""
        <h2>🌐 Δείκτης Ψηφιακής Πρόσβασης</h2>
        <p style='color:gray;'>Ποσοστά πρόσβασης στο διαδίκτυο ανά περιοχή</p>
    """, unsafe_allow_html=True)

    digital_data = {
        "Περιοχή": ["Κέρκυρα", "Λευκίμμη", "Αχαράβη", "Γαστούρι", "Σιδάρι"],
        "Ποσοστό Πρόσβασης (%)": [88, 79, 76, 82, 78]
    }
    digital_df = pd.DataFrame(digital_data)
    fig2 = px.bar(digital_df, x="Περιοχή", y="Ποσοστό Πρόσβασης (%)", color="Ποσοστό Πρόσβασης (%)", color_continuous_scale="Blues")
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.markdown("""
        <h2>🌤️ Live Καιρικά Δεδομένα για Κέρκυρα</h2>
        <p style='color:gray;'>Μέσω WeatherAPI.com</p>
    """, unsafe_allow_html=True)

    API_KEY = "efc3e0e550ae45c98b5184129252107"  # βάλε το σωστό εδώ
city = "Corfu"
url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&lang=el"

def get_weather():
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"❌ Σφάλμα API: {res.status_code}")
            return None
    except Exception as e:
        st.error(f"❌ Σφάλμα σύνδεσης: {e}")
        return None

data = get_weather()

if data:
    current = data['current']
    st.success(f"🌡 Θερμοκρασία: {current['temp_c']} °C")
    st.write(f"💧 Υγρασία: {current['humidity']} %")
    st.write(f"🍃 Άνεμος: {current['wind_kph']} km/h")
    st.write(f"☁️ Κατάσταση: {current['condition']['text']}")
    st.image("https:" + current['condition']['icon'], width=64)
else:
    st.warning("⚠️ Δεν βρέθηκαν δεδομένα.")

data = get_forecast()
if data:
    forecast = data['forecast']['forecastday']
    current = data['current']
    astro = forecast[0]['astro']

    with st.expander("🌤 Τρέχουσες Συνθήκες", expanded=True):
        condition = current['condition']['text']
        icon = current['condition']['icon']
        st.metric("🌡 Θερμοκρασία", f"{current['temp_c']} °C")
        st.metric("💧 Υγρασία", f"{current['humidity']} %")
        st.metric("🍃 Άνεμος", f"{current['wind_kph']} km/h")
        st.write(f"🌥 Κατάσταση: {condition}")
        st.image("https:" + icon, width=60)

    with st.expander("🔮 Πρόγνωση Καιρού (3 Ημέρες)", expanded=False):
        for day in forecast:
            date = day['date']
            condition = day['day']['condition']['text']
            icon = day['day']['condition']['icon']
            max_temp = day['day']['maxtemp_c']
            min_temp = day['day']['mintemp_c']
            humidity = day['day']['avghumidity']
            wind = day['day']['maxwind_kph']

            st.subheader(f"📅 {date}")
            st.image("https:" + icon, width=50)
            st.write(f"🌤 Κατάσταση: {condition}")
            st.write(f"🌡 Μέγιστη: {max_temp}°C | Ελάχιστη: {min_temp}°C")
            st.write(f"💧 Μέση Υγρασία: {humidity}%")
            st.write(f"🍃 Μέγιστος Άνεμος: {wind} km/h")

    with st.expander("🌅 Ώρες Ηλίου & Σελήνης", expanded=False):
        st.write(f"☀️ Ανατολή Ηλίου: {astro['sunrise']}")
        st.write(f"🌇 Δύση Ηλίου: {astro['sunset']}")
        st.write(f"🌙 Ανατολή Σελήνης: {astro['moonrise']}")
        st.write(f"🌘 Δύση Σελήνης: {astro['moonset']}")

    if 'tide' in data:
        with st.expander("🌊 Θαλάσσιες Συνθήκες (Tides)", expanded=False):
            tides = data['tide']['tide']
            for tide_entry in tides:
                st.write(f"📌 {tide_entry['tide_type']} στις {tide_entry['tide_time']} (Ύψος: {tide_entry['tide_height_mt']} m)")
else:
    st.warning("⚠️ Δεν βρέθηκαν στοιχεία πρόγνωσης.")


