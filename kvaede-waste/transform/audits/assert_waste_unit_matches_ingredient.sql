-- no kg or l left after the conversion in stg_waste
AUDIT (name assert_waste_unit_matches_ingredient);

SELECT *
FROM @this_model
WHERE ingredient_unit IS NULL OR unit <> ingredient_unit
