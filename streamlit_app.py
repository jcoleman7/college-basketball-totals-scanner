import streamlit as st
from datetime import date, timedelta
from scanner.compare import compare_games

st.set_page_config(
    page_title="College Basketball Totals Scanner",
    page_icon="🏀",
    layout="wide",
)

st.title("🏀 College Basketball Totals Scanner")
st.caption("Compares model-projected game totals against sportsbook lines.")

selected_date = st.date_input(
    "Game date",
    value=date.today(),
)

threshold = 10.0

if st.button("🔄 Scan Games", type="primary"):
    game_date = selected_date.strftime("%Y%m%d")

    with st.spinner("Fetching odds, stats, and schedules..."):
        try:
            matched, unmatched = compare_games(game_date)

            if not matched:
                st.warning("No sportsbook lines could be matched for this date.")
            else:
                qualifying = [game for game in matched if game["difference"] >= threshold]

                unique_games = {
                    (game["game_date"], game["away_team"], game["home_team"])
                    for game in qualifying
                }

                col1, col2, col3 = st.columns(3)
                col1.metric("Matched lines", len(matched))
                col2.metric("Qualifying book-lines", len(qualifying))
                col3.metric("Unique qualifying games", len(unique_games))

                st.subheader("🚨 Qualifying Lines (10+ Point Difference)")

                if qualifying:
                    qualifying_data = []

                    for game in sorted(
                        qualifying,
                        key=lambda x: x["difference"],
                        reverse=True,
                    ):
                        qualifying_data.append({
                            "Date": game["game_date"],
                            "Matchup": f'{game["away_team"]} @ {game["home_team"]}',
                            "Sportsbook": game["book"],
                            "Model Total": round(game["model_total"], 1),
                            "Book Total": game["sportsbook_total"],
                            "Difference": round(game["difference"], 1),
                            "Direction": game["direction"],
                        })

                    st.dataframe(
                        qualifying_data,
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.info("No lines currently meet the 10-point threshold.")

                st.subheader("All Matched Sportsbook Lines")

                all_data = []

                for game in sorted(
                    matched,
                    key=lambda x: x["difference"],
                    reverse=True,
                ):
                    all_data.append({
                        "Date": game["game_date"],
                        "Matchup": f'{game["away_team"]} @ {game["home_team"]}',
                        "Sportsbook": game["book"],
                        "Model Total": round(game["model_total"], 1),
                        "Book Total": game["sportsbook_total"],
                        "Difference": round(game["difference"], 1),
                        "Direction": game["direction"],
                    })

                st.dataframe(
                    all_data,
                    use_container_width=True,
                    hide_index=True,
                )

                if unmatched:
                    with st.expander(f"Unmatched lines ({len(unmatched)})"):
                        for game in unmatched:
                            st.write(
                                f'{game["away_team"]} @ {game["home_team"]} — {game["book"]}'
                            )

                st.caption(
                    "Model projections are estimates, not guarantees. "
                    "A large difference does not ensure a profitable bet."
                )

        except Exception as error:
            st.error(f"Scanner error: {error}")