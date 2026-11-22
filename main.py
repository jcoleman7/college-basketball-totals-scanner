"""Small first-run test for the formula and Telegram delivery.

The full daily game/Fliff scan will be connected after we verify the
women's stats source and a Fliff odds feed that covers both leagues.
"""
import os
from dotenv import load_dotenv
from scanner.model import TeamStats, projected_total, line_difference, qualifies
from scanner.telegram_notify import send_telegram_message

load_dotenv()

def main():
    # Example-only values. Replace these with fetched stats and Fliff total.
    a = TeamStats("Example Team A", 1.20, 0.90, 70.0)
    b = TeamStats("Example Team B", 1.15, 0.95, 68.0)
    book_total = 145.5

    calc = projected_total(a, b)
    diff = line_difference(calc, book_total)

    print(f"Calculated total: {calc:.1f}")
    print(f"Fliff total:      {book_total:.1f}")
    print(f"Difference:       {diff:.1f}")
    print(f"Qualifies:        {qualifies(calc, book_total, float(os.getenv('ALERT_THRESHOLD', '10')))}")

    # Only send a test message when credentials are configured.
    if os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"):
        send_telegram_message(
            "College Basketball Scanner test\\n"
            f"Example calculated total: {calc:.1f}\\n"
            f"Example Fliff total: {book_total:.1f}\\n"
            f"Difference: {diff:.1f}"
        )

if __name__ == "__main__":
    main()
