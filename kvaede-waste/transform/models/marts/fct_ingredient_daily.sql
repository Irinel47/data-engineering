-- used vs wasted per day, store and ingredient, in units and DKK
MODEL (
  name marts.fct_ingredient_daily,
  kind FULL,
  grain (date, store_id, ingredient_id),
  audits (unique_combination_of_columns(columns := (date, store_id, ingredient_id)))
);

WITH waste AS (
  SELECT waste_date AS date, store_id, ingredient_id, sum(quantity) AS quantity_wasted
  FROM staging.stg_waste
  GROUP BY ALL
)
SELECT
  u.usage_date                                  AS date,
  u.store_id,
  st.store_name,
  st.city,
  u.ingredient_id,
  i.ingredient_name,
  i.unit,
  u.quantity_used,
  coalesce(w.quantity_wasted, 0)                AS quantity_wasted,
  u.quantity_used * i.cost_per_unit_dkk         AS used_value_dkk,
  coalesce(w.quantity_wasted, 0) * i.cost_per_unit_dkk AS wasted_value_dkk
FROM intermediate.int_ingredient_usage AS u
LEFT JOIN waste AS w
  ON w.date = u.usage_date AND w.store_id = u.store_id AND w.ingredient_id = u.ingredient_id
JOIN staging.stg_stores AS st ON st.store_id = u.store_id
JOIN staging.stg_ingredients AS i ON i.ingredient_id = u.ingredient_id
