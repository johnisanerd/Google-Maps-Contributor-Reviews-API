"""
Google Maps Contributor Reviews API: A Quick Start Example
See more at: https://apify.com/johnvc/google-maps-contributor-reviews-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/google-maps-contributor-reviews-api/input-schema?fpr=9n7kx3

This script shows how to call the Google Maps Contributor Reviews API on Apify
from Python and read its structured JSON output. It pulls a reviewer's history
and prints each review with the place reviewed. Inputs are kept small so your
first call stays cheap.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
"""

import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

# Initialize the Apify client with your API token (read from .env)
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Build the Actor input.
# Inputs are kept small (one contributor) to keep this first run inexpensive:
# you are billed per review returned. Pass `contributorIds` to profile several.
run_input = {
    "contributorId": "107022004965696773221",  # a Google Maps contributor ID
    "hl": "en",                     # two-letter language code
    "maxResultsPerContributor": 10,
}

# Run the Actor and wait for it to finish
run = client.actor("johnvc/google-maps-contributor-reviews-api").call(run_input=run_input)
if run is None:
    raise SystemExit("The Actor run did not return a result.")

# Read structured results from the run's default dataset
# (apify-client 3.x returns a Run object; use .default_dataset_id, not run["..."])
items = list(client.dataset(run.default_dataset_id).iterate_items())
print(f"Returned {len(items)} review(s).\n")

# Show each review with the reviewer and the place reviewed.
for item in items:
    name = item.get("contributor_name", "")
    rating = item.get("rating")
    place = (item.get("place_info") or {}).get("title", "")
    snippet = item.get("snippet", "")
    print(f"{item.get('position')}. {name} rated {place}: {rating} stars")
    if snippet:
        print(f"   {snippet[:160]}\n")
