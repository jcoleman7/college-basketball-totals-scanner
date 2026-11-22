"""Fetch NCAA basketball full-game totals from TheRundown."""

import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

BASE_URL = "https://therundown.io/api/v2"
SPORT_ID = 5
TOTAL_MARKET_ID = 3

BOOKS = {
    "19": "DraftKings",
    "22": "BetMGM",
    "23": "FanDuel",
}


def fetch_totals(game_date):
    """
    Fetch main full-game totals for DraftKings, BetMGM, and FanDuel.

    game_date format: YYYYMMDD or YYYY-MM-DD

    Returns one entry per sportsbook line.
    Does not average sportsbook totals.
    """

    api_key = os.getenv("THERUNDOWN_API_KEY")

    if not api_key:
        raise RuntimeError("THERUNDOWN_API_KEY is missing from .env")

    game_date = game_date.replace("-", "")

    formatted_date = (
        f"{game_date[:4]}-{game_date[4:6]}-{game_date[6:8]}"
    )

    url = (
        f"{BASE_URL}/sports/{SPORT_ID}/events/{formatted_date}"
    )

    response = requests.get(
        url,
        headers={"X-TheRundown-Key": api_key},
        params={
            "market_ids": str(TOTAL_MARKET_ID),
            "affiliate_ids": ",".join(BOOKS.keys()),
            "main_line": "true",
            "hide_closed": "true",
        },
        timeout=30,
    )

    response.raise_for_status()

    events = response.json().get("events", [])
    results = []

    for event in events:
        event_time = event.get("event_date")

        if not event_time:
            continue

        eastern_date = (
            datetime.fromisoformat(event_time.replace("Z", "+00:00"))
            .astimezone(ZoneInfo("America/New_York"))
            .strftime("%Y%m%d")
        )

        teams = event.get("teams", [])

        away_team = next(
            (team["name"] for team in teams if team.get("is_away")),
            None,
        )

        home_team = next(
            (team["name"] for team in teams if team.get("is_home")),
            None,
        )

        if not away_team or not home_team:
            continue

        for market in event.get("markets", []):

            if (
                market.get("market_id") != TOTAL_MARKET_ID
                or market.get("period_id") != 0
            ):
                continue

            for participant in market.get("participants", []):

                if participant.get("name") != "Over":
                    continue

                for line in participant.get("lines", []):

                    for book_id, price_data in line.get(
                        "prices", {}
                    ).items():

                        if book_id not in BOOKS:
                            continue

                        if not price_data.get("is_main_line", False):
                            continue

                        results.append({
                            "away_team": away_team,
                            "home_team": home_team,
                            "game_date": eastern_date,
                            "book": BOOKS[book_id],
                            "total": float(line["value"]),
                            "odds": price_data.get("price"),
                        })

    return results
