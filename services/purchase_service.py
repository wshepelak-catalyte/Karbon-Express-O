from repositories.purchase_repository import PurchaseRepository
from repositories.customer_repository import CustomerRepository
from models.purchase import Purchase
from models.customer import Customer

class PurchaseService:
    def __init__(self, purchase_repository: PurchaseRepository, customer_repository: CustomerRepository):
        self._purchase_repository = purchase_repository
        self._customer_repository = customer_repository

    def add_purchase(self, purchase: Purchase) -> Purchase:
        """Create a purchase record and link it to the stored customer account."""
        if purchase.customer is None or not hasattr(purchase.customer, "username"):
            raise ValueError("Purchase must include a customer with a username.")

        customer = self._customer_repository.get_by_username(purchase.customer.username)
        if customer is None:
            raise ValueError(f"Customer '{purchase.customer.username}' does not exist.")

        purchase.customer = customer
        customer.add_purchase(purchase)
        return self._purchase_repository.add(purchase)

    def get_customer_purchase_history(self, username: str) -> list[Purchase]:
        """Return all purchases for a given customer by username."""
        customer = self._customer_repository.get_by_username(username)
        if customer is None:
            return []
        return list(customer.purchases)
