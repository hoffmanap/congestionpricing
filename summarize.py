import pandas as pd
import json

with open('data.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)
df['toll_hour'] = pd.to_datetime(df['toll_hour'])

# Extract temporal features
df['hour'] = df['toll_hour'].dt.hour
df['day'] = df['toll_hour'].dt.day_name()
df['month'] = df['toll_hour'].dt.month_name()
df['year'] = df['toll_hour'].dt.year
df['date_str'] = df['toll_hour'].dt.date.astype(str)

# Ensure numeric and region fields
df['crz_entries'] = pd.to_numeric(df['crz_entries'], errors='coerce').fillna(0)
if 'detection_region' not in df.columns:
    df['detection_region'] = 'Unknown'

# Aggregate by all dimensions
summary = df.groupby(['year', 'month', 'day', 'hour', 'detection_region', 'date_str'], as_index=False)['crz_entries'].sum()

summary.to_json('summary.json', orient='records')
