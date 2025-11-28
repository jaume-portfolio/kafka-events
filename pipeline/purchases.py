import uuid
import random
from datetime import datetime
from dataclasses import dataclass
from dataclasses import asdict


@dataclass
class Purchase:
    """Purchase data structure."""

    id: int
    user_id: int
    product_name: str
    quantity_kg: float
    total_price: float
    created_at: str


class GeneratePurchase:
    """
    Random purchase generator:
    - Generates purchase records for a given user
    - Calculates total price based on product and quantity
    """

    PRODUCTS = {
        "apples": 2.5,
        "bananas": 2.6,
        "kiwis": 4.5,
        "cherries": 8.5,
    }

    def __init__(self, user_id):
        """Set user ID for generated purchases."""
        self.user_id = user_id

    def __call__(self):
        """Generate a random purchase dictionary."""
        product_name = random.choice(list(self.PRODUCTS.keys()))
        quantity_kg = random.uniform(0.5, 4)
        params = {
            "id": uuid.uuid4().int % 100000,
            "user_id": self.user_id,
            "product_name": product_name,
            "quantity_kg": quantity_kg,
            "total_price": quantity_kg * self.PRODUCTS[product_name],
            "created_at": str(datetime.now()),
        }

        purchase = Purchase(**params)

        return asdict(purchase)
