"""Minimal client for the 99.co Singapore API on RapidAPI.

Set RAPIDAPI_KEY in your environment (or in a .env file at the repo root).
"""

import os
import re

import requests

HOST = "99-co-sg-api.p.rapidapi.com"


def _load_dotenv():
    """Read RAPIDAPI_KEY from a .env in the current folder or the repo root, if present."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    for path in (".env", os.path.join(root, ".env")):
        if os.path.exists(path):
            for line in open(path, encoding="utf-8"):
                key, sep, value = line.strip().partition("=")
                if sep and value and not key.startswith("#"):
                    os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def get(path, **params):
    """GET an endpoint and return the `data` object of the response."""
    key = os.environ.get("RAPIDAPI_KEY")
    if not key:
        raise SystemExit("Set RAPIDAPI_KEY first (see .env.example).")
    response = requests.get(
        f"https://{HOST}{path}",
        params={k: v for k, v in params.items() if v is not None},
        headers={"x-rapidapi-host": HOST, "x-rapidapi-key": key},
        timeout=60,
    )
    response.raise_for_status()
    body = response.json()
    if not body.get("success", True):
        raise RuntimeError(f"{path} failed: {body}")
    return body["data"]


def find_location(query, kind=None):
    """First /autocomplete match, optionally of one type: district, zone, subway_station, cluster."""
    for section in get("/autocomplete", query=query)["sections"]:
        for location in section["locations"]:
            if kind is None or location["type"] == kind:
                return location
    raise SystemExit(f"No 99.co location matches {query!r}" + (f" of type {kind}" if kind else ""))


_UNITS = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000}


def sgd(text):
    """Turn display strings like "S$ 13.390M", "+S$ 2.890M" or "S$ 3,323" into numbers."""
    if text is None:
        return None
    match = re.search(r"([+-]?)S\$\s*([\d,.]+)\s*([KMB])?", str(text))
    if not match:
        return None
    sign, number, unit = match.groups()
    value = float(number.replace(",", "")) * _UNITS.get(unit or "", 1)
    return -value if sign == "-" else value
