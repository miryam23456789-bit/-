"""התאמת רשימת מוצרים לתקציב הבחירה."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

if __package__:
    from .catalog import Product
else:
    from catalog import Product


@dataclass(frozen=True)
class MatchResult:
    """תוצאת התאמה לתרחיש מציאת פריט יחיד."""

    product: Optional[Product]


def find_one_within_budget(
    products: list[Product],
    max_budget: Decimal,
) -> MatchResult:
    """בוחר מוצר אחד שמחירו אינו גבוה מהתקציב.

    Args:
        products: רשימת מוצרים מאותו סוג פריט.
        max_budget: התקציב המרבי שהמשתמש הגדיר.

    Returns:
        MatchResult: מוצר מתאים, או תוצאה ללא מוצר אם אין התאמה.
    """
    for product in products:
        if product.price <= max_budget:
            return MatchResult(product=product)
    return MatchResult(product=None)
