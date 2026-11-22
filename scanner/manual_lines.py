
from scanner.engine import calculate_game
from scanner.model import line_difference, qualifies


def run_manual_scan(games, all_stats):
    results = []
    skipped = 0

    print("\nMANUAL FLIFF TOTAL ENTRY")
    print("Enter the full-game over/under total for each matchup.")
    print("Press Enter to skip a game.\n")

    for i, game in enumerate(games, start=1):
        matchup = f"{game['away_team']} @ {game['home_team']}"

        while True:
            entry = input(f"{i}/{len(games)} - {matchup}: Fliff O/U: ").strip()

            if not entry:
                skipped += 1
                break

            try:
                fliff_total = float(entry)
                if fliff_total <= 0:
                    print("Enter a positive number.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")

        if not entry:
            continue

        projection = calculate_game(game, all_stats)
        predicted = projection["projected_total"]
        difference = line_difference(predicted, fliff_total)

        result = {
            **projection,
            "fliff_total": fliff_total,
            "difference": difference,
            "qualifies": qualifies(predicted, fliff_total),
        }

        results.append(result)

        if result["qualifies"]:
            print(
                f"  *** ALERT: {difference:.2f} POINT DIFFERENCE ***"
            )

    alerts = [r for r in results if r["qualifies"]]

    print("\n========== SCAN RESULTS ==========")
    print(f"Games entered: {len(results)}")
    print(f"Games skipped: {skipped}")
    print(f"Qualifying alerts: {len(alerts)}")

    for r in alerts:
        print(
            f"\n{r['away_team']} @ {r['home_team']}"
            f"\nModel: {r['projected_total']:.2f}"
            f"\nFliff: {r['fliff_total']:.2f}"
            f"\nDifference: {r['difference']:.2f}"
        )

    return results
