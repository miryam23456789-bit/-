"""ממשק המשתמש עבור תרחיש חיפוש פריט יחיד."""

from dataclasses import dataclass


@dataclass(frozen=True)
class UserRequest:
    """בקשה גולמית שהזין המשתמש.

    הטקסט מכיל את סוג הפריט ואת התקציב המרבי, לדוגמה:
    "ספה, תקציב מקסימלי 1000 ש\"ח".
    """

    text: str


def read_request() -> UserRequest:
    """קורא סוג רהיט ותקציב מהטרמינל ומחזיר אותם בבקשה אחת.

    Returns:
        UserRequest: הבקשה הגולמית. טקסט ריק מציין שהמשתמש ביקש לצאת.
    """
    item_type = input("הקלידו סוג רהיט (או Enter לסיום): ").strip()
    if not item_type:
        return UserRequest(text="")

    budget = input("הקלידו תקציב מרבי ב-NIS (או Enter לסיום): ").strip()
    if not budget:
        return UserRequest(text="")

    return UserRequest(text=f"{item_type}|{budget}")


def show_result(result_text: str) -> None:
    """מציג למשתמש את תוצאת החיפוש או הודעה שאין מוצר מתאים.

    Args:
        result_text: מלל התוצאה שהוכן לתצוגה.
    """
    print(result_text)
