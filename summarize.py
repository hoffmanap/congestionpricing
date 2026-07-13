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
new_summary = df.groupby(
    ['year', 'month', 'day', 'hour', 'detection_region', 'date_str'],
    as_index=False
)['crz_entries'].sum()
new_data_list = new_summary.to_dict(orient='records')

# 2. Manage the Historical Archive
archive_file = 'data_archive.json'
if os.path.exists(archive_file):
    with open(archive_file, 'r') as f:
        full_data = json.load(f)
else:
    full_data = []


def record_key(row):
    """Unique key for a (date, hour, region) record."""
    return (row['date_str'], row['hour'], row['detection_region'])


# 3. Dedup: only append records we haven't already archived.
# (Fixes the gap flagged in the original script's own comment -- without
# this, re-fetched/overlapping rows from the source API get appended
# every single run, so the archive grows but never actually reflects
# new data.)
existing_keys = {record_key(r) for r in full_data}

new_records_to_add = [
    r for r in new_data_list if record_key(r) not in existing_keys
]

full_data.extend(new_records_to_add)

# 4. Save the updated master archive
with open(archive_file, 'w') as f:
    json.dump(full_data, f, indent=4)

print(f"Fetched {len(new_data_list)} aggregated rows, "
      f"{len(new_records_to_add)} were new and added to the archive.")
