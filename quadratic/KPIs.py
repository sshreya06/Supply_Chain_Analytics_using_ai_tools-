#code for creating a table "KPIs" for important KPIs using collected data, in quadratic

import pandas as pd

order_lines_raw = q.cells("'fact_order_line'!A:K")
order_agg_raw = q.cells("'fact_aggregate'!A:F")

def use_second_row_as_header(df):
    new_header = df.iloc[1]
    df = df[2:].reset_index(drop=True)
    df.columns = new_header
    return df

order_lines = use_second_row_as_header(order_lines_raw)
order_agg = use_second_row_as_header(order_agg_raw)

#KPIS:
# 1. Total order lines
total_order_lines = len(order_lines)

# 2. Line fill rate
line_fill_rate = (order_lines['In Full'] == '1').mean() * 100

# 3. Volume fill rate
volume_fill_rate = (order_lines['delivery_qty'].sum() / order_lines['order_qty'].sum()) * 100

# 4. Total orders
total_orders = len(order_agg)

# 5. On time delivery %
on_time_delivery = (order_agg['on_time'] == 1).mean() * 100

# 6. In full delivery %
in_full_delivery = (order_agg['in_full'] == '1').mean() * 100

# 7. OTIF %
otif = (order_agg['otif'] == '1').mean() * 100

# Build KPI table
kpi_df = pd.DataFrame({
    "KPI": [
        "Total Order Lines",
        "Line Fill Rate %",
        "Volume Fill Rate %",
        "Total Orders",
        "On Time Delivery %",
        "In Full Delivery %",
        "On Time In Full %"
    ],
    "Value": [
        total_order_lines,
        line_fill_rate,
        volume_fill_rate,
        total_orders,
        on_time_delivery,
        in_full_delivery,
        otif
    ]
})

kpi_df
