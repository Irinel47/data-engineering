MODEL (
  name staging.stg_sales,
  kind FULL,
  audits (
    unique_combination_of_columns(columns := (sale_date, store_id, menu_item_id)),
    forall(criteria := (quantity > 0))
  )
);

SELECT
  sale_date::DATE  AS sale_date,
  store_id,
  menu_item_id,
  quantity::INT    AS quantity
FROM raw.sales
