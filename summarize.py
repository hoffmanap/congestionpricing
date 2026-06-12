import pandas as pd
import json
import os

# 1. Load the new data
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

# Aggregate new data
new_summary = df.groupby(['year', 'month', 'day', 'hour', 'detection_region', 'date_str'], as_index=False)['crz_entries'].sum()
new_data_list = new_summary.to_dict(orient='records')

# 2. Manage the Historical Archive
archive_file = 'data_archive.json'

if os.path.exists(archive_file):
    with open(archive_file, 'r') as f:
        full_data = json.load(f)
else:
    full_data = []

# 3. Append new data to the archive
# Note: In a production environment, you may want to add a check here to ensure 
# you aren't appending the exact same date_str/region twice.
full_data.extend(new_data_list)

# 4. Save the updated master archive
with open(archive_file, 'w') as f:
    json.dump(full_data, f, indent=4)
