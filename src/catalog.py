"""אחזקת קטלוג מוצרים וחיפוש פריטים לפי סוג."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Product:
    """ייצוג מוצר יחיד בקטלוג."""

    id: str
    name: str
    item_type: str
    price: Decimal


# נתוני דוגמה עבור תרחיש חיפוש פריט יחיד.
_PRODUCTS = [
    Product(
        id="sofa-1",
        name="Modern Sofa",
        item_type="sofa",
        price=Decimal("700"),
    ),
    Product(
        id="rug-1",
        name="Modern Rug",
        item_type="rug",
        price=Decimal("150"),
    ),
]

_ITEM_TYPE_ALIASES = {
    "sofa": "sofa",
    "ספה": "sofa",
    "ספות": "sofa",
    "rug": "rug",
    "שטיח": "rug",
    "שטיחים": "rug",
}


def search_by_item_type(item_type: str) -> list[Product]:
    """מחזיר מוצרים מהקטלוג לפי סוג פריט.

    Args:
        item_type: סוג הפריט המבוקש, באנגלית או בעברית.

    Returns:
        list[Product]: כל המוצרים בקטלוג התואמים לסוג הפריט.
    """
    normalized_type = _ITEM_TYPE_ALIASES.get(item_type.strip().casefold())
    if normalized_type is None:
        return []
    return [product for product in _PRODUCTS if product.item_type == normalized_type]
