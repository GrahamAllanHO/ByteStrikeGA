from datetime import datetime
from typing import List


def format_names(names: List[str]) -> List[str]:
    # Example: ["alice", "bob"] -> ["ALICE", "BOB"]
    return [name.upper() for name in names]


def format_dates(dates: List[str]) -> List[str]:
    # Using the same pattern as format_names above:
    # Example: ["2026-01-17", "2026-02-20"] -> ["Jan 17, 2026", "Feb 20, 2026"]
    return [
        datetime.strptime(date, "%Y-%m-%d").strftime("%b %d, %Y").replace(" 0", " ")
        for date in dates
    ]

def calculate(a: float, b: float, c: float) -> float:
    """
    Calculate the area of a triangle given three side lengths using Heron's formula.

    Args:
        a: Length of side A
        b: Length of side B
        c: Length of side C

    Returns:
        The area of the triangle
    """
    # Heron's formula: sqrt(s * (s - a) * (s - b) * (s - c))
    s = (a + b + c) / 2
    return (s * (s - a) * (s - b) * (s - c)) ** 0.5 


