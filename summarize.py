import pandas as pd
import json

# Load data explicitly
with open('data.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Ensure columns exist before converting
if 'toll_hour' in df.columns:
    df['toll_hour'] = pd.to_datetime(df['toll_hour'])
    df['hour'] = df['toll_hour'].dt.hour
    df['day'] = df['toll_hour'].dt.day_name()
    df['date_str'] = df['toll_hour'].dt.date.astype(str)

# Ensure crz_entries is numeric (handles the '0' string issue)
df['crz_entries'] = pd.to_numeric(df['crz_entries'], errors='coerce').fillna(0)

# Check if detection_region exists, otherwise use a placeholder
if 'detection_region' not in df.columns:
    df['detection_region'] = 'Unknown'

# Aggregate
summary = df.groupby(['day', 'hour', 'detection_region', 'date_str'])['crz_entries'].sum().reset_index()

# Save summary
summary.to_json('summary.json', orient='records')
