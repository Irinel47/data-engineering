MODEL (
  name staging.stg_stores,
  kind FULL,
  audits (unique_values(columns := (store_id)), not_null(columns := (store_id, store_name)))
);

SELECT
  store_id,
  store_name,
  city
FROM raw.stores
