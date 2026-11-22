"""עיבוד בקשות טבעיות והמרתן למידע מובנה."""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import re

if __package__:
    from .matcher import MatchResult
else:
    from matcher import MatchResult


@dataclass(frozen=True)
class SearchRequest:
    """בקשת חיפוש מובנית לתרחיש הראשון."""

    item_type: str
    max_budget: Decimal


def parse_search_request(user_text: str) -> SearchRequest:
    """מחלץ סוג פריט ותקציב מקסימלי מהקלט המובנה של ה-UI.

    Args:
        user_text: סוג פריט ותקציב בפורמט "סוג|תקציב".

    Returns:
        SearchRequest: סוג הפריט והתקציב המאותר.

    Raises:
        ValueError: כאשר אין מספיק מידע כדי לבנות בקשה מוגדרת.
    """
    item_type, separator, budget_text = user_text.partition("|")
    if not separator or not item_type.strip() or not budget_text.strip():
        raise ValueError("יש להזין סוג רהיט ותקציב.")

    # מאפשר להזין גם סכום עם מטבע, למשל "1000 NIS" או "1000 ש\"ח".
    amount = re.fullmatch(
        r"\s*(\d+(?:[.,]\d+)?)\s*(?:NIS|ש[\"'״]?ח|₪)?\s*",
        budget_text,
        flags=re.IGNORECASE,
    )
    if amount is None:
        raise ValueError("התקציב חייב להיות מספר חיובי.")

    try:
        max_budget = Decimal(amount.group(1).replace(",", "."))
    except InvalidOperation as error:
        raise ValueError("התקציב חייב להיות מספר חיובי.") from error

    if max_budget <= 0:
        raise ValueError("התקציב חייב להיות מספר חיובי.")

    return SearchRequest(item_type=item_type.strip(), max_budget=max_budget)


def format_match_result(match: MatchResult) -> str:
    """ממיר תוצאת התאמה למלל מתאים להצגה למשתמש.

    Args:
        match: תוצאת מודול Matcher.

    Returns:
        str: פריט מתאים עם המחיר, או הודעה שאין מוצר מתאים.
    """
    if match.product is None:
        return "No matching item found within budget"
    return f"{match.product.name} - {match.product.price} NIS"
