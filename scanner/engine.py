
from scanner.model import TeamStats, projected_total
from scanner.team_mapping import teamrankings_name


def build_team_stats(espn_name, all_stats):
    """Find a team's TeamRankings data and create a TeamStats object."""

    tr_name = teamrankings_name(espn_name, all_stats.keys())

    if tr_name is None:
        raise ValueError(
            f"No TeamRankings match found for: {espn_name}"
        )

    stats = all_stats[tr_name]

    return TeamStats(
        team=espn_name,
        offensive_efficiency=stats["offensive_efficiency"],
        defensive_efficiency=stats["defensive_efficiency"],
        possessions_per_game=stats["possessions_per_game"],
    )


def calculate_game(game, all_stats):
    """Calculate a game's projected total using the exact requested formula."""

    away = build_team_stats(game["away_team"], all_stats)
    home = build_team_stats(game["home_team"], all_stats)

    total = projected_total(away, home)

    return {
        "away_team": away.team,
        "home_team": home.team,
        "projected_total": total,
    }
