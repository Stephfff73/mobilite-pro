def car_cost(distance_oneway_km, consumption_l_100km, diesel_eur_l,
             tolls_roundtrip_eur=0.0, destination_parking_eur=0.0,
             return_same_day=True, access_cost_eur=0.0):
    trips = 2 if return_same_day else 1
    distance = max(0.0, float(distance_oneway_km)) * trips
    litres = distance * max(0.0, float(consumption_l_100km)) / 100
    fuel = litres * max(0.0, float(diesel_eur_l))
    total = fuel + max(0.0, tolls_roundtrip_eur) + max(0.0, destination_parking_eur) + max(0.0, access_cost_eur)
    return {"distance_km": distance, "litres": litres, "fuel_eur": fuel,
            "tolls_eur": max(0.0, tolls_roundtrip_eur),
            "parking_eur": max(0.0, destination_parking_eur), "total_eur": total}

def scenario_total(items):
    return sum(max(0.0, float(x or 0)) for x in items)
