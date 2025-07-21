import pandas as pd
import plotly.express as px
import streamlit as st

# Tabs για θεματική οργάνωση
tab1, tab2, tab3 = st.tabs(["📊 Τουρισμός", "🚗 Κυκλοφορία", "🌐 Ψηφιακή Πρόσβαση"])

with tab1:
    st.title("📊 Δείκτες Τουριστικής Κίνησης")
    st.subheader("Αφίξεις Τουριστών στο Αεροδρόμιο Κέρκυρας (demo)")

    # Demo Time Series για Αφίξεις
    months = ['April', 'May', 'June', 'July', 'August', 'September', 'October']
    arrivals = [40000, 60000, 95000, 130000, 145000, 90000, 30000]
    df_arrivals = pd.DataFrame({'Μήνας': months, 'Αφίξεις': arrivals})

    fig_arrivals = px.area(df_arrivals, x='Μήνας', y='Αφίξεις', markers=True)
    st.plotly_chart(fig_arrivals, use_container_width=True)

    # KPI Cards
    st.subheader("Κύριοι Δείκτες")
    col1, col2, col3 = st.columns(3)
    col1.metric("TSI", "1350%", "+150% σε σχέση με πέρυσι")
    col2.metric("PFI", "212%", "+45% σε σχέση με τον προηγούμενο μήνα")
    col3.metric("DRI", "68.2 / 100", "↗ σταθερή αύξηση")

with tab2:
    st.title("🚗 Δείκτης Κυκλοφοριακής Πίεσης (demo)")
    st.write("Ανά περιοχή και ώρα")

    areas = ['Κέντρο', 'Αεροδρόμιο', 'Παλαιοκαστρίτσα', 'Σιδάρι']
    hours = ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00']
    traffic_data = [
        [85, 90, 95, 93, 87, 80],
        [70, 75, 78, 76, 72, 68],
        [60, 63, 67, 66, 62, 60],
        [50, 55, 58, 59, 54, 52],
    ]
    df_traffic = pd.DataFrame(traffic_data, index=areas, columns=hours)
    st.dataframe(df_traffic.style.background_gradient(cmap='Reds'), height=250)

with tab3:
    st.title("🌐 Δείκτης Ψηφιακής Πρόσβασης ανά Περιοχή (demo)")
    digital_data = {
        "Περιοχή": ["Κέρκυρα", "Λευκίμμη", "Αχαράβη", "Γαστούρι", "Σιδάρι"],
        "Ποσοστό Πρόσβασης (%)": [92, 81, 75, 84, 78]
    }
    df_digital = pd.DataFrame(digital_data)
    fig_digital = px.bar(df_digital, x='Περιοχή', y='Ποσοστό Πρόσβασης (%)',
                         color='Ποσοστό Πρόσβασης (%)', color_continuous_scale='blues')
    st.plotly_chart(fig_digital, use_container_width=True)

