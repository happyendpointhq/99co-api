# 99.co API and Scraper

The 99.co API returns Singapore property data from 99.co as JSON: condo, HDB and landed
listings for sale and rent, full listing records, new launch projects, project details,
sold and rental transactions, price trends, nearby amenities and the public agent
directory. 99.co has no public developer API for its listings, so this REST API is the way
to use its data in your own code without maintaining a 99.co scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/99co-api?utm_source=github&utm_medium=readme&utm_campaign=99co-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/99-co-sg-api
- Product page: https://happyendpoint.com/library/99co-api?utm_source=github&utm_medium=readme&utm_campaign=99co-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://99-co-sg-api.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 16, all `GET` |
| Coverage | Singapore: residential, commercial, industrial and land |
| Property types | Condos, HDB flats, landed homes, plus room rentals |
| Currency and units | Singapore dollars (S$), square feet |
| Format | JSON, every response wrapped in `{"success": true, "data": {...}}` |

---

## What data you get

**Search**
- Sale and rent listings by district, area, MRT station, project or the whole island
- Filters for property type and sub-type, segment, price, bedrooms, bathrooms, furnishing, tenure, room rentals and selling-point tags
- Radius search around a point, sort by relevance or distance, up to 50 results a page
- Result counts without the listings (`/search-count`)

**Listings**
- Price, price per square foot, beds, baths, floor area, built year, furnishing, lease type
- Address with postal code, district number, region, neighbourhood and coordinates
- Nearest MRT with walking time, photos, floor plans, videos and virtual tours
- Full records: description, details table, lease, amenities, recent transactions in the project, comparison insights, project overview, similar listings

**Projects**
- New launch and upcoming developments with price ranges
- Project details, facilities, floor plans, active units and nearby amenities

**Market**
- Sold and rental transactions for a project, area or district, 20 a page
- Price trends over 1 month to 10 years, with lowest, highest and average price per square foot

**Agents**
- Public agent directory and profiles with agency and listing breakdown

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/99-co-sg-api). Copy `.env.example` to `.env` and paste your key.

### 2. Make a request

Searches take location ids, not place names. Look one up first:

```bash
curl "https://99-co-sg-api.p.rapidapi.com/autocomplete?query=orchard" \
  -H "x-rapidapi-host: 99-co-sg-api.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"

curl "https://99-co-sg-api.p.rapidapi.com/search-property?listing_type=rent&query_ids=dtdistrict09&rooms=2,2&page_size=10" \
  -H "x-rapidapi-host: 99-co-sg-api.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py orchard
```

```python
from client import find_location, get

district = find_location("orchard", kind="district")  # dtdistrict09
results = get("/search-property", listing_type="rent", query_ids=district["id"], rooms="2,2")
for row in results["results"]["listings"]:
    print(row["priceFormatted"], row["floorAreaSqft"], row["title"])
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs orchard
```

---

## Example response

One row from `GET /search-property?listing_type=rent&query_ids=dtdistrict09&rooms=2,2`,
trimmed, from a live call on 20 October 2026. The full responses are in [`samples/`](samples/).

```json
{
  "success": true,
  "data": {
    "results": {
      "title": "Residential Properties for Rent in District 9",
      "totalCount": 317,
      "listings": [
        {
          "id": "nUakgpSzMK6eJr9KHKnhZp",
          "title": "2+1 Bed Condo for Rent in Helios Residences",
          "mainCategory": "condo",
          "propertySegment": "residential",
          "price": 8200,
          "priceFormatted": "S$ 8,200",
          "psf": "S$ 6.4",
          "beds": "2",
          "bathrooms": 2,
          "floorAreaSqft": 1281,
          "builtYear": "2011",
          "furnishing": "Partially furnished",
          "estMortgage": null,
          "neighbourhood": "Cairnhill",
          "nearestMrt": { "name": "Newton MRT", "durationFormatted": "8 mins", "walkOrTransit": "walk" }
        }
      ]
    },
    "nearbyResults": null
  }
}
```

---

## Endpoints

Base URL: `https://99-co-sg-api.p.rapidapi.com`

### Search and locations

| Endpoint | Returns |
|---|---|
| `GET /autocomplete` | Location and project ids for a typed name (districts, areas, MRT stations, projects) |
| `GET /search-property` | Sale or rent listings with all filters |
| `GET /search-count` | The number of listings a search would return |

### Listings

| Endpoint | Returns |
|---|---|
| `GET /listing-details` | The full listing record |
| `GET /listing-details-by-url` | The same, from a 99.co listing URL |
| `GET /similar-listings` | Comparable listings for one listing |

### Projects

| Endpoint | Returns |
|---|---|
| `GET /new-projects` | New launch and upcoming developments |
| `GET /project-details` | One project: facilities, floor plans, active units |
| `GET /project-details-by-url` | The same, from a 99.co project URL |
| `GET /project-nearby` | Amenities near a project: MRT, schools, supermarkets, parks |

### Market data

| Endpoint | Returns |
|---|---|
| `GET /transactions` | Sold or rental transactions for a project, area or district |
| `GET /transaction-trends` | Average price over time, price range and average psf |

### Agents

| Endpoint | Returns |
|---|---|
| `GET /agents` | The public agent directory |
| `GET /agent-details` | One public agent profile |
| `GET /status` | Service health |

