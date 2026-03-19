import os
import numpy as np
import pandas as pd

np.random.seed(42)
N = 500

transport_types = ["truck", "rail", "air", "sea"]
suppliers = ["AlphaLogistics", "BetaTrans", "GammaFreight", "DeltaShip"]
routes = [
    "Moscow-SPb", "Moscow-Kazan", "SPb-Novosibirsk",
    "Kazan-Yekaterinburg", "Moscow-Krasnodar", "Novosibirsk-Omsk",
]

distance_km = np.random.uniform(50, 5000, N)

data = {
    "shipment_id": range(1, N + 1),
    "route": np.random.choice(routes, N),
    "transport_type": np.random.choice(transport_types, N),
    "supplier": np.random.choice(suppliers, N),
    "transit_time_h": (distance_km / np.random.uniform(60, 120, N)).round(1),
    "shipping_cost_usd": (distance_km * np.random.uniform(0.3, 1.2, N)).round(2),
    "cargo_weight_kg": np.random.uniform(100, 20000, N).round(0),
    "distance_km": distance_km.round(1),
    "fuel_liters": (distance_km * 0.35 + np.random.uniform(0, 50, N)).round(1),
    "units_handled": np.random.randint(1, 500, N),
    "delay_h": np.random.exponential(scale=3, size=N).round(1),
}

df = pd.DataFrame(data)

os.makedirs("data", exist_ok=True)
output_path = os.path.join("data", "supply_chain.csv")
df.to_csv(output_path, index=False)

print(f"[✓] Датасет сгенерирован: {output_path} ({N} строк, {len(df.columns)} столбцов)")
print(df.head(3).to_string(index=False))
