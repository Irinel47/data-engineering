MODEL (
  name staging.stg_ingredients,
  kind FULL,
  audits (
    unique_values(columns := (ingredient_id)),
    accepted_values(column := unit, is_in := ('g', 'ml', 'pcs'))
  )
);

SELECT
  ingredient_id,
  ingredient_name,
  unit,
  cost_per_unit_dkk::DOUBLE AS cost_per_unit_dkk
FROM raw.ingredients
