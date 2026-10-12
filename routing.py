import requests
from urllib.parse import quote

USER_AGENT = "MobilitePro/0.1 (prototype personnel; configurez un contact avant production)"

def geocode(address):
    url = "https://nominatim.openstreetmap.org/search"
    response = requests.get(url, params={"q": address, "format": "jsonv2", "limit": 1},
                            headers={"User-Agent": USER_AGENT}, timeout=15)
    response.raise_for_status()
    results = response.json()
    if not results:
        raise ValueError(f"Adresse introuvable : {address}")
    return float(results[0]["lon"]), float(results[0]["lat"])

def driving_route(origin, destination):
    try:
        lon1, lat1 = geocode(origin)
        lon2, lat2 = geocode(destination)
        url = f"https://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}"
        response = requests.get(url, params={"overview":"false", "alternatives":"false"},
                                headers={"User-Agent": USER_AGENT}, timeout=25)
        response.raise_for_status()
        data = response.json()
        if data.get("code") != "Ok" or not data.get("routes"):
            raise ValueError("Le moteur de routage n'a pas renvoyé de route.")
        route = data["routes"][0]
        return {
            "ok": True, "distance_km": route["distance"]/1000,
            "duration_min": round(route["duration"]/60),
            "map_url": f"https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route={lat1}%2C{lon1}%3B{lat2}%2C{lon2}"
        }
    except Exception as exc:
        return {"ok": False, "error": str(exc)}
