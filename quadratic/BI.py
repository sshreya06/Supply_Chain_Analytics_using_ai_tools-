# example code for creating Business Insights (BI) using quadratic
# (refer the screenshots to view the graph)


# 1. revenue loss due to undelivered orders (by customers)
import pandas as pd
import plotly.express as px      #quadratic uses plotly.express for plotting graphs instead of traditional matplotlib.pyplot

fs_raw = q.cells("'fact_summary'!A:Z")

def use_second_row_as_header(df):
    new_header = df.iloc[1]
    df = df[2:].reset_index(drop=True)
    df.columns = new_header
    return df

fact_summary = use_second_row_as_header(fs_raw)

fact_summary["total_amount"] = pd.to_numeric(
    fact_summary["total_amount"], errors="coerce"
)

fact_summary["customer_id"] = (
    fact_summary["customer_id"]
    .astype(str)
    .str.strip()
)

# filter undelivered orders
undelivered = fact_summary[fact_summary["In Full"] == '0']

# calculate revenue loss
loss_by_customer = (
    undelivered
    .groupby("customer_id", as_index=False)["total_amount"]
    .sum()
    .rename(columns={"total_amount": "revenue_loss"})
    .sort_values("revenue_loss", ascending=False)
)
 
# visualise by plotting a bar graph
fig = px.bar(
    loss_by_customer,
    x="customer_id",
    y="revenue_loss",
    title="1. Revenue Loss Due to Undelivered Orders (by Customer)",
    labels={
        "customer_id": "Customer ID",
        "revenue_loss": "Revenue Loss (INR)"
    }
)

fig