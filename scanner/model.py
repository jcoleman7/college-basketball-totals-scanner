from dataclasses import dataclass

@dataclass
class TeamStats:
    team: str
    offensive_efficiency: float
    defensive_efficiency: float
    possessions_per_game: float

def team_score(stats: TeamStats) -> float:
    """User's exact formula: (OE * possessions) + (DE * possessions)."""
    return (
        stats.offensive_efficiency * stats.possessions_per_game
        + stats.defensive_efficiency * stats.possessions_per_game
    )

def projected_total(team_a: TeamStats, team_b: TeamStats) -> float:
    """Average the two team scores, exactly as requested."""
    return (team_score(team_a) + team_score(team_b)) / 2

def line_difference(calculated_total: float, book_total: float) -> float:
    return abs(calculated_total - book_total)

def qualifies(calculated_total: float, book_total: float, threshold: float = 10.0) -> bool:
    return line_difference(calculated_total, book_total) >= threshold
