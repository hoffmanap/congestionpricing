import pandas as pd
import json

with open('data.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Ensure numeric columns exist
df['crz_entries'] = pd.to_numeric(df['crz_entries'], errors='coerce').fillna(0)

# Convert dates if they exist
if 'toll_hour' in df.columns:
    df['toll_hour'] = pd.to_datetime(df['toll_hour'])
    df['hour'] = df['toll_hour'].dt.hour
    df['day'] = df['toll_hour'].dt.day_name()
    df['date_str'] = df['toll_hour'].dt.date.astype(str)
else:
    # Fallback if toll_hour is missing
    df['hour'] = 0
    df['day'] = 'Unknown'
    df['date_str'] = 'Unknown'

# Ensure detection_region exists
if 'detection_region' not in df.columns:
    df['detection_region'] = 'Unknown'

# IMPORTANT: as_index=False keeps the grouping columns as actual columns in the JSON
summary = df.groupby(['day', 'hour', 'detection_region', 'date_str'], as_index=False)['crz_entries'].sum()

# Save summary
summary.to_json('summary.json', orient='records')
