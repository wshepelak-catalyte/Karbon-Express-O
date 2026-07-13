from models.purchase import Purchase
from numbers import Number

class PurchaseRepository:
    def __init__(self):
        self._purchases: list[Purchase] = []

    def get_all(self) -> list[Purchase]:
        return self._purchases

    def get_by_id(self, id: Number) -> Purchase | None:
        return next((p for p in self._purchases if p.id == id), None)

    def add(self, purchase: Purchase) -> Purchase:
        self._purchases.append(purchase)
        return purchase

    def update(self, id: Number, purchase: Purchase) -> Purchase | None:
        existing_purchase = self.get_by_id(id)
        if existing_purchase:
            self._purchases.remove(existing_purchase)
            self._purchases.append(purchase)
            return purchase
        return None