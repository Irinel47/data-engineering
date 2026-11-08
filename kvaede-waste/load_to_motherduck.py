"""Loads the CSV files into MotherDuck as raw tables, untouched."""

import argparse
import os

import duckdb

FILES = ["stores", "ingredients", "recipes", "sales", "waste"]
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data").replace("\\", "/")

ap = argparse.ArgumentParser()
ap.add_argument("--reset", action="store_true", help="drop and recreate the kvaede database first")
ap.add_argument("--local", action="store_true", help="write to data/kvaede.duckdb instead of MotherDuck")
args = ap.parse_args()

if args.local:
    con = duckdb.connect(f"{DATA}/kvaede.duckdb")
else:
    con = duckdb.connect("md:")  # token from MOTHERDUCK_TOKEN
    if args.reset:
        con.execute("DROP DATABASE IF EXISTS kvaede CASCADE")
    con.execute("CREATE DATABASE IF NOT EXISTS kvaede")
    con.execute("USE kvaede")

con.execute("CREATE SCHEMA IF NOT EXISTS raw")
for name in FILES:
    con.execute(f"CREATE OR REPLACE TABLE raw.{name} AS SELECT * FROM read_csv('{DATA}/{name}.csv')")
    rows = con.execute(f"SELECT count(*) FROM raw.{name}").fetchone()[0]
    print(f"raw.{name:<12} {rows:>6} rows")
