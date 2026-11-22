
import requests
import re

BASE = "https://sports.core.api.espn.com/v2/sports/basketball/leagues/"

LEAGUES = {
    "MEN": "mens-college-basketball",
    "WOMEN": "womens-college-basketball",
}

for label, league in LEAGUES.items():
    root = BASE + league + "/seasons/2027/types/2/groups/"

    groups_response = requests.get(
        root + "50/children",
        params={"limit": 1000},
        timeout=20,
    )
    groups_response.raise_for_status()

    groups = groups_response.json()["items"]
    team_ids = set()

    for group in groups:
        group_id = re.search(
            r"/groups/(\d+)",
            group["$ref"],
        ).group(1)

        response = requests.get(
            root + group_id + "/teams",
            params={"limit": 1000},
            timeout=20,
        )
        response.raise_for_status()

        teams = response.json()["items"]

        for team in teams:
            team_id = re.search(
                r"/teams/(\d+)",
                team["$ref"],
            ).group(1)

            team_ids.add(team_id)

    print("\n", label)
    print("Conferences:", len(groups))
    print("D1 team IDs:", len(team_ids))
    print("Wilson excluded:", "111914" not in team_ids)
    print("Louisiana Christian excluded:", "2347" not in team_ids)
