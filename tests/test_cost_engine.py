from core.cost_engine import car_cost

def test_car_cost_round_trip():
    result = car_cost(100, 6, 1.75, 10, 5, True)
    assert result["distance_km"] == 200
    assert result["litres"] == 12
    assert round(result["fuel_eur"], 2) == 21.00
    assert round(result["total_eur"], 2) == 36.00

def test_one_way():
    result = car_cost(100, 6, 1.75, 0, 0, False)
    assert result["distance_km"] == 100
    assert result["litres"] == 6
