import re
import requests
from datetime import datetime

BASE_URLS = {
    "men": "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard",
    "women": "https://site.api.espn.com/apis/site/v2/sports/basketball/womens-college-basketball/scoreboard",
}

LEAGUES = {
    "men": "mens-college-basketball",
    "women": "womens-college-basketball",
}

SEASON = 2027

_D1_TEAM_CACHE = {}

# Identify the request as a normal browser-style request.
ESPN_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.espn.com/",
}


def fetch_d1_team_ids(gender):
    if gender not in LEAGUES:
        raise ValueError("Gender must be 'men' or 'women'.")

    if gender in _D1_TEAM_CACHE:
        return _D1_TEAM_CACHE[gender]

    league = LEAGUES[gender]

    root = (
        f"https://sports.core.api.espn.com/v2/sports/basketball/"
        f"leagues/{league}/seasons/{SEASON}/types/2/groups/"
    )

    response = requests.get(
        root + "50/children",
        params={"limit": 1000},
        headers=ESPN_HEADERS,
        timeout=20,
    )
    response.raise_for_status()

    groups = response.json().get("items", [])
    team_ids = set()

    for group in groups:
        match = re.search(r"/groups/(\d+)", group["$ref"])
        if not match:
            continue

        group_id = match.group(1)

        response = requests.get(
            root + group_id + "/teams",
            params={"limit": 1000},
            headers=ESPN_HEADERS,
            timeout=20,
        )
        response.raise_for_status()

        for team in response.json().get("items", []):
            match = re.search(r"/teams/(\d+)", team["$ref"])
            if match:
                team_ids.add(match.group(1))

    if not team_ids:
        raise RuntimeError(f"Could not retrieve {gender} D1 team IDs.")

    _D1_TEAM_CACHE[gender] = team_ids
    return team_ids


def fetch_schedule(gender, game_date=None):
    if gender not in BASE_URLS:
        raise ValueError("Gender must be 'men' or 'women'.")

    if game_date is None:
        game_date = datetime.now().strftime("%Y%m%d")

    d1_team_ids = fetch_d1_team_ids(gender)

    response = requests.get(
        BASE_URLS[gender],
        params={
            "dates": game_date,
            "groups": 50,
            "limit": 500,
        },
        headers=ESPN_HEADERS,
        timeout=20,
    )
    response.raise_for_status()

    events = response.json().get("events", [])
    games = []

    for event in events:
        competitions = event.get("competitions", [])
        if not competitions:
            continue

        competitors = competitions[0].get("competitors", [])
        if len(competitors) != 2:
            continue

        home = next(
            (team for team in competitors if team.get("homeAway") == "home"),
            None,
        )

        away = next(
            (team for team in competitors if team.get("homeAway") == "away"),
            None,
        )

        if not home or not away:
            continue

        home_id = str(home.get("team", {}).get("id", ""))
        away_id = str(away.get("team", {}).get("id", ""))

        if home_id not in d1_team_ids or away_id not in d1_team_ids:
            continue

        games.append({
            "game_id": event.get("id"),
            "date": event.get("date"),
            "away_team": away.get("team", {}).get("displayName"),
            "home_team": home.get("team", {}).get("displayName"),
            "status": event.get("status", {}).get("type", {}).get("description"),
            "gender": gender,
        })

    return games
