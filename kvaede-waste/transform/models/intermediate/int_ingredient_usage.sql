-- items sold x recipe = ingredients used
MODEL (
  name intermediate.int_ingredient_usage,
  kind FULL,
  grain (usage_date, store_id, ingredient_id)
);

SELECT
  s.sale_date                     AS usage_date,
  s.store_id,
  r.ingredient_id,
  sum(s.quantity * r.quantity)    AS quantity_used
FROM staging.stg_sales AS s
JOIN staging.stg_recipes AS r USING (menu_item_id)
GROUP BY ALL
