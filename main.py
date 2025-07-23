# 📁 corfu-social-dashboard/main.py (cleaned-up start)

import streamlit as st
import requests
from pandas import DataFrame
import plotly.express as px
import numpy as np

# Streamlit app config
st.set_page_config(page_title="Corfu Social Dashboard", layout="wide")

# Hide Streamlit default padding for cleaner UI
st.markdown("""
    <style>
        .css-18e3th9 {padding-top: 1rem;}
    </style>
""", unsafe_allow_html=True)

# ----------------------
# Sidebar Setup
# ----------------------
with st.sidebar:
    st.title("⚙️ Ρυθμίσεις Πίνακα")
    selected_tab = st.radio("Μετάβαση σε:", ["📊 Δείκτες", "📈 Γραφήματα", "🌤 Καιρός", "🔧 Ρυθμίσεις"])

# ----------------------
# Define App Structure
# ----------------------
def show_dashboard():
    st.header("📊 Δείκτες Τουριστικής Κίνησης - Demo")
    with st.expander("ℹ️ Τι δείχνουν αυτοί οι δείκτες;", expanded=False):
        st.markdown("""
        - **Τουριστικός Κορεσμός**: Αναλογία τουριστών προς τον πληθυσμό και την αντοχή των υποδομών.
        - **Πληθυσμιακή Πίεση**: Μεταβολή πληθυσμού λόγω εποχικότητας (εργαζόμενοι & τουρίστες).
        - **Ψηφιακή Συνδεσιμότητα**: Πρόσβαση των κατοίκων/τουριστών σε ψηφιακές υπηρεσίες.
         - **WCI**: Δείχνει την πίεση στο δίκτυο ύδρευσης σε σχέση με τη ζήτηση ανά επισκέπτη.
        - **WPI**: Εκτιμά την κυκλοφοριακή συμφόρηση βάσει δεδομένων ροής.
        - **NTI**: Αντικατοπτρίζει τη δραστηριότητα και κορεσμό κατά τις νυχτερινές ώρες.
        """)
    col1, col2, col3 = st.columns(3)
    col1.metric("Τουριστικός Κορεσμός", "1350%", "+150% από πέρυσι")
    col2.metric("Πληθυσμιακή Πίεση", "212%", "+45% από προηγούμενο μήνα")
    col3.metric("Ψηφιακή Συνδεσιμότητα", "68.2 / 100", "→ σταθερό")

    st.subheader("💧 Δείκτες Πίεσης Πόρων και Υποδομών")
    col4, col5, col6 = st.columns(3)
    col4.metric("🚰 WCI (Υδατική Κατανάλωση)", "310 lt/ημ", "+20% σε σχέση με όριο ασφαλείας")
    col5.metric("🚦 WPI (Κυκλοφοριακή Πίεση)", "78 / 100", "↑ αυξημένη ένταση στο κέντρο")
    col6.metric("🌃 NTI (Νυχτερινή Ένταση)", "89 / 100", "↑ νυχτερινή δραστηριότητα")

