// 99.co Singapore API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs orchard

const HOST = '99-co-sg-api.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`99.co API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

const query = process.argv[2] ?? 'orchard';
const { sections } = await get('/autocomplete', { query });
const district = sections.flatMap((s) => s.locations).find((l) => l.type === 'district');
if (!district) throw new Error(`No 99.co district matches ${query}`);
console.log(`Using ${district.title} (${district.id})`);

const { results } = await get('/search-property', {
  listing_type: 'sale',
  query_ids: district.id,
  main_category: 'condo',
  page_size: 10,
});
console.log(`${results.totalCount} condos for sale`);
for (const row of results.listings) {
  console.log(`${row.priceFormatted.padStart(14)}  ${String(row.floorAreaSqft ?? '?').padStart(5)} sqft  ${row.title}`);
}
