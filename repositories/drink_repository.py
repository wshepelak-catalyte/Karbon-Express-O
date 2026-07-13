# repositories/drink_repository.py
from numbers import Number

from models.drink import Drink

class DrinkRepository:
    def __init__(self):
        self._drinks: list[Drink] = []

    def get_all(self) -> list[Drink]:
        return self._drinks

    def get_by_id(self, id: Number) -> Drink | None:
        return next((d for d in self._drinks if d.id == id), None)

    def add(self, drink: Drink) -> Drink:
        self._drinks.append(drink)
        return drink

    def update(self, id: Number, drink: Drink) -> Drink | None:
        existing_drink = self.get_by_id(id)
        if existing_drink:
            self._drinks.remove(existing_drink)
            self._drinks.append(drink)
            return drink
        return None

    def delete(self, id: Number) -> bool:
        drink = self.get_by_id(id)
        if drink:
            self._drinks.remove(drink)
            return True
        return False