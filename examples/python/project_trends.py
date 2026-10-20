"""Price trend and recent sales for one Singapore project, area or district.

    python project_trends.py "orchard bel air"
    python project_trends.py "orchard" --kind district --type rent

Transactions are display strings ("S$ 13.390M", "4,029"), so client.sgd() turns them into
numbers before any arithmetic.
"""

import argparse

from client import find_location, get, sgd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("place", help="a project, area or district name")
    parser.add_argument("--kind", default="cluster", choices=["cluster", "zone", "district"],
                        help="cluster = a project (default)")
    parser.add_argument("--type", default="sale", choices=["sale", "rent"])
    parser.add_argument("--time-frame", default="5y", choices=["10y", "5y", "1y", "6m", "3m", "1m"])
    args = parser.parse_args()

    place = find_location(args.place, kind=args.kind)
    print(f"{place['title']} ({place['type']}, {place['id']})\n")

    trends = get("/transaction-trends", query_ids=place["id"], type=args.type, time_frame=args.time_frame)
    print(f"Average {args.type} price by period, {trends.get('period')}:")
    for point in trends.get("trend") or []:
        print(f"  {point['period']:<8} {point['averagePriceFormatted']:>12}  ({point['transactionCount']} transactions)")
    summary = trends.get("summary") or {}
    print(f"  range {summary.get('lowestPrice')} to {summary.get('highestPrice')}, average {summary.get('averagePsf')}\n")

    deals = get("/transactions", query_ids=place["id"], type=args.type, page_num=1)["transactions"]
    print(f"Latest {len(deals)} transactions (20 a page):")
    for deal in deals:
        price = sgd(deal.get("price"))
        profit = sgd(deal.get("profit"))
        gain = f"  {profit / (price - profit):+.0%} over {deal.get('holding_period')} yrs" if price and profit else ""
        # Columns depend on the location: a project returns blk/unit/beds, a wider area
        # returns address/type. The response's `columns` list says which you got.
        where = deal.get("address") or f"blk {deal.get('blk')} #{deal.get('unit')}"
        print(f"  {deal.get('date'):<8} {deal.get('price'):>12}  {deal.get('area'):>6} sqft  {where}  {deal.get('sale_type')}{gain}")


if __name__ == "__main__":
    main()
