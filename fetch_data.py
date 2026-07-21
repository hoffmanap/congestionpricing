import requests
import json
import sys
import time

API_KEY = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else None
START_DATE = sys.argv[2]

BASE_URL = "https://data.ny.gov/resource/t6yz-b64h.json"
PAGE_SIZE = 50000       # Socrata's practical per-request cap, regardless of $limit
MAX_PAGES = 20          # safety cap: up to 1,000,000 rows in one run
REQUEST_TIMEOUT = 120   # deep-offset pages get slower to compute on Socrata's end
MAX_RETRIES = 4         # transient timeouts/connection errors per page
# NOTE: $order includes ":id ASC" as a tiebreaker. toll_hour alone isn't
# unique -- many rows (different regions/vehicle classes) share the same
# timestamp -- so offset-based pagination on toll_hour alone isn't
# guaranteed stable between requests. That instability can duplicate or
# skip rows across page boundaries. :id (Socrata's internal row id) is
# unique, so adding it as a secondary sort makes paging deterministic.

headers = {"X-App-Token": API_KEY} if API_KEY else {}
all_rows = []
offset = 0

def fetch_page(offset):
    params = {
        "$where": f"toll_hour >= '{START_DATE}'",
        "$order": "toll_hour ASC, :id ASC",
        "$limit": PAGE_SIZE,
        "$offset": offset,
    }
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(BASE_URL, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            return resp.json()
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            last_err = e
            wait = 5 * attempt
            print(f"  Page at offset {offset} failed (attempt {attempt}/{MAX_RETRIES}): {e}. Retrying in {wait}s...")
            time.sleep(wait)
    raise last_err

try:
    while True:
        page = fetch_page(offset)
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
except Exception as e:
    # Even if a page ultimately fails after retries, don't throw away
    # whatever was already fetched -- save it, and let the next scheduled
    # run pick up from the latest date this run managed to reach.
    print(f"Stopping early after a page failed permanently: {e}")
    print(f"Saving the {len(all_rows)} rows fetched so far -- the next run will continue from here.")

with open("data.json", "w") as f:
    json.dump(all_rows, f)

print(f"Total rows written to data.json: {len(all_rows)}")

with open("data.json", "w") as f:
    json.dump(all_rows, f)

print(f"Total rows written to data.json: {len(all_rows)}")
