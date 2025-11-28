import uuid
import random
from datetime import datetime
from dataclasses import dataclass
from dataclasses import asdict


@dataclass
class User:
    """User data structure."""

    user_id: int
    name: str
    email: str
    created_at: str


class GenerateUser:
    """
    Random user generator:
    - Returns normal users
    - Occasionally returns a "bad" user with extra fields
    """

    EMAILS = ["example.com", "test.com", "mail.com", "dev.io"]
    NAMES = [
        "Alice",
        "Bob",
        "Charlie",
        "Diana",
        "Eve",
        "Frank",
        "Grace",
        "Hank",
        "Ivy",
        "Jack",
        "Luna",
        "Mason",
    ]

    def _generate_bad_user(self):
        """Generate a user with extra field 'country'."""
        name = random.choice(self.NAMES)
        params = {
            "name": name,
            "email": name + "@" + random.choice(self.EMAILS),
            "user_id": uuid.uuid4().int % 100000,
            "created_at": str(datetime.now()),
            "country": "ESP",
        }

        return params

    def __call__(self):
        """Generate a random user dict (~2% chance for bad user)."""
        if random.randint(1, 50) == 1:
            user = self._generate_bad_user()
            return user

        name = random.choice(self.NAMES)
        params = {
            "name": name,
            "email": name + "@" + random.choice(self.EMAILS),
            "user_id": uuid.uuid4().int % 100000,
            "created_at": str(datetime.now()),
        }
        user = asdict(User(**params))

        return user
