from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, computed_field, model_validator


class RoomImageRequest(BaseModel):
    image_uri: str


class RoomAnalysis(BaseModel):
    room_type: Literal["living_room", "other"]
    colors: list[str] = Field(default_factory=list)
    existing_furniture: list[str] = Field(default_factory=list)


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class UserProfile(BaseModel):
    style: str = Field(min_length=1)
    budget: Decimal = Field(gt=0)
    needs: list[str] = Field(default_factory=list)


class Product(BaseModel):
    id: str
    name: str
    category: str
    price: Decimal = Field(gt=0)
    style_tags: list[str] = Field(default_factory=list)


class ProductSearchRequest(BaseModel):
    style: str
    max_price: Decimal = Field(gt=0)


class ShoppingBasket(BaseModel):
    budget: Decimal = Field(gt=0)
    items: list[Product] = Field(default_factory=list)

    @computed_field
    @property
    def total_price(self) -> Decimal:
        return sum((item.price for item in self.items), Decimal("0"))

    @model_validator(mode="after")
    def ensure_within_budget(self):
        if self.total_price > self.budget:
            raise ValueError("Basket total exceeds budget")
        return self


# Interfaces for the vision and conversation modules.
def analyze_room(request: RoomImageRequest) -> RoomAnalysis:
    raise NotImplementedError


def extract_profile(messages: list[ChatMessage]) -> UserProfile:
    raise NotImplementedError


MOCK_PRODUCTS = [
    Product(
        id="sofa-1",
        name="ספה מודרנית",
        category="sofa",
        price=Decimal("700"),
        style_tags=["modern"],
    ),
    Product(
        id="rug-1",
        name="שטיח מודרני",
        category="rug",
        price=Decimal("150"),
        style_tags=["modern"],
    ),
    Product(
        id="lamp-1",
        name="מנורת רצפה",
        category="lighting",
        price=Decimal("100"),
        style_tags=["modern"],
    ),
    Product(
        id="chair-1",
        name="כורסה קלאסית",
        category="chair",
        price=Decimal("300"),
        style_tags=["classic"],
    ),
]


def search_products(request: ProductSearchRequest) -> list[Product]:
    style = request.style.casefold()
    return [
        product
        for product in MOCK_PRODUCTS
        if style in {tag.casefold() for tag in product.style_tags}
        and product.price <= request.max_price
    ]


def recommend(profile: UserProfile) -> ShoppingBasket:
    candidates = search_products(
        ProductSearchRequest(style=profile.style, max_price=profile.budget)
    )

    selected = []
    remaining = profile.budget

    for product in candidates:
        if product.price <= remaining:
            selected.append(product)
            remaining -= product.price

    return ShoppingBasket(budget=profile.budget, items=selected)


basket = recommend(
    UserProfile(style="modern", budget=Decimal("1000"))
)

print([item.name for item in basket.items])
print(basket.total_price)  # 950
