"""TeamRankings men's Division I stats reader.

The parser deliberately selects the column named '2026'. It does not use
Last 3, Last 1, Home, Away, or 2025.
"""
from io import StringIO
import pandas as pd
import requests

BASE = "https://www.teamrankings.com/ncaa-basketball/stat"
STAT_URLS = {
    "offensive_efficiency": f"{BASE}/offensive-efficiency",
    "defensive_efficiency": f"{BASE}/defensive-efficiency",
    "possessions_per_game": f"{BASE}/possessions-per-game",
}

def _find_2026_table(html: str) -> dict[str, float]:
    tables = pd.read_html(StringIO(html))
    for table in tables:
        # Normalize potentially multi-level headers.
        if isinstance(table.columns, pd.MultiIndex):
            table.columns = [
                " ".join(str(x) for x in col if str(x) != "nan").strip()
                for col in table.columns
            ]
        cols = [str(c).strip() for c in table.columns]
        team_col = next((c for c in cols if c.lower() == "team" or c.lower().endswith(" team")), None)
        year_col = next((c for c in cols if c == "2026" or c.endswith(" 2026")), None)
        if team_col and year_col:
            result = {}
            for _, row in table.iterrows():
                team = str(row[team_col]).strip()
                raw = str(row[year_col]).strip().replace(",", "")
                if not team or team.lower() in {"nan", "team"} or raw in {"--", "-", "nan"}:
                    continue
                try:
                    result[team] = float(raw)
                except ValueError:
                    continue
            if result:
                return result
    raise RuntimeError("Could not find a TeamRankings table with Team and 2026 columns.")

def fetch_stat(stat_name: str) -> dict[str, float]:
    if stat_name not in STAT_URLS:
        raise ValueError(f"Unknown stat: {stat_name}")
    response = requests.get(
        STAT_URLS[stat_name],
        headers={"User-Agent": "Mozilla/5.0 (compatible; CollegeBasketballScanner/0.1)"},
        timeout=25,
    )
    response.raise_for_status()
    return _find_2026_table(response.text)

def fetch_mens_team_stats() -> dict[str, dict[str, float]]:
    """Return {team: {offensive_efficiency, defensive_efficiency, possessions_per_game}}."""
    datasets = {name: fetch_stat(name) for name in STAT_URLS}
    teams = set.intersection(*(set(data) for data in datasets.values()))
    return {
        team: {name: datasets[name][team] for name in STAT_URLS}
        for team in sorted(teams)
    }

def fetch_womens_team_stats():
    """Not implemented: TeamRankings women's equivalent URLs have not been verified.

    This intentionally raises instead of substituting men's data or guessing
    a URL. We'll connect a verified women's D-I source in the next build step.
    """
    raise NotImplementedError(
        "Women's TeamRankings stat pages are not verified yet; do not substitute men's stats."
    )
