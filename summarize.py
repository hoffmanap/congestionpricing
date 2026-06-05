import pandas as pd

# Load data
df = pd.read_json('data.json')
df['toll_hour'] = pd.to_datetime(df['toll_hour'])

# Identify the most recent date to use as a benchmark later
most_recent_date = df['toll_hour'].max().date()

# Aggregate: sum entries by day of week, hour, and region
df['hour'] = df['toll_hour'].dt.hour
df['day'] = df['toll_hour'].dt.day_name()
# Store date as string to identify 'most recent' day in the dashboard
df['date_str'] = df['toll_hour'].dt.date.astype(str)

summary = df.groupby(['day', 'hour', 'detection_region', 'date_str'])['crz_entries'].sum().reset_index()

# Save summary
summary.to_json('summary.json', orient='records')
