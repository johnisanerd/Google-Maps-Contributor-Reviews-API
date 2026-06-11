"""
Google Maps Contributor Reviews API: Batch Multi-Contributor Example
See more at: https://apify.com/johnvc/google-maps-contributor-reviews-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/google-maps-contributor-reviews-api/input-schema?fpr=9n7kx3

This script shows the batch capability of the Google Maps Contributor Reviews
API on Apify: pass a list of contributor IDs with the `contributorIds` input
and the Actor pulls each reviewer's history in a single run, tagging every
review with its `contributor_id`. That makes it easy to profile several
reviewers side by side. Inputs are kept small so your first call stays cheap.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
"""

import os
from collections import defaultdict
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

# Initialize the Apify client with your API token (read from .env)
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Build the Actor input.
# This run uses the `contributorIds` list to profile several reviewers at once.
# Each review row carries the `contributor_id` it came from. The contributor ID
# is the long numeric ID from a reviewer's Google Maps profile; add more IDs to
# the list to compare more reviewers. Inputs are kept small to keep this first
# run inexpensive: you are billed per review returned.
run_input = {
    "contributorIds": [
        "107022004965696773221",
        # "another-contributor-id-here",  # add more reviewer IDs to compare
    ],
    "hl": "en",                    # two-letter language code
    "maxResultsPerContributor": 10,
}

# Run the Actor and wait for it to finish
run = client.actor("johnvc/google-maps-contributor-reviews-api").call(run_input=run_input)
if run is None:
    raise SystemExit("The Actor run did not return a result.")

# Read structured results from the run's default dataset
# (apify-client 3.x returns a Run object; use .default_dataset_id, not run["..."])
items = list(client.dataset(run.default_dataset_id).iterate_items())
print(f"Returned {len(items)} review(s) across {len(run_input['contributorIds'])} contributor(s).\n")

# Group the reviews by their contributor so the batch structure is visible.
by_contributor = defaultdict(list)
for item in items:
    by_contributor[item.get("contributor_id", "")].append(item)

# Print a short report per contributor.
for contributor_id, reviews in by_contributor.items():
    name = reviews[0].get("contributor_name", contributor_id) if reviews else contributor_id
    print(f"=== {name} ({contributor_id}): {len(reviews)} review(s) ===")
    for item in reviews:
        rating = item.get("rating")
        place = (item.get("place_info") or {}).get("title", "")
        print(f"  {item.get('position')}. {place}: {rating} stars")
    print()
