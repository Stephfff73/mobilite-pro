def recommend(rows, priority):
    eligible = []
    for row in rows:
        if row.get("Mode") == "Voiture":
            eligible.append(row)
        elif row.get("Coût total (€)", 0) and row.get("Temps porte-à-porte (h)") and row.get("Données") != "À confirmer":
            eligible.append(row)
    if len(eligible) == 1:
        return ("Pour l'instant, seule la voiture dispose d'un scénario calculé. "
                "Renseignez les tarifs et durées confirmés du train et de l'avion pour obtenir une comparaison équitable.")
    if priority == "Coût minimal":
        chosen = min(eligible, key=lambda r: r["Coût total (€)"])
    elif priority == "Ponctualité maximale":
        chosen = min(eligible, key=lambda r: r["Temps porte-à-porte (h)"])
    elif priority == "Empreinte carbone minimale":
        with_carbon = [r for r in eligible if r.get("CO₂e (kg)") is not None and r["CO₂e (kg)"] > 0]
        if not with_carbon:
            return "Impossible de classer les modes par carbone : fournissez des facteurs ou estimations comparables et sourcés."
        chosen = min(with_carbon, key=lambda r: r["CO₂e (kg)"])
    else:
        # Score simple normalisé coût/temps, avec préférence prudente pour données vérifiées.
        min_cost = min(max(r["Coût total (€)"], 0.01) for r in eligible)
        min_time = min(max(r["Temps porte-à-porte (h)"], 0.01) for r in eligible)
        chosen = min(eligible, key=lambda r: 0.5*r["Coût total (€)"]/min_cost + 0.5*r["Temps porte-à-porte (h)"]/min_time)
    return (f"Selon le critère sélectionné, **{chosen['Mode']}** ressort en tête parmi les scénarios renseignés. "
            "Vérifiez les tarifs, horaires, marges de correspondance et perturbations avant de réserver.")
