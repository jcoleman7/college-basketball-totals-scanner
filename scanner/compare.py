
"""Match sportsbook totals to model projections."""

import re

from scanner.schedule import fetch_schedule
from scanner.teamrankings import fetch_mens_team_stats
from scanner.engine import calculate_game
from scanner.team_mapping import teamrankings_name, normalize_name
from scanner.odds import fetch_totals


def team_key(name, available_names):
    """Normalize a team name to its TeamRankings name."""
    mapped = teamrankings_name(name, available_names)

    if mapped:
        return normalize_name(mapped)

    # Fallback for names not recognized by the ESPN mapper.
    name = name.lower().strip()
    name = name.replace("&", " and ")
    name = re.sub(r"[^a-z0-9]", "", name)

    aliases = {
        "southernmississippi": "southernmiss",
        "southernmiss": "southernmiss",
    }

    return aliases.get(name, name)


def compare_games(game_date):
    print("Fetching sportsbook totals...")
    odds = fetch_totals(game_date)

    print("Fetching TeamRankings stats...")
    stats = fetch_mens_team_stats()
    available_names = stats.keys()

    eastern_dates = sorted({line["game_date"] for line in odds})
    projections = {}

    for date in eastern_dates:
        print(f"Fetching Division I schedule for {date}...")
        games = fetch_schedule("men", date)

        for game in games:
            try:
                result = calculate_game(game, stats)

                key = frozenset([
                    team_key(game["away_team"], available_names),
                    team_key(game["home_team"], available_names),
                ])

                projections[key] = result

            except ValueError as error:
                print("MODEL MATCH ERROR:", error)

    matched = []
    unmatched = []

    for line in odds:
        key = frozenset([
            team_key(line["away_team"], available_names),
            team_key(line["home_team"], available_names),
        ])

        projection = projections.get(key)

        if projection is None:
            unmatched.append(line)
            continue

        model_total = projection["projected_total"]
        sportsbook_total = line["total"]
        difference = abs(model_total - sportsbook_total)

        matched.append({
            "away_team": line["away_team"],
            "home_team": line["home_team"],
            "game_date": line["game_date"],
            "book": line["book"],
            "model_total": model_total,
            "sportsbook_total": sportsbook_total,
            "difference": difference,
            "direction": (
                "Model higher"
                if model_total > sportsbook_total
                else "Model lower"
            ),
            "qualifies": difference >= 10,
        })

    return matched, unmatched
