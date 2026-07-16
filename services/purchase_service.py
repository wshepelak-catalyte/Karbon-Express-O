from repositories.purchase_repository import PurchaseRepository
from datetime import datetime, timezone
from typing import Any
from decimal import Decimal
from models.purchase import Purchase
from models.customer import Customer
from exceptions import PurchaseIdNotFound

class PurchaseService:
    def __init__(self, purchase_repository: PurchaseRepository):
        self._purchase_repository = purchase_repository
        self._empty_ids = []
        self._next_id = 0

    def create_purchase(
                self,
                timestamp : datetime,
                items : list[Any],
                total_cost : float | Decimal,
                customer : Customer 
            ):
        created_purchase_id = None
        if len(self._empty_ids) == 0:
            created_purchase_id = self._next_id
            self._next_id += 1
        else:
            created_purchase_id = self._empty_ids.pop()

        created_purchase = Purchase(
                id=created_purchase_id,
                timestamp=timestamp,
                items=items,
                total_cost=Decimal(str(total_cost)),
                customer=customer
            )
        self._purchase_repository.add(created_purchase)

    def get_all_purchases(self):
        return self._purchase_repository.get_all()
    
    def get_total_spending(self) -> Decimal:
        total = Decimal("0")
        for purchase in self._purchase_repository.get_all():
            total += purchase.total_cost
        return total
    
    def get_purchase_by_id(self, id : int) -> Purchase:
        returned_purchase = self._purchase_repository.get_by_id(id)
        if returned_purchase is None:
            raise PurchaseIdNotFound(f"No purchase with ID {str(id)} was found in the repository")
        return returned_purchase
    
    def update_purchase(
                self,
                id : int,
                timestamp : datetime,
                items : list[Any],
                total_cost : Decimal | float,
                customer : Customer
            ):
        old_purchase = self._purchase_repository.get_by_id(id)
        if old_purchase is None:
            raise PurchaseIdNotFound(f"No purchase with ID {str(id)} was found in the repository")
        updated_purchase = Purchase(
            id=id,
            timestamp=timestamp,
            items=items,
            total_cost=Decimal(str(total_cost)),
            customer=customer
        )

        self._purchase_repository.update(id, updated_purchase)

    def delete_ingredient(self, id : int):
        deleted_purchase = self._purchase_repository.get_by_id(id)
        if deleted_purchase is None:
            raise PurchaseIdNotFound(f"No purchase with ID {str(id)} was found in the repository")
        self._empty_ids.append(deleted_purchase.id)
        self._purchase_repository.delete(id)
