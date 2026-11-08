MODEL (
  name staging.stg_recipes,
  kind FULL,
  audits (
    unique_combination_of_columns(columns := (menu_item_id, ingredient_id)),
    forall(criteria := (quantity > 0))
  )
);

SELECT
  menu_item_id,
  menu_item_name,
  category,
  price_dkk::DOUBLE  AS price_dkk,
  ingredient_id,
  quantity::DOUBLE   AS quantity
FROM raw.recipes
