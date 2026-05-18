#code for creating a date dimensions table "dim_date" in quadratic
import pandas as pd

start_date = '2025-03-01'
end_date = '2025-03-31'
dates = pd.date_range(start=start_date, end=end_date)

df = pd.DataFrame({'date': dates})

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

df['day_name'] = df['date'].dt.day_name()
df['month_name'] = df['date'].dt.month_name()

df['week_of_year'] = df['date'].dt.isocalendar().week

df['is_weekend'] = df['day_name'].isin(['Saturday', 'Sunday'])

df['is_weekend'] = df['is_weekend'].map({True: 'TRUE', False: 'FALSE'})

df['date'] = df['date'].dt.strftime('%Y-%m-%d')

df
