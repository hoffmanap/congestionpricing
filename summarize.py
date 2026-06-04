import pandas as pd
import json

# Load the raw data
df = pd.read_json('data.json')
df['toll_hour'] = pd.to_datetime(df['toll_hour'])

# Aggregate: Calculate sum of entries by day of week and hour
df['hour'] = df['toll_hour'].dt.hour
df['day'] = df['toll_hour'].dt.day_name()
summary = df.groupby(['day', 'hour'])['crz_entries'].sum().reset_index()

# Save as a lightweight JSON
summary.to_json('summary.json', orient='records')
