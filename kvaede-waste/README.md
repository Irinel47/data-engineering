# Kvaede – ingredient waste per store

A small end-to-end data project on a juice bar chain I made up: how much of
what each bar uses ends up in the bin, and where it's worse than the chain
average.

The idea: **items sold × recipe = ingredients used**, compared with the waste
the staff registered, in DKK.

```
generate_data.py → MotherDuck (raw) → SQLMesh (staging → marts) → Cube → D3 dashboard
```

![Dashboard](docs/dashboard.gif)

![Lineage](docs/lineage.gif)

## Files

| File | What it does |
|---|---|
| `generate_data.py` | Writes 5 CSVs to `data/`: stores, ingredients, recipes, daily sales and waste. Two things are planted: Kongens Nytorv wastes ~20% of its avocados, and 8% of waste rows are in kg or l instead of g or ml. |
| `load_to_motherduck.py` | Loads the CSVs into `kvaede.raw` in MotherDuck, unchanged. |
| `transform/models/staging/` | One model per raw table. `stg_waste` converts kg and l to g and ml. |
| `transform/models/intermediate/int_ingredient_usage.sql` | Sales × recipes = ingredients used per store and day. |
| `transform/models/marts/fct_ingredient_daily.sql` | Used vs wasted per day, store and ingredient, in units and DKK. |
| `transform/audits/`, `transform/tests/` | The audit checks no kg or l is left after the conversion. The unit test checks 4 Avo Shakes + 2 Avo Toasts = 3 avocados. Key and quantity audits are declared in each model. |
| `cube/model/cubes/ingredient_waste.yml` | The metrics: used value, wasted value and waste %. |
| `dashboard/index.html` | The D3 report (top GIF), reading Cube's REST API. |
| `docs/lineage.html` | Clickable map of the pipeline (second GIF). Opens without anything running. |

## Run it

Needs Python, Node.js and a free MotherDuck account. Commands are PowerShell, from this folder.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python generate_data.py
$env:MOTHERDUCK_TOKEN = "<your token>"
python load_to_motherduck.py

cd transform
sqlmesh test
sqlmesh plan

cd ..\cube
npm install
Copy-Item .env.example .env   # add your token
npm run dev                   # keep it running

# second terminal
cd dashboard
python -m http.server 8080    # http://localhost:8080
```

## What it finds

- Chain waste is 4.0% of the value used, from 3.0% (Østerbro) to 5.4% (Kongens Nytorv).
- Kongens Nytorv's problem is one ingredient: avocado at 20.5% vs 6.7% for the chain.
- Vesterbro is above the chain on almost every ingredient, so it's a habit, not one item.

All names and figures are invented.
