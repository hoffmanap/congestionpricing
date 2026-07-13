import requests
import json
import sys

API_KEY = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else None
START_DATE = sys.argv[2]

BASE_URL = "https://data.ny.gov/resource/t6yz-b64h.json"
PAGE_SIZE = 50000       # Socrata's practical per-request cap, regardless of $limit
MAX_PAGES = 20          # safety cap: up to 1,000,000 rows in one run

headers = {"X-App-Token": API_KEY} if API_KEY else {}
all_rows = []
offset = 0

while True:
    params = {
        "$where": f"toll_hour >= '{START_DATE}'",
        "$order": "toll_hour ASC",
        "$limit": PAGE_SIZE,
        "$offset": offset,
    }
    resp = requests.get(BASE_URL, headers=headers, params=params, timeout=60)
    resp.raise_for_status()
    page = resp.json()
    all_rows.extend(page)
    print(f"Fetched page at offset {offset}: {len(page)} rows (running total: {len(all_rows)})")

    if len(page) < PAGE_SIZE:
        # fewer rows than a full page means we've reached the end of
        # whatever the source currently has available
        break

    offset += PAGE_SIZE
    if offset // PAGE_SIZE >= MAX_PAGES:
        print(f"Hit the {MAX_PAGES}-page safety cap -- will keep catching up on the next scheduled run.")
        break

with open("data.json", "w") as f:
    json.dump(all_rows, f)

print(f"Total rows written to data.json: {len(all_rows)}")
