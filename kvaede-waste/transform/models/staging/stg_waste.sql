-- staff sometimes type kg or l instead of g or ml, so I convert to the ingredient's unit
MODEL (
  name staging.stg_waste,
  kind FULL,
  audits (
    forall(criteria := (quantity > 0)),
    assert_waste_unit_matches_ingredient
  )
);

SELECT
  w.waste_date::DATE   AS waste_date,
  w.store_id,
  w.ingredient_id,
  w.reason,
  w.quantity           AS quantity_entered,
  w.unit               AS unit_entered,
  CASE WHEN w.unit IN ('kg', 'l') THEN w.quantity * 1000 ELSE w.quantity END AS quantity,
  CASE w.unit WHEN 'kg' THEN 'g' WHEN 'l' THEN 'ml' ELSE w.unit END          AS unit,
  i.unit               AS ingredient_unit
FROM raw.waste AS w
LEFT JOIN staging.stg_ingredients AS i USING (ingredient_id)
