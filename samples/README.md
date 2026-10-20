# Sample responses

Example `200` responses for six 99.co Singapore API endpoints. Long arrays are cut to their
first few items, and agent names, phone numbers and contact lines are removed. Field names
and values are otherwise unchanged.

| File | Request | Source |
|---|---|---|
| `autocomplete.json` | `GET /autocomplete?query=orchard` | API documentation |
| `search-property.json` | `GET /search-property?listing_type=rent&query_ids=dtdistrict09&rooms=2,2` | Live response, 20 Oct 2026 |
| `listing-details.json` | `GET /listing-details?listing_id=nUakgpSzMK6eJr9KHKnhZp` | Live response, 20 Oct 2026 |
| `transactions.json` | `GET /transactions?query_ids=deGCf9CT83sWPVxWaGQGy7w5&type=sale` | API documentation |
| `transaction-trends.json` | `GET /transaction-trends?query_ids=deGCf9CT83sWPVxWaGQGy7w5&type=sale&time_frame=5y` | API documentation |
| `new-projects.json` | `GET /new-projects?listing_type=sale` | API documentation |

The search and listing samples are live responses because the live records carry more
fields than the documented examples (`buildupSqft`, `landAreaSqft`, `leaseType`, `postedAt`
on search rows; `lease`, `status`, `isOwnerListing`, `hdbUnitConfiguration` and more on
listings) and `address.districtNumber` is a number (`9`), not the documented `"D11"`.

They are useful for writing parsers and tests before you subscribe. Live data changes
daily, so do not hard-code these values.