def show_graphs():
    st.header("📈 Οπτικοποίηση Δεικτών - Demo")
    st.subheader("Αφίξεις στο Αεροδρόμιο Κέρκυρας")

    # Δυναμικά δεδομένα
    months = ["April", "May", "June", "July", "August", "September", "October"]
    arrivals = [45000, 65000, 98000, 130000, 145000, 85000, 32000]
    growth = np.round(np.random.uniform(-0.1, 0.3, len(months)), 2)

    df = DataFrame({
        "Μήνας": months,
        "Αφίξεις": arrivals,
        "Μεταβολή": growth
    })

    with st.expander("📊 Πίνακας Αφίξεων", expanded=True):
        st.dataframe(df.style.format({"Αφίξεις": "{:,}"}))

    with st.expander("📈 Γραφήματα", expanded=True):
        chart_type = st.selectbox("Επιλέξτε τύπο διαγράμματος:", ["Area", "Bar", "Line"])

        if chart_type == "Area":
            fig = px.area(df, x="Μήνας", y="Αφίξεις", title="Εποχική Κατανομή Αφίξεων", color_discrete_sequence=["#007acc"])
        elif chart_type == "Bar":
            fig = px.bar(df, x="Μήνας", y="Αφίξεις", title="Αφίξεις ανά Μήνα", color="Μήνας")
        else:
            fig = px.line(df, x="Μήνας", y="Αφίξεις", title="Γραμμικό Διάγραμμα Αφίξεων", markers=True)

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("🌍 Θερμικός Χάρτης Προέλευσης Τουριστών", expanded=False):
            st.caption("Top 10 χώρες με τις περισσότερες αφίξεις στην Κέρκυρα (demo)")

            country_data = {
                "Χώρα": ["Ην. Βασίλειο", "Γερμανία", "Ιταλία", "Γαλλία", "Ολλανδία", "Πολωνία", "Ρουμανία", "Τσεχία",
                         "Σουηδία", "Νορβηγία"],
                "Αφίξεις": [86000, 79000, 62000, 48000, 41000, 39000, 35000, 33000, 31000, 29000],
                "Σημαία": ["🇬🇧", "🇩🇪", "🇮🇹", "🇫🇷", "🇳🇱", "🇵🇱", "🇷🇴", "🇨🇿", "🇸🇪", "🇳🇴"]
            }

            cdf = DataFrame(country_data)
            cdf.sort_values("Αφίξεις", ascending=False, inplace=True)

            st.dataframe(cdf.style.background_gradient(subset=["Αφίξεις"], cmap='Blues'))

            fig_map = px.density_heatmap(
    cdf,
    x="Χώρα",
    y="Αφίξεις",
    z="Αφίξεις",
    color_continuous_scale="YlOrRd",
    title="Θερμική Κατανομή Αφίξεων ανά Χώρα",
    category_orders={"Χώρα": cdf["Χώρα"].tolist()}
)

            st.plotly_chart(fig_map, use_container_width=True)

def show_weather():
    st.header("🌤 Live Καιρικά Δεδομένα - Κέρκυρα")
    st.caption("Μέσω WeatherAPI.com")

    API_KEY = "efc3e0e550ae45c98b5184129252107"  # Βάλε εδώ το κλειδί σου
    city = "Corfu"

    @st.cache_data(ttl=600)
    def get_forecast():
        url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3&lang=el&aqi=no&alerts=no"
        try:
            res = requests.get(url)
            if res.status_code == 200:
                return res.json()
            else:
                st.error(f"❌ API error: {res.status_code}")
                return None
        except:
            return None

    data = get_forecast()
    if not data:
        st.warning("⚠️ Δεν βρέθηκαν δεδομένα.")
        return

    current = data['current']
    forecast = data['forecast']['forecastday']
    astro = forecast[0]['astro']

    with st.expander("📍 Τρέχουσες Συνθήκες", expanded=True):
        st.metric("🌡 Θερμοκρασία", f"{current['temp_c']} °C")
        st.metric("💧 Υγρασία", f"{current['humidity']}%")
        st.metric("🍃 Άνεμος", f"{current['wind_kph']} km/h")
        st.image("https:" + current['condition']['icon'], width=60)

    with st.expander("🔮 Πρόγνωση 3 Ημερών"):
        for day in forecast:
            st.subheader(day['date'])
            st.image("https:" + day['day']['condition']['icon'], width=50)
            st.write(f"Κατάσταση: {day['day']['condition']['text']}")
            st.write(f"Μέγιστη Θερμοκρασία: {day['day']['maxtemp_c']} °C")
            st.write(f"Ελάχιστη Θερμοκρασία: {day['day']['mintemp_c']} °C")

    with st.expander("🌄 Ώρες Ηλίου/Σελήνης"):
        st.write(f"☀️ Ανατολή Ηλίου: {astro['sunrise']}")
        st.write(f"🌇 Δύση Ηλίου: {astro['sunset']}")
        st.write(f"🌙 Ανατολή Σελήνης: {astro['moonrise']}")
        st.write(f"🌘 Δύση Σελήνης: {astro['moonset']}")


# ----------------------
# Main App Logic
# ----------------------
if selected_tab == "📊 Δείκτες":
    show_dashboard()
elif selected_tab == "📈 Γραφήματα":
    show_graphs()
elif selected_tab == "🌤 Καιρός":
    show_weather()
else:
    st.info("⚙️ Πεδίο Ρυθμίσεων – σύντομα διαθέσιμο.")

