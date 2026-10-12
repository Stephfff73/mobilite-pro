import streamlit as st
import pandas as pd
from datetime import date, time, timedelta
from services.routing import driving_route, geocode
from core.cost_engine import car_cost, scenario_total
from core.recommendation import recommend
from services.carbon import estimate_carbon

st.set_page_config(page_title="Mobilité Pro", page_icon="🧭", layout="wide")
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#f5f8fc 0%,#eef4f7 100%);}
.block-container {padding-top: 1.6rem; max-width: 1400px;}
.hero {padding: 1.5rem 1.8rem; border-radius: 22px; color: white;
background: linear-gradient(115deg,#102b46,#176b78); margin-bottom: 1rem;}
.hero h1 {color:white; margin:0; font-size:2.2rem;}
.hero p {color:#dcecf1; margin:.4rem 0 0 0;}
.metric-card {background:white;border:1px solid #e2eaf0;border-radius:16px;padding:1rem;}
.small-note {color:#526779;font-size:.88rem;}
</style>
<div class="hero">
<h1>🧭 Mobilité Pro</h1>
<p>Planifiez vos déplacements professionnels avec une vision porte-à-porte : budget, ponctualité et empreinte carbone.</p>
</div>
""", unsafe_allow_html=True)

HOME = "57 Impasse de la Ville, 38300 Châteauvilain"
with st.sidebar:
    st.header("⚙️ Paramètres")
    home = st.text_input("Adresse de départ et de retour", HOME)
    consumption = st.number_input("Consommation diesel (L/100 km)", 1.0, 20.0, 6.0, 0.1)
    diesel_price = st.number_input("Prix du diesel (€/L)", 0.5, 4.0, 1.75, 0.01)
    tolls_roundtrip = st.number_input("Péages voiture A/R (€)", 0.0, 1000.0, 0.0, 1.0)
    car_parking = st.number_input("Stationnement destination (€)", 0.0, 1000.0, 0.0, 1.0)
    safety_minutes = st.slider("Marge de sécurité avant le rendez-vous (minutes)", 15, 240, 90, 15)
    st.caption("Les coûts d'entretien/dépréciation peuvent être ajoutés plus tard. Les tarifs des transporteurs doivent être confirmés avant réservation.")

st.subheader("1 · Votre déplacement")
with st.form("trip"):
    c1, c2 = st.columns([2,1])
    with c1:
        destination = st.text_input("Destination du rendez-vous", placeholder="Adresse, entreprise, ville…")
        meeting_date = st.date_input("Date du rendez-vous", value=date.today() + timedelta(days=7), min_value=date.today())
    with c2:
        meeting_time = st.time_input("Heure impérative d'arrivée", value=time(9,30), step=timedelta(minutes=15))
        nights = st.number_input("Nombre de nuits sur place", min_value=0, max_value=30, value=0)
    c3,c4,c5 = st.columns(3)
    with c3:
        multiple = st.checkbox("Plusieurs rendez-vous ?")
    with c4:
        priorities = st.selectbox("Priorité", ["Équilibre coût / temps / fiabilité", "Coût minimal", "Ponctualité maximale", "Empreinte carbone minimale"])
    with c5:
        return_same_day = st.checkbox("Retour le jour même", value=True)
    extra_addresses = st.text_area("Autres adresses (une par ligne)", disabled=not multiple, placeholder="Adresse du 2e rendez-vous\nAdresse du 3e rendez-vous")
    submitted = st.form_submit_button("Comparer les scénarios", type="primary", use_container_width=True)

if submitted:
    if not destination.strip():
        st.error("Saisissez une destination pour lancer la comparaison.")
        st.stop()
    with st.spinner("Recherche de l'itinéraire routier et calcul des coûts…"):
        route = driving_route(home, destination)
    st.session_state["last_trip"] = {
        "destination": destination, "date": str(meeting_date), "time": str(meeting_time),
        "nights": int(nights), "route": route
    }
    st.subheader("2 · Votre tableau de bord")
    if route.get("ok"):
        km_oneway = route["distance_km"]
        minutes_oneway = route["duration_min"]
        cc = car_cost(km_oneway, consumption, diesel_price, tolls_roundtrip, car_parking, return_same_day)
        carbon_car = estimate_carbon("car", km_oneway * (2 if return_same_day else 1))
        a,b,c,d = st.columns(4)
        a.metric("Distance routière (aller)", f"{km_oneway:.0f} km")
        b.metric("Temps routier estimé (aller)", f"{minutes_oneway//60} h {minutes_oneway%60:02.0f} min")
        c.metric("Carburant estimé", f"{cc['fuel_eur']:.2f} €")
        d.metric("CO₂ voiture estimé", f"{carbon_car:.1f} kg CO₂e")
        st.caption("Itinéraire fourni par OSRM (durée indicative sans garantie de trafic en temps réel). Vérifiez l'itinéraire avant le départ.")
        st.link_button("Ouvrir l'itinéraire dans OpenStreetMap", route["map_url"])
    else:
        st.warning("L'itinéraire automatique n'a pas pu être calculé. Vérifiez l'adresse et utilisez le calcul manuel ci-dessous.")
        st.write(route.get("error", "Service de routage indisponible."))
        km_oneway = st.number_input("Distance aller estimée (km)", min_value=0.0, value=100.0)
        minutes_oneway = st.number_input("Durée aller estimée (minutes)", min_value=0, value=90)
        cc = car_cost(km_oneway, consumption, diesel_price, tolls_roundtrip, car_parking, return_same_day)
        carbon_car = estimate_carbon("car", km_oneway * (2 if return_same_day else 1))

    st.subheader("3 · Comparez les trois modes")
    st.info("Les prix et durées train/avion ci-dessous sont à renseigner depuis une offre réelle. Les champs vides ne sont pas inventés.")
    train1, train2, train3 = st.columns(3)
    with train1:
        st.markdown("### 🚗 Voiture")
        st.metric("Coût calculé", f"{cc['total_eur']:.2f} €")
        st.metric("Temps de conduite A/R", f"{(minutes_oneway * (2 if return_same_day else 1))/60:.1f} h")
        st.metric("CO₂ estimé", f"{carbon_car:.1f} kg")
        st.caption("Carburant + péages saisis + stationnement destination. Hors usure/dépréciation.")
    with train2:
        st.markdown("### 🚄 Train")
        rail_fare = st.number_input("Billet A/R après carte Liberté (€)", min_value=0.0, value=0.0, key="rail_fare")
        rail_duration = st.number_input("Temps porte-à-porte total (heures)", min_value=0.0, value=0.0, key="rail_duration")
        rail_access = st.number_input("Voiture domicile–gare A/R (€)", min_value=0.0, value=0.0, key="rail_access")
        rail_parking = st.number_input("Parking gare (€)", min_value=0.0, value=0.0, key="rail_parking")
        rail_local = st.number_input("Transports locaux A/R (€)", min_value=0.0, value=0.0, key="rail_local")
        rail_carbon = st.number_input("CO₂ train total (kg CO₂e, source)", min_value=0.0, value=0.0, key="rail_carbon")
        rail_total = scenario_total([rail_fare, rail_access, rail_parking, rail_local])
        st.metric("Coût total renseigné", f"{rail_total:.2f} €")
        st.caption("Le tarif doit correspondre à votre carte Liberté et au train exact. Zéro signifie non renseigné, pas gratuit.")
    with train3:
        st.markdown("### ✈️ Avion")
        air_fare = st.number_input("Billet A/R + bagages (€)", min_value=0.0, value=0.0, key="air_fare")
        air_duration = st.number_input("Temps porte-à-porte total (heures)", min_value=0.0, value=0.0, key="air_duration")
        air_access = st.number_input("Voiture domicile–aéroport A/R (€)", min_value=0.0, value=0.0, key="air_access")
        air_parking = st.number_input("Parking aéroport (€)", min_value=0.0, value=0.0, key="air_parking")
        air_local = st.number_input("Transferts locaux A/R (€)", min_value=0.0, value=0.0, key="air_local")
        air_carbon = st.number_input("CO₂ avion total (kg CO₂e, source)", min_value=0.0, value=0.0, key="air_carbon")
        air_total = scenario_total([air_fare, air_access, air_parking, air_local])
        st.metric("Coût total renseigné", f"{air_total:.2f} €")
        st.caption("L'avion n'est pertinent que si une liaison réelle et adaptée existe. Incluez les temps d'accès, contrôles et transferts.")

    rows = [
        {"Mode": "Voiture", "Coût total (€)": round(cc["total_eur"],2), "Temps porte-à-porte (h)": round(minutes_oneway*(2 if return_same_day else 1)/60,2), "CO₂e (kg)": round(carbon_car,1), "Données": "Itinéraire estimé"},
        {"Mode": "Train", "Coût total (€)": round(rail_total,2), "Temps porte-à-porte (h)": rail_duration or None, "CO₂e (kg)": rail_carbon or None, "Données": "À confirmer" if not rail_fare or not rail_duration else "Saisie utilisateur"},
        {"Mode": "Avion", "Coût total (€)": round(air_total,2), "Temps porte-à-porte (h)": air_duration or None, "CO₂e (kg)": air_carbon or None, "Données": "À confirmer" if not air_fare or not air_duration else "Saisie utilisateur"},
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.subheader("4 · Recommandation")
    st.write(recommend(rows, priorities))
    st.subheader("5 · Heure de départ conseillée")
    buffer_hours = safety_minutes / 60
    depart = (pd.Timestamp.combine(meeting_date, meeting_time) - pd.Timedelta(minutes=minutes_oneway + safety_minutes))
    st.metric("Départ voiture conseillé", depart.strftime("%d/%m/%Y à %H:%M"))
    st.caption(f"Marge de sécurité configurée : {safety_minutes} minutes, ajoutée au temps routier estimé. Ce calcul ne garantit pas l'absence d'aléas.")
    st.subheader("6 · Hébergement")
    if nights:
        st.write(f"Vous avez indiqué {nights} nuit(s). Recherchez les hébergements pour les dates exactes et comparez le prix total, les frais et la distance au rendez-vous.")
        st.link_button("Rechercher des hôtels à proximité", "https://www.google.com/travel/hotels")
        st.link_button("Rechercher des locations", "https://www.airbnb.fr/")
        st.caption("Les liens ouvrent des recherches générales ; aucun tarif ni disponibilité n'a été vérifié.")
    else:
        st.write("Aucune nuitée prévue. Cochez un nombre de nuits supérieur à zéro pour intégrer l'hébergement à votre budget.")
    if multiple and extra_addresses.strip():
        st.subheader("7 · Étapes supplémentaires")
        st.write("Adresses à intégrer dans une prochaine version d'optimisation multi-étapes :")
        st.code(extra_addresses)

else:
    st.markdown("### Votre espace de préparation")
    c1,c2,c3 = st.columns(3)
    c1.info("**Budget complet**\n\nCarburant, péages, parkings, billets et transferts.")
    c2.info("**Ponctualité**\n\nHeure de départ calculée à rebours avec une marge configurable.")
    c3.info("**Empreinte carbone**\n\nEstimations distinctes par mode et méthode documentée.")
    st.markdown("**Pour commencer :** saisissez une destination et l'heure impérative du rendez-vous, puis cliquez sur « Comparer les scénarios ».")
    st.caption("Prototype MVP : les tarifs ferroviaires/aériens, les parkings et le trafic temps réel ne sont pas encore connectés à des fournisseurs commerciaux.")
