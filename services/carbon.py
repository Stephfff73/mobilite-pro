# Facteur provisoire configurable. À remplacer/valider avec le facteur ADEME approprié
# (véhicule, carburant, occupation et périmètre exacts) avant usage de reporting officiel.
DIESEL_TAILPIPE_KG_PER_L = 2.68

def estimate_carbon(mode, distance_km, litres=None, factor_kg_per_km=None):
    distance = max(0.0, float(distance_km))
    if mode == "car":
        if litres is not None:
            return float(litres) * DIESEL_TAILPIPE_KG_PER_L
        # Valeur d'usage illustrative à la consommation par défaut de 6 L/100 km.
        return distance * 0.06 * DIESEL_TAILPIPE_KG_PER_L
    if factor_kg_per_km is not None:
        return distance * max(0.0, float(factor_kg_per_km))
    return 0.0  # Ne pas inventer un facteur train/avion absent.
