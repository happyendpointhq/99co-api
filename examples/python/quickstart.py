"""Find a district, search two-bedroom rentals in it, then open the first listing.

    python quickstart.py "orchard"
"""

import sys

from client import find_location, get

query = sys.argv[1] if len(sys.argv) > 1 else "orchard"

# 1. Resolve a place name to a location id. Searches take ids such as dtdistrict09, not names.
district = find_location(query, kind="district")
print(f"Using {district['title']} ({district['id']})")

# 2. Two-bedroom residential rentals in that district. rooms is a min,max range.
results = get(
    "/search-property",
    listing_type="rent",
    query_ids=district["id"],
    property_segments="residential",
    rooms="2,2",
    page_size=10,
)["results"]
print(f"{results['totalCount']:,} listings, showing {len(results['listings'])}\n")
for row in results["listings"]:
    # For rentals, psf is monthly rent per square foot, not a sale price per square foot.
    print(
        f"{row['priceFormatted']:>12}  {row.get('floorAreaSqft') or '?':>5} sqft  {row.get('psf') or '':>10} psf  "
        f"{row['mainCategory']:<6} {row['title']}  ({row['id']})"
    )

# 3. Full record for the first result: details table, project overview, nearest MRT.
if results["listings"]:
    listing = get("/listing-details", listing_id=results["listings"][0]["id"])
    # districtNumber is a plain number on live responses (9), not "D9".
    print(f"\n{listing['title']}, {listing['address']['formatted']} (District {listing['address']['districtNumber']})")
    print(f"Price: {listing['price']} (priceValue {listing['priceValue']})")
    for label, value in (listing.get("details") or {}).items():
        print(f"  {label}: {value}")
    if listing.get("nearestMrt"):
        print(f"  {listing['nearestMrt']['text']}")
