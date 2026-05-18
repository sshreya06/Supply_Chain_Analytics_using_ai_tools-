| table_name         | column_name          | data_type        |
| ------------------ | -------------------- | ---------------- |
| dim_customers      | customer_id          | bigint           |
| dim_customers      | customer_name        | text             |
| dim_customers      | city                 | text             |
| dim_customers      | currency             | text             |
| dim_products       | product_id           | bigint           |
| dim_products       | price_INR            | bigint           |
| dim_products       | product_name         | text             |
| dim_products       | category             | text             |
| dim_products       | price_USD            | double precision |
| dim_targets_orders | ontime_target%       | bigint           |
| dim_targets_orders | customer_id          | bigint           |
| dim_targets_orders | infull_target%       | bigint           |
| dim_targets_orders | otif_target%         | bigint           |
| fact_aggregate     | in_full              | text             |
| fact_aggregate     | on_time              | bigint           |
| fact_aggregate     | otif                 | text             |
| fact_aggregate     | customer_id          | bigint           |
| fact_aggregate     | order_id             | text             |
| fact_aggregate     | order_placement_date | date             |
| fact_order_line    | order_placement_date | date             |
| fact_order_line    | product_id           | bigint           |
| fact_order_line    | order_qty            | bigint           |
| fact_order_line    | delivery_qty         | bigint           |
| fact_order_line    | customer_id          | bigint           |
| fact_order_line    | On Time              | text             |
| fact_order_line    | order_id             | text             |
| fact_order_line    | agreed_delivery_date | text             |
| fact_order_line    | actual_delivery_date | text             |
| fact_order_line    | In Full              | text             |
| fact_order_line    | On Time In Full      | text             |