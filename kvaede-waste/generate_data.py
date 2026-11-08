"""Fake data for Kvaede, a juice bar chain I made up.

Two things are planted for the pipeline to find: Kongens Nytorv wastes far
more avocado than the other bars, and some waste is typed in kg or l
instead of g or ml.
"""

import csv
import math
import os
import random
from datetime import date, timedelta

random.seed(42)
OUT = os.path.join(os.path.dirname(__file__), "data")
START, DAYS = date(2025, 11, 1), 365

STORES = [
    # id, name, city, daily sales per menu item, waste habit (1 = normal)
    ("S01", "Strøget",          "København", 38, 0.9),
    ("S02", "Nørreport",        "København", 34, 1.0),
    ("S03", "Vesterbro",        "København", 26, 1.2),
    ("S04", "Nørrebro",         "København", 24, 1.1),
    ("S05", "Østerbro",         "København", 22, 0.8),
    ("S06", "København H",      "København", 36, 1.0),
    ("S07", "CPH Airport",      "Kastrup",   40, 1.3),
    ("S08", "Kongens Nytorv",   "København", 30, 1.0),
    ("S09", "Aarhus C",         "Aarhus",    28, 0.9),
    ("S10", "Odense C",         "Odense",    20, 1.1),
]

INGREDIENTS = [
    # id, name, unit, cost per unit (DKK), normal waste rate
    ("I01", "Avocado",           "pcs",  6.50,  0.05),
    ("I02", "Banana",            "g",    0.012, 0.04),
    ("I03", "Apple",             "g",    0.014, 0.02),
    ("I04", "Orange",            "g",    0.014, 0.02),
    ("I05", "Ginger",            "g",    0.045, 0.02),
    ("I06", "Spinach",           "g",    0.055, 0.06),
    ("I07", "Strawberry",        "g",    0.060, 0.07),
    ("I08", "Mango",             "g",    0.035, 0.05),
    ("I09", "Oat milk",          "ml",   0.021, 0.02),
    ("I10", "Milk",              "ml",   0.011, 0.03),
    ("I11", "Coffee beans",      "g",    0.185, 0.01),
    ("I12", "Sourdough bun",     "pcs",  4.00,  0.06),
    ("I13", "Tuna mix",          "g",    0.090, 0.04),
    ("I14", "Tomato",            "g",    0.023, 0.04),
    ("I15", "Cheese",            "g",    0.100, 0.02),
]

MENU = [
    # id, name, category, price (DKK), recipe
    ("J01", "Green Juice",       "juice",  62, {"I06": 40, "I03": 250, "I05": 10}),
    ("J02", "Orange Kick",       "juice",  59, {"I04": 400, "I05": 10}),
    ("J03", "Ginger Shot",       "juice",  29, {"I05": 40, "I03": 40}),
    ("M01", "Avo Shake",         "shake",  72, {"I01": 0.5, "I02": 100, "I09": 200}),
    ("M02", "Strawberry Shake",  "shake",  69, {"I07": 120, "I02": 100, "I10": 200}),
    ("M03", "Mango Shake",       "shake",  69, {"I08": 150, "I09": 200}),
    ("C01", "Espresso",          "coffee", 32, {"I11": 18}),
    ("C02", "Latte",             "coffee", 46, {"I11": 18, "I10": 220}),
    ("C03", "Oat Latte",         "coffee", 49, {"I11": 18, "I09": 220}),
    ("F01", "Tuna Avo Sandwich", "food",   75, {"I12": 1, "I13": 60, "I01": 0.5, "I14": 30}),
    ("F02", "Cheese Toast",      "food",   65, {"I12": 1, "I15": 40, "I14": 30}),
    ("F03", "Avo Toast",         "food",   69, {"I12": 1, "I01": 0.5, "I06": 15, "I14": 20}),
]

HIGH_WASTE = ("S08", "I01", 4.0)   # Kongens Nytorv, avocado, 4x the normal rate


def write(name, header, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"  {name:<16} {len(rows):>6} rows")


def demand_factor(day, category):
    # more juice and shakes in summer, more coffee in winter, busier Fri/Sat
    summer = (1 - math.cos(2 * math.pi * (day.timetuple().tm_yday - 15) / 365)) / 2
    season = {"juice": 0.8 + 0.4 * summer, "shake": 0.8 + 0.4 * summer,
              "coffee": 1.2 - 0.4 * summer, "food": 1.0}[category]
    weekday = 1.15 if day.weekday() in (4, 5) else 1.0
    return season * weekday


def main():
    print("Writing data/")
    write("stores.csv", ["store_id", "store_name", "city"], [s[:3] for s in STORES])
    write("ingredients.csv", ["ingredient_id", "ingredient_name", "unit", "cost_per_unit_dkk"],
          [i[:4] for i in INGREDIENTS])
    write("recipes.csv", ["menu_item_id", "menu_item_name", "category", "price_dkk", "ingredient_id", "quantity"],
          [(m[0], m[1], m[2], m[3], ing, qty) for m in MENU for ing, qty in m[4].items()])

    unit = {i[0]: i[2] for i in INGREDIENTS}
    waste_rate = {i[0]: i[4] for i in INGREDIENTS}
    sales, waste = [], []

    for d in range(DAYS):
        day = START + timedelta(days=d)
        for store_id, _, _, avg, habit in STORES:
            used = {}
            for item_id, _, category, _, recipe in MENU:
                qty = max(0, round(random.gauss(avg * demand_factor(day, category), avg * 0.2)))
                if qty:
                    sales.append((day, store_id, item_id, qty))
                for ing, per_item in recipe.items():
                    used[ing] = used.get(ing, 0) + qty * per_item

            for ing, qty_used in used.items():
                rate = waste_rate[ing] * habit
                if (store_id, ing) == HIGH_WASTE[:2]:
                    rate *= HIGH_WASTE[2]
                wasted = qty_used * rate * random.uniform(0.3, 1.7)
                if unit[ing] == "pcs":
                    wasted = round(wasted)
                else:
                    wasted = round(wasted / 10) * 10
                if wasted <= 0:
                    continue
                reason = random.choices(["expired", "end_of_day", "damaged"], weights=[5, 4, 1])[0]
                u = unit[ing]
                if u != "pcs" and random.random() < 0.08:  # typed in kg / l by mistake
                    wasted, u = wasted / 1000, {"g": "kg", "ml": "l"}[u]
                waste.append((day, store_id, ing, wasted, u, reason))

    write("sales.csv", ["sale_date", "store_id", "menu_item_id", "quantity"], sales)
    write("waste.csv", ["waste_date", "store_id", "ingredient_id", "quantity", "unit", "reason"], waste)


if __name__ == "__main__":
    main()
