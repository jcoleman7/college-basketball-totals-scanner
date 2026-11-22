# College Basketball Scanner — starter project

This is the first working foundation for the scanner:
- Your exact scoring formula
- A TeamRankings men's stats reader that explicitly selects the `2026` column
- Telegram phone-notification delivery
- A configurable 10-point alert threshold

## Important: what is not connected yet

This is **not yet the complete automatic scanner**. Before enabling live alerts, we still need to connect:
1. A verified women's Division I source for offensive efficiency, defensive efficiency, and possessions per game. The men's TeamRankings pages are verified; equivalent women's pages have not been verified, so this project refuses to guess or reuse men's data.
2. A reliable Fliff odds feed covering both men's and women's D-I full-game totals.
3. A D-I daily schedule feed and team-name matching.

The app should never silently substitute another sportsbook's total for Fliff's total.

## Setup

1. Install Python 3.11 or newer.
2. Unzip this folder.
3. Open Terminal in this folder.
4. Install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   # Windows: .venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env`.

## Telegram phone notifications

1. Install Telegram on your iPhone and sign in.
2. In Telegram, search for `@BotFather`, open it, and send `/newbot`.
3. Follow its prompts. Copy the bot token into `TELEGRAM_BOT_TOKEN` in `.env`.
4. Open your new bot and press **Start** (or send `/start`).
5. In a browser, open this URL, replacing `YOUR_TOKEN` with your token:

   `https://api.telegram.org/botYOUR_TOKEN/getUpdates`

6. Find `message` → `chat` → `id` in the returned JSON. Put that number in `TELEGRAM_CHAT_ID`.
7. Keep `.env` private. Never share your bot token or upload it to GitHub.

## Run the first test

```bash
python main.py
```

The sample numbers are illustrative only. They are not live team statistics or a real Fliff market. Once Telegram is configured, this sends a test notification to your phone.

## Formula implemented

For each team:

`team_score = (offensive_efficiency * possessions_per_game) + (defensive_efficiency * possessions_per_game)`

Then:

`calculated_total = (team_a_score + team_b_score) / 2`

Alert when:

`abs(calculated_total - fliff_full_game_total) >= 10.0`

No division by 100 is applied; the implementation follows the formula you specified and the decimal efficiency values displayed by TeamRankings.

## Next build step

Connect and validate the women's D-I statistics source and the Fliff totals feed, then add the daily schedule scanner and background polling.
