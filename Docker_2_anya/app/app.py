
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH   = os.getenv("DATA_PATH",   "/data/supply_chain.csv")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/output/heatmap.png")

print("=" * 60)
print("  SUPPLY CHAIN ANALYTICS — Вариант 18")
print("=" * 60)

df = pd.read_csv(DATA_PATH)
print(f"\nДатасет загружен: {DATA_PATH}")
print(f"Строк: {len(df)}, столбцов: {len(df.columns)}\n")

numeric_cols = [
    "transit_time_h", "shipping_cost_usd", "cargo_weight_kg",
    "distance_km", "fuel_liters", "units_handled", "delay_h"
]

print("── Основные статистики ──────────────────────────────────")
print(df[numeric_cols].describe().round(2).to_string())

print("\n── Средние значения по типу транспорта ─────────────────")
group = df.groupby("transport_type")[["shipping_cost_usd", "transit_time_h", "delay_h"]].mean().round(2)
print(group.to_string())

print("\n── ТОП-3 поставщика по объему перевозок (ед.) ──────────")
top_sup = df.groupby("supplier")["units_handled"].sum().sort_values(ascending=False).head(3)
print(top_sup.to_string())

corr = df[numeric_cols].corr().round(2)

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5,
    linecolor="white",
    annot_kws={"size": 11},
    ax=ax,
)
ax.set_title("Матрица корреляций признаков Supply Chain", fontsize=14, pad=15)
ax.tick_params(axis="x", rotation=30, labelsize=10)
ax.tick_params(axis="y", rotation=0, labelsize=10)

plt.tight_layout()

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
plt.savefig(OUTPUT_PATH, dpi=150)
plt.close()

print(f"\n[✓] Тепловая карта сохранена: {OUTPUT_PATH}")
print("=" * 60)