---

## Things to know about the data

These come from building against the API and from live responses. They are the mistakes
that produce wrong numbers rather than errors.

- **Location ids carry their type.** Districts look like `dtdistrict09`, areas start with
  `zo`, MRT stations with `sg-mrt-`, projects (clusters) with `de`. Leave `query_type` blank
  and it is derived from the id. `/autocomplete` can also return Google places with
  `"type": "google"` and ids like `ChIJB7XD...`; those are not 99.co location ids, so
  `client.find_location()` filters by type.
- **On rentals, `psf` is monthly rent per square foot.** The live Orchard example above is
  S$ 8,200 a month for 1,281 sqft, shown as `"psf": "S$ 6.4"`. On sale listings the same
  field is the asking price per square foot. Never mix the two in one column.
- **"2+1 Bed" counts as two bedrooms.** A `rooms=2,2` search returns "2+1" units (two
  bedrooms plus a study or utility room) alongside plain two-beds. Read the title or
  `/listing-details` if the extra room matters.
- **`rooms` and `bathrooms` are `min,max` ranges.** `2,2` means exactly two, `2,3` two or
  three, and `0` is a studio. `beds` comes back as a string (`"2"`), `bathrooms` as a number.
- **Prices come both as numbers and as display strings.** Search rows have `price` (a
  number) and `priceFormatted`; listing records have `price` as text (`"S$ 8,200"`) and
  `priceValue` as the number. Transactions are text only: `"price": "S$ 13.390M"`,
  `"area": "4,029"`, `"profit": "+S$ 2.890M"`. `client.sgd()` converts these.
- **Timestamps are in microseconds.** `postedAt` on the live listing is `1792501149518961`,
  which is 20 October 2026 only after dividing by 1,000,000.
- **`districtNumber` is a number on live data.** The documentation shows `"D11"`, the live
  record has `9`.
- **Rental transactions are banded.** The transaction history on a live rental listing gives
  sizes as ranges (`"1,900 - 2,000 sqft"`) and bedrooms as `"3-room"`, not exact values.
- **`estMortgage` is often null.** It was null on every live rental row we checked; it is a
  display estimate on sale listings, not a quote.
- **Market endpoints do not take the whole island.** `/transactions` and
  `/transaction-trends` need a project, area or district id; `singapore` is not accepted.

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | District lookup, two-bed rentals in it, one full listing record |
| [`examples/python/project_trends.py`](examples/python/project_trends.py) | Price trend and the latest transactions for a project, area or district, with resale gains |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | District lookup and condos for sale in Node 18+, no dependencies |
| [`samples/`](samples/) | Example responses for six endpoints |

---

## API or your own 99.co scraper

A homemade 99.co scraper has to follow the site's search URLs, page structure and anti-bot
rules, and it breaks when any of them change. This API returns the same listings, projects
and transactions as documented JSON with a stable contract, so the work you keep is the
analysis. If you need a one-off Singapore file or a recurring export rather than API calls,
[contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=99co-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can query Singapore
property data without code:

```json
{
  "mcpServers": {
    "99co": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: 99-co-sg-api.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Is there a 99.co API?

99.co does not publish a public developer API for its listings. This API, built and
maintained by Happy Endpoint and independent of 99.co, provides that access as REST and
JSON.

### Is there a free 99.co API?

Yes. The RapidAPI listing has a free plan, and every endpoint can be tried on it.

### How do I scrape 99.co data in Python?

Install `requests`, set `RAPIDAPI_KEY`, and call the endpoints with the two RapidAPI
headers. [`examples/python/client.py`](examples/python/client.py) is a small client with a
location lookup and a price parser, and the other scripts in that folder are ready to run.

### Can I get HDB and condo transaction prices in Singapore?

Yes. `/transactions` returns sold or rental transactions for a project, area or district,
20 a page, and `/transaction-trends` gives the average price over time with the price range
and average psf. [`project_trends.py`](examples/python/project_trends.py) prints both.

### Can I track new launch condos?

Yes. `/new-projects` lists new launch and upcoming developments with price ranges, and
`/project-details` adds facilities, floor plans and the units on the market.

### Where is the 99.co API documentation?

Every endpoint, parameter and response is documented on the RapidAPI listing, and the
endpoint table above summarises them. Example responses are in [`samples/`](samples/).

### Do you cover other property portals?

Yes, including Bayut and PropertyFinder in the UAE, Aqar and Wasalt in Saudi Arabia,
Rent.com and Realtor.com in the US, and Suumo in Japan. See the
[API library](https://happyendpoint.com/library?utm_source=github&utm_medium=readme&utm_campaign=99co-api).

---

## Related repos

- [awesome-real-estate-apis](https://github.com/happyendpointhq/awesome-real-estate-apis) - real estate APIs and data sources by country, including free and official ones
- [uae-real-estate-api](https://github.com/happyendpointhq/uae-real-estate-api) - Bayut and PropertyFinder through one API, with asking-vs-paid examples
- [rent-com-api](https://github.com/happyendpointhq/rent-com-api) - US rental listings, floor plans and rent estimates
- [bayut-api-python-examples](https://github.com/happyendpointhq/bayut-api-python-examples) - more Python patterns for a property API

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: happyendpointhq@gmail.com

## Licence

MIT. See [LICENSE](LICENSE).
